import { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

export function setupInterceptors(axiosInstance: AxiosInstance): AxiosInstance {
  // Request Interceptor
  axiosInstance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      // Prepared for future token or API header injection
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  axiosInstance.interceptors.response.use(
    (response: AxiosResponse) => {
      return response;
    },
    (error) => {
      // Prepared for centralized error handling in future phases
      return Promise.reject(error);
    }
  );

  return axiosInstance;
}
