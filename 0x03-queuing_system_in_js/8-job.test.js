import { Queue } from 'kue';
import createPushNotificationsJobs from './path-to-your-script'; // Update with the correct path

jest.mock('kue');

describe('createPushNotificationsJobs', () => {
  let queue: jest.Mocked<Queue>;

  beforeEach(() => {
    queue = new Queue();
    queue.testMode();
  });

  afterEach(() => {
    queue.shutdown(1000, (err) => {
      if (err) throw err;
    });
    jest.clearAllMocks();
  });

  it('should create push notification jobs', () => {
    const jobs = [
      { phoneNumber: '123', message: 'Test message 1' },
      { phoneNumber: '456', message: 'Test message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.jobs.length).toBe(2);

    queue.jobs.forEach((job) => {
      if (Math.random() < 0.5) {
        job.complete();
      } else {
        job.failed();
      }
    });

    expect(queue.jobs[0].emit).toHaveBeenCalledWith('enqueue');
    expect(queue.jobs[0].emit).toHaveBeenCalledWith('complete');
    expect(queue.jobs[1].emit).toHaveBeenCalledWith('enqueue');
    expect(queue.jobs[1].emit).toHaveBeenCalledWith('failed');
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).toThrowError('Jobs is not an array');
    expect(queue.jobs.length).toBe(0);
  });
});
