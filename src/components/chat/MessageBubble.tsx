import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, User, Copy, Check } from 'lucide-react';
import { ChatMessage } from '@/types';
import { Avatar } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { MarkdownRenderer } from './MarkdownRenderer';
import { cn } from '@/lib/utils';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={cn(
        'group relative flex gap-3 md:gap-4 p-4 rounded-2xl transition-colors',
        isUser
          ? 'bg-primary/5 dark:bg-primary/10 border border-primary/10 ml-auto max-w-[85%]'
          : 'bg-card border border-border shadow-xs max-w-[95%]'
      )}
    >
      <Avatar
        fallback={
          isUser ? (
            <User className="h-4 w-4 text-muted-foreground" />
          ) : (
            <Bot className="h-4 w-4 text-primary" />
          )
        }
        className={cn(
          'h-8 w-8 shrink-0 rounded-xl',
          isUser ? 'bg-secondary' : 'bg-primary/10'
        )}
      />

      <div className="flex-1 space-y-1.5 overflow-hidden">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold tracking-tight">
              {isUser ? 'You' : 'Lee Kuan Yew AI'}
            </span>
            <span className="text-[10px] text-muted-foreground">{message.timestamp}</span>
          </div>

          {!isUser && (
            <Button
              variant="ghost"
              size="icon"
              onClick={handleCopy}
              className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Copy response"
            >
              {copied ? (
                <Check className="h-3.5 w-3.5 text-emerald-500" />
              ) : (
                <Copy className="h-3.5 w-3.5 text-muted-foreground" />
              )}
            </Button>
          )}
        </div>

        <MarkdownRenderer content={message.content} />
      </div>
    </motion.div>
  );
};
