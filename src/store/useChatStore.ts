import { create } from 'zustand';
import { ChatMessage, ChatConversation } from '@/types';

const INITIAL_DEMO_MESSAGES: ChatMessage[] = [
  {
    id: 'msg-1',
    role: 'assistant',
    content:
      'Greetings. I am an AI representation modeled after **Lee Kuan Yew**, trained on my memoirs, public speeches, interviews, and official records.\n\nYou may ask me questions regarding governance, economic development, diplomacy, Singapore\'s history, or leadership philosophy.',
    timestamp: '10:00 AM',
  },
];

const DEMO_CONVERSATIONS: ChatConversation[] = [
  {
    id: 'conv-1',
    title: 'Governance & National Leadership',
    createdAt: '2026-07-26',
    updatedAt: '2026-07-26',
    messages: INITIAL_DEMO_MESSAGES,
  },
  {
    id: 'conv-2',
    title: 'Economic Transformation Strategy',
    createdAt: '2026-07-25',
    updatedAt: '2026-07-25',
    messages: [],
  },
  {
    id: 'conv-3',
    title: 'Geopolitics in Southeast Asia',
    createdAt: '2026-07-24',
    updatedAt: '2026-07-24',
    messages: [],
  },
];

interface ChatStoreState {
  conversations: ChatConversation[];
  activeConversationId: string;
  messages: ChatMessage[];
  inputPrompt: string;
  isGenerating: boolean;
  setInputPrompt: (text: string) => void;
  selectConversation: (id: string) => void;
  createNewChat: () => void;
  addMessage: (content: string, role?: 'user' | 'assistant') => void;
  clearMessages: () => void;
  setIsGenerating: (generating: boolean) => void;
}

export const useChatStore = create<ChatStoreState>((set, get) => ({
  conversations: DEMO_CONVERSATIONS,
  activeConversationId: 'conv-1',
  messages: INITIAL_DEMO_MESSAGES,
  inputPrompt: '',
  isGenerating: false,

  setInputPrompt: (inputPrompt) => set({ inputPrompt }),

  selectConversation: (id) => {
    const conv = get().conversations.find((c) => c.id === id);
    set({
      activeConversationId: id,
      messages: conv ? conv.messages : [],
    });
  },

  createNewChat: () => {
    const newId = `conv-${Date.now()}`;
    const newConv: ChatConversation = {
      id: newId,
      title: 'New Inquiry',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: INITIAL_DEMO_MESSAGES,
    };
    set((state) => ({
      conversations: [newConv, ...state.conversations],
      activeConversationId: newId,
      messages: INITIAL_DEMO_MESSAGES,
      inputPrompt: '',
    }));
  },

  addMessage: (content, role = 'user') => {
    const newMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role,
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    set((state) => ({
      messages: [...state.messages, newMessage],
      inputPrompt: '',
    }));
  },

  clearMessages: () => set({ messages: [] }),

  setIsGenerating: (isGenerating) => set({ isGenerating }),
}));
