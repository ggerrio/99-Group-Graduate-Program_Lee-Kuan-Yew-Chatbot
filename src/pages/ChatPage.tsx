import React from 'react';
import { useChatStore } from '@/store/useChatStore';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatContainer } from '@/components/chat/ChatContainer';
import { ChatFooter } from '@/components/chat/ChatFooter';

export const ChatPage: React.FC = () => {
  const {
    messages,
    inputPrompt,
    isGenerating,
    setInputPrompt,
    addMessage,
    clearMessages,
    createNewChat,
    setIsGenerating,
  } = useChatStore();

  const handleSend = (text: string) => {
    addMessage(text, 'user');
    setIsGenerating(true);

    // Simulated UI-only response echo for Phase 1 testing
    setTimeout(() => {
      addMessage(
        `Thank you for your inquiry: *"__${text}__"*\n\nThis is a Phase 1 frontend placeholder response. In Phase 2 & 3, this will return factually grounded answers from Lee Kuan Yew's historical texts via Retrieval-Augmented Generation (RAG) and Google Gemini 2.5.`,
        'assistant'
      );
      setIsGenerating(false);
    }, 1200);
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
