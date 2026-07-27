export type Theme = 'light' | 'dark' | 'system';

export type MessageRole = 'user' | 'assistant' | 'system';

export interface CitationItem {
  document_title: string;
  document_type: string;
  year?: number | null;
  page_number: number;
  score: number;
}

export interface ChatFilters {
  document_type?: string;
  year?: number;
  category?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string | null;
  filters?: ChatFilters | null;
}

export interface ChatResponseData {
  answer: string;
  citations: CitationItem[];
  session_id: string;
  is_refusal: boolean;
  is_post_2015_inference: boolean;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  timestamp: string;
  data: T;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  isStreaming?: boolean;
  citations?: CitationItem[];
  isRefusal?: boolean;
  isPost2015Inference?: boolean;
  isError?: boolean;
  errorMessage?: string;
  retryPrompt?: string;
}

export interface ChatConversation {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messages: ChatMessage[];
}

export interface SuggestedPrompt {
  id: string;
  title: string;
  description: string;
  category: 'Leadership' | 'Economics' | 'Diplomacy' | 'Philosophy';
  promptText: string;
}

export interface HealthCheckResponse {
  status: string;
}

