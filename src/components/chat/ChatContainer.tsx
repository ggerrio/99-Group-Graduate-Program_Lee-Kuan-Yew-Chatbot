import React from 'react';
import { ChatMessage } from '@/types';
import { MessageBubble } from './MessageBubble';
import { EmptyState } from './EmptyState';
import { TypingIndicator } from './TypingIndicator';
import { LoadingSkeleton } from './LoadingSkeleton';
import { useAutoScroll } from '@/hooks/useAutoScroll';

interface ChatContainerProps {
  messages: ChatMessage[];
  isGenerating?: boolean;
  onSelectPrompt: (promptText: string) => void;
  onRetry?: (prompt: string, messageId: string) => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isGenerating,
  onSelectPrompt,
  onRetry,
}) => {
  const containerRef = useAutoScroll<HTMLDivElement>([messages, isGenerating]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        <EmptyState onSelectPrompt={onSelectPrompt} />
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full"
    >
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} onRetry={onRetry} />
      ))}

      {isGenerating && (
        <div className="space-y-3">
          <LoadingSkeleton />
          <TypingIndicator />
        </div>
      )}
    </div>
  );
};
