import React from 'react';
import { Paperclip, Square, ArrowUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Tooltip } from '@/components/ui/tooltip';

interface ChatFooterProps {
  input: string;
  onChangeInput: (text: string) => void;
  onSend: (text: string) => void;
  isGenerating?: boolean;
  onStop?: () => void;
}

export const ChatFooter: React.FC<ChatFooterProps> = ({
  input,
  onChangeInput,
  onSend,
  isGenerating,
  onStop,
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isGenerating) {
        onSend(input.trim());
      }
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isGenerating) {
      onSend(input.trim());
    }
  };

  return (
    <div className="border-t bg-card/80 backdrop-blur-xs p-3 md:p-4 shrink-0">
      <form onSubmit={handleSubmit} className="mx-auto max-w-4xl space-y-2">
        <div className="relative flex items-end rounded-2xl border border-input bg-background shadow-xs focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all p-2">
          {/* File Attachment Placeholder */}
          <Tooltip content="Attachment disabled in Phase 1">
            <Button
              type="button"
              variant="ghost"
              size="icon"
              disabled
              className="h-9 w-9 text-muted-foreground shrink-0 rounded-xl"
            >
              <Paperclip className="h-4 w-4" />
            </Button>
          </Tooltip>

          {/* Multiline Text Input */}
          <textarea
            value={input}
            onChange={(e) => onChangeInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Lee Kuan Yew about governance, economy, diplomacy..."
            rows={1}
            className="flex-1 max-h-32 min-h-[40px] resize-none bg-transparent px-2 py-2 text-sm placeholder:text-muted-foreground focus:outline-none"
          />

          {/* Action Button: Send or Stop */}
          {isGenerating ? (
            <Tooltip content="Stop Generation (Placeholder)">
              <Button
                type="button"
                size="icon"
                onClick={onStop}
                variant="destructive"
                className="h-9 w-9 shrink-0 rounded-xl"
              >
                <Square className="h-4 w-4 fill-current" />
              </Button>
            </Tooltip>
          ) : (
            <Button
              type="submit"
              size="icon"
              disabled={!input.trim()}
              className="h-9 w-9 shrink-0 rounded-xl bg-primary text-primary-foreground transition-all hover:opacity-90 disabled:opacity-40"
            >
              <ArrowUp className="h-4 w-4" />
            </Button>
          )}
        </div>

        <div className="flex items-center justify-between px-2 text-[11px] text-muted-foreground">
          <span>Press Enter to send, Shift + Enter for new line</span>
          <span>Phase 1 UI Shell</span>
        </div>
      </form>
    </div>
  );
};
