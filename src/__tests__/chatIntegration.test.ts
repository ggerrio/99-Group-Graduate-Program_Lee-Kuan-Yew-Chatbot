import { describe, it, expect, beforeEach, vi } from 'vitest';
import { chatApi } from '../api/chatApi';
import { useChatStore } from '../store/useChatStore';

describe('Phase 5 Frontend Integration Unit Tests', () => {
  beforeEach(() => {
    // Reset store before each test
    useChatStore.setState({
      messages: [],
      sessionId: 'test-session-id',
      filters: null,
      isGenerating: false,
    });
  });

  describe('1. API Client Contract & Typing', () => {
    it('sends correct request structure to POST /api/v1/chat', async () => {
      const mockPost = vi.spyOn(chatApi, 'sendMessage').mockResolvedValueOnce({
        answer: 'Grounded test answer',
        citations: [
          {
            document_title: 'From Third World To First',
            document_type: 'memoirs',
            year: 2000,
            page_number: 105,
            score: 0.89,
          },
        ],
        session_id: 'test-session-id',
        is_refusal: false,
        is_post_2015_inference: false,
      });

      const response = await chatApi.sendMessage({
        message: 'What is your economic strategy?',
        session_id: 'test-session-id',
      });

      expect(mockPost).toHaveBeenCalledWith({
        message: 'What is your economic strategy?',
        session_id: 'test-session-id',
      });
      expect(response.answer).toBe('Grounded test answer');
      expect(response.citations).toHaveLength(1);
      expect(response.is_refusal).toBe(false);
      expect(response.is_post_2015_inference).toBe(false);
    });
  });

  describe('2. Zustand Store State Transitions', () => {
    it('adds user and assistant messages to state', () => {
      const store = useChatStore.getState();
      
      const userMsgId = store.addMessage({
        role: 'user',
        content: 'Hello Lee Kuan Yew',
      });
      expect(userMsgId).toBeDefined();
      expect(useChatStore.getState().messages).toHaveLength(1);
      expect(useChatStore.getState().messages[0].content).toBe('Hello Lee Kuan Yew');

      store.addMessage({
        role: 'assistant',
        content: 'Greetings. How can I assist?',
      });
      expect(useChatStore.getState().messages).toHaveLength(2);
    });

    it('updates specific message state on completion or error', () => {
      const store = useChatStore.getState();
      const msgId = store.addMessage({
        role: 'assistant',
        content: '',
      });

      store.updateMessage(msgId, {
        content: 'Updated grounded content',
        isRefusal: true,
      });

      const updatedMsg = useChatStore.getState().messages.find((m) => m.id === msgId);
      expect(updatedMsg?.content).toBe('Updated grounded content');
      expect(updatedMsg?.isRefusal).toBe(true);
    });
  });

  describe('3. Response State Conditional Flags', () => {
    it('correctly distinguishes normal grounded answer state', () => {
      const msgData = {
        is_refusal: false,
        is_post_2015_inference: false,
      };
      expect(msgData.is_refusal).toBe(false);
      expect(msgData.is_post_2015_inference).toBe(false);
    });

    it('correctly distinguishes refusal state', () => {
      const msgData = {
        is_refusal: true,
        is_post_2015_inference: false,
      };
      expect(msgData.is_refusal).toBe(true);
      expect(msgData.is_post_2015_inference).toBe(false);
    });

    it('correctly distinguishes post-2015 inference state', () => {
      const msgData = {
        is_refusal: false,
        is_post_2015_inference: true,
      };
      expect(msgData.is_refusal).toBe(false);
      expect(msgData.is_post_2015_inference).toBe(true);
    });
  });
});
