import { useMutation } from '@tanstack/react-query';
import { chatApi } from '@/api/chatApi';
import { useChatStore } from '@/store/useChatStore';
import { ChatResponseData } from '@/types';

export const useSendMessage = () => {
  const {
    sessionId,
    filters,
    addMessage,
    updateMessage,
    setIsGenerating,
    setSessionId,
  } = useChatStore();

  const mutation = useMutation<
    ChatResponseData,
    Error,
    { message: string; targetAssistantMsgId?: string }
  >({
    mutationFn: async ({ message }) => {
      return await chatApi.sendMessage({
        message,
        session_id: sessionId,
        filters: filters || undefined,
      });
    },

    onMutate: () => {
      setIsGenerating(true);
    },

    onSuccess: (data, variables) => {
      setIsGenerating(false);

      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
      }

      if (variables.targetAssistantMsgId) {
        // Replace retry placeholder message
        updateMessage(variables.targetAssistantMsgId, {
          content: data.answer,
          citations: data.citations,
          isRefusal: data.is_refusal,
          isPost2015Inference: data.is_post_2015_inference,
          isError: false,
          errorMessage: undefined,
          retryPrompt: undefined,
        });
      } else {
        // Add new assistant message
        addMessage({
          role: 'assistant',
          content: data.answer,
          citations: data.citations,
          isRefusal: data.is_refusal,
          isPost2015Inference: data.is_post_2015_inference,
        });
      }
    },

    onError: (error, variables) => {
      setIsGenerating(false);
      const errMsg = error.message || 'An error occurred while getting response.';

      if (variables.targetAssistantMsgId) {
        updateMessage(variables.targetAssistantMsgId, {
          isError: true,
          errorMessage: errMsg,
          retryPrompt: variables.message,
        });
      } else {
        addMessage({
          role: 'assistant',
          content: '',
          isError: true,
          errorMessage: errMsg,
          retryPrompt: variables.message,
        });
      }
    },
  });

  const sendMessage = (text: string) => {
    if (!text.trim() || mutation.isPending) return;

    // 1. Add user message to UI
    addMessage({
      role: 'user',
      content: text.trim(),
    });

    // 2. Trigger mutation
    mutation.mutate({ message: text.trim() });
  };

  const retryMessage = (prompt: string, errorMsgId?: string) => {
    if (!prompt.trim() || mutation.isPending) return;

    if (errorMsgId) {
      updateMessage(errorMsgId, {
        isError: false,
        errorMessage: undefined,
        content: '',
      });
      mutation.mutate({ message: prompt.trim(), targetAssistantMsgId: errorMsgId });
    } else {
      sendMessage(prompt);
    }
  };

  return {
    sendMessage,
    retryMessage,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
  };
};
