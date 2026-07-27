import axios, { AxiosError } from 'axios';
import { ChatRequest, ChatResponseData, ApiResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const chatApiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30-second timeout for LLM & RAG retrieval
});

export const chatApi = {
  /**
   * Sends a message to the backend chat API (POST /api/v1/chat)
   */
  sendMessage: async (payload: ChatRequest): Promise<ChatResponseData> => {
    try {
      const response = await chatApiClient.post<ApiResponse<ChatResponseData>>(
        '/api/v1/chat',
        payload
      );

      if (!response.data.success || !response.data.data) {
        throw new Error(response.data.message || 'Failed to generate response from backend.');
      }

      return response.data.data;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        const axiosErr = error as AxiosError<ApiResponse<unknown>>;
        
        if (axiosErr.code === 'ECONNABORTED' || axiosErr.message.includes('timeout')) {
          throw new Error('Request timed out while waiting for AI response. Please try again.');
        }

        if (!axiosErr.response) {
          throw new Error('Unable to connect to backend server. Please verify the backend is running.');
        }

        const status = axiosErr.response.status;
        const serverData = axiosErr.response.data;

        if (status === 422) {
          throw new Error('Invalid request payload sent to chat API.');
        }

        if (serverData && typeof serverData === 'object' && 'message' in serverData) {
          throw new Error(String(serverData.message));
        }

        if (status >= 500) {
          throw new Error(`Server error (${status}). The AI service encountered an issue.`);
        }
      }

      if (error instanceof Error) {
        throw error;
      }

      throw new Error('An unexpected error occurred while communicating with the chat service.');
    }
  },
};
