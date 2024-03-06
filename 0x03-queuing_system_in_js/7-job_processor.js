#!/usr/bin/yarn dev
import { createQueue } from 'kue';

const blacklistedNumbers = ['4153518780', '4153518781'];

const sendNotification = (phoneNumber, message, job, done) => {
  job.progress(0);

  if (blacklistedNumbers.includes(phoneNumber)) {
    const errorMessage = `Phone number ${phoneNumber} is blacklisted`;
    console.error(errorMessage);
    done(new Error(errorMessage));
  } else {
    job.progress(50);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    done();
  }
};

const queue = createQueue({ name: 'push_notification_code_2', concurrency: 2 });

queue.process('push_notification_code_2', (job, done) => {
  const { phoneNumber, message } = job.data;

  sendNotification(phoneNumber, message, job, done);
});

console.log('Job processor is running...');
