import axios from 'axios';

const API_KEY = 'qPzT2B7AhloXs9BEgmQcoaBuMpabQO6s';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5010',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`, 
  },
});

export default axiosInstance;