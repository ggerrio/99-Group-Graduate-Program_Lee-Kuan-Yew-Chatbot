import React from 'react';
import { useChatStore } from '@/store/useChatStore';
import { useSendMessage } from '@/hooks/useChat';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatContainer } from '@/components/chat/ChatContainer';
import { ChatFooter } from '@/components/chat/ChatFooter';

export const ChatPage: React.FC = () => {
  const {
    messages,
    inputPrompt,
    isGenerating,
    setInputPrompt,
    clearMessages,
    createNewChat,
    setIsGenerating,
  } = useChatStore();

  const { sendMessage, retryMessage } = useSendMessage();

  const handleSend = (text: string) => {
    sendMessage(text);
  };

  const handleRetry = (prompt: string, messageId: string) => {
    retryMessage(prompt, messageId);
  };

  return (
    <div className="flex flex-col h-full w-full bg-background overflow-hidden">
      <ChatHeader
        title="Lee Kuan Yew Chatbot"
        onNewChat={createNewChat}
        onClearChat={clearMessages}
      />
      <ChatContainer
        messages={messages}
        isGenerating={isGenerating}
        onSelectPrompt={handleSend}
        onRetry={handleRetry}
      />
      <ChatFooter
        input={inputPrompt}
        onChangeInput={setInputPrompt}
        onSend={handleSend}
        isGenerating={isGenerating}
        onStop={() => setIsGenerating(false)}
      />
    </div>
  );
};
