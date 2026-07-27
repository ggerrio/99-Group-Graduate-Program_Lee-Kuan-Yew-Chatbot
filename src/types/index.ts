export type Theme = 'light' | 'dark' | 'system';

export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  isStreaming?: boolean;
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
