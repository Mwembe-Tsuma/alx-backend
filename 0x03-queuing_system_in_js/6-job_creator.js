#!/usr/bin/yarn dev
import { createQueue } from 'kue';

// Create a Kue job queue named 'push_notification_code'
const queue = createQueue({ name: 'push_notification_code' });

// Create a job with specific data
const job = queue.create('push_notification_code', {
  phoneNumber: '07045679939',
  message: 'Account registered',
});

// Event handlers for job lifecycle events
job
  .on('enqueue', () => {
    console.log('Notification job created:', job.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });

// Save the job to the queue
job.save();
