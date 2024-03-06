// Import the required libraries
import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

process.on('SIGINT', () => {
  client.quit();
});

async function setNewSchool(schoolName, value) {
  await setAsync(schoolName, value);
  console.log(`Value for ${schoolName} set successfully`);
}

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(`The value for ${schoolName} is: ${value}`);
  } catch (error) {
    console.error(`Error retrieving value for ${schoolName}: ${error.message}`);
  }
}

async function performOperations() {
  await displaySchoolValue('Holberton');
  await setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

performOperations();
