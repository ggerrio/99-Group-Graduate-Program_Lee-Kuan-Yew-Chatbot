import axios from 'axios';
import { setupInterceptors } from './interceptors';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const rawClient = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = setupInterceptors(rawClient);
