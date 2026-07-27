import { create } from 'zustand';
import { ChatMessage, ChatConversation, ChatFilters, CitationItem } from '@/types';

// Helper to generate UUID session ID
const generateSessionId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `sess-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
};

const INITIAL_GREETING: ChatMessage = {
  id: 'msg-greeting',
  role: 'assistant',
  content:
    'Greetings. I am an AI representation modeled after **Lee Kuan Yew**, trained on my memoirs, public speeches, interviews, and official records.\n\nYou may ask me questions regarding governance, economic development, diplomacy, Singapore\'s history, or leadership philosophy.',
  timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
};

interface ChatStoreState {
  sessionId: string;
  conversations: ChatConversation[];
  activeConversationId: string;
  messages: ChatMessage[];
  inputPrompt: string;
  isGenerating: boolean;
  filters: ChatFilters | null;
  
  // Actions
  setSessionId: (sessionId: string) => void;
  setFilters: (filters: ChatFilters | null) => void;
  setInputPrompt: (text: string) => void;
  selectConversation: (id: string) => void;
  createNewChat: () => void;
  addMessage: (message: Partial<ChatMessage> & { content: string; role: 'user' | 'assistant' }) => string;
  updateMessage: (id: string, updates: Partial<ChatMessage>) => void;
  removeMessage: (id: string) => void;
  clearMessages: () => void;
  setIsGenerating: (generating: boolean) => void;
}

export const useChatStore = create<ChatStoreState>((set, get) => ({
  sessionId: generateSessionId(),
  conversations: [
    {
      id: 'conv-1',
      title: 'Lee Kuan Yew Persona Session',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: [INITIAL_GREETING],
    },
  ],
  activeConversationId: 'conv-1',
  messages: [INITIAL_GREETING],
  inputPrompt: '',
  isGenerating: false,
  filters: null,

  setSessionId: (sessionId) => set({ sessionId }),
  setFilters: (filters) => set({ filters }),
  setInputPrompt: (inputPrompt) => set({ inputPrompt }),

  selectConversation: (id) => {
    const conv = get().conversations.find((c) => c.id === id);
    set({
      activeConversationId: id,
      messages: conv ? conv.messages : [],
    });
  },

  createNewChat: () => {
    const newSessionId = generateSessionId();
    const newConvId = `conv-${Date.now()}`;
    const newConv: ChatConversation = {
      id: newConvId,
      title: 'New Inquiry',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: [INITIAL_GREETING],
    };
    set((state) => ({
      sessionId: newSessionId,
      conversations: [newConv, ...state.conversations],
      activeConversationId: newConvId,
      messages: [INITIAL_GREETING],
      inputPrompt: '',
    }));
  },

  addMessage: (msgData) => {
    const msgId = msgData.id || `msg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;
    const newMessage: ChatMessage = {
      id: msgId,
      role: msgData.role,
      content: msgData.content,
      timestamp: msgData.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      citations: msgData.citations,
      isRefusal: msgData.isRefusal,
      isPost2015Inference: msgData.isPost2015Inference,
      isError: msgData.isError,
      errorMessage: msgData.errorMessage,
      retryPrompt: msgData.retryPrompt,
    };

    set((state) => {
      const updatedMessages = [...state.messages, newMessage];
      const updatedConvs = state.conversations.map((c) =>
        c.id === state.activeConversationId ? { ...c, messages: updatedMessages, updatedAt: new Date().toISOString() } : c
      );
      return {
        messages: updatedMessages,
        conversations: updatedConvs,
        inputPrompt: msgData.role === 'user' ? '' : state.inputPrompt,
      };
    });

    return msgId;
  },

  updateMessage: (id, updates) => {
    set((state) => {
      const updatedMessages = state.messages.map((m) => (m.id === id ? { ...m, ...updates } : m));
      const updatedConvs = state.conversations.map((c) =>
        c.id === state.activeConversationId ? { ...c, messages: updatedMessages, updatedAt: new Date().toISOString() } : c
      );
      return {
        messages: updatedMessages,
        conversations: updatedConvs,
      };
    });
  },

  removeMessage: (id) => {
    set((state) => {
      const updatedMessages = state.messages.filter((m) => m.id !== id);
      const updatedConvs = state.conversations.map((c) =>
        c.id === state.activeConversationId ? { ...c, messages: updatedMessages } : c
      );
      return {
        messages: updatedMessages,
        conversations: updatedConvs,
      };
    });
  },

  clearMessages: () =>
    set((state) => {
      const updatedConvs = state.conversations.map((c) =>
        c.id === state.activeConversationId ? { ...c, messages: [] } : c
      );
      return { messages: [], conversations: updatedConvs };
    }),

  setIsGenerating: (isGenerating) => set({ isGenerating }),
}));
