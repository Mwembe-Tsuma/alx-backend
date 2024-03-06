import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();

const getAsync = promisify(client.get).bind(client);

const reserveSeat = async (number) => {
  await client.set('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const numberOfAvailableSeats = await getAsync('available_seats');
  return numberOfAvailableSeats ? parseInt(numberOfAvailableSeats) : 0;
};

reserveSeat(50);

let reservationEnabled = true;

app.get('/available_seats', (req, res) => {
  res.json({ numberOfAvailableSeats: getCurrentAvailableSeats() });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }

    return res.json({ status: 'Reservation in process' });
  });

  job
    .on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err.message || err.toString()}`);
    });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  await queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();

    if (currentAvailableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(currentAvailableSeats - 1);
      if (currentAvailableSeats - 1 === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });
});

const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
