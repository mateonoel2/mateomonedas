import axios from 'axios';
import { API_KEY } from './config'; 

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8080',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
  },
});

export default axiosInstance;
