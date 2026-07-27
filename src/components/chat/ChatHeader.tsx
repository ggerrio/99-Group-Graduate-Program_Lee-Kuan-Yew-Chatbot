import React from 'react';
import { Sparkles, Trash2, Plus, Menu } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ThemeToggle } from '@/components/common/ThemeToggle';
import { useSidebar } from '@/hooks/useSidebar';

interface ChatHeaderProps {
  title: string;
  onNewChat: () => void;
  onClearChat: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({
  title,
  onNewChat,
  onClearChat,
}) => {
  const { sidebarOpen, toggleSidebar } = useSidebar();

  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-4 md:px-6 shrink-0">
      <div className="flex items-center gap-3 min-w-0">
        {!sidebarOpen && (
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="shrink-0"
            aria-label="Toggle Navigation"
          >
            <Menu className="h-5 w-5" />
          </Button>
        )}

        <div className="flex items-center gap-2 truncate">
          <div className="p-1.5 bg-primary/10 rounded-lg shrink-0">
            <Sparkles className="h-4 w-4 text-primary" />
          </div>
          <h1 className="text-base font-semibold truncate tracking-tight">{title}</h1>
          <Badge variant="outline" className="hidden sm:inline-flex text-[10px] ml-1">
            RAG Ready
          </Badge>
        </div>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <Button
          variant="ghost"
          size="sm"
          onClick={onNewChat}
          className="hidden sm:inline-flex gap-1.5 text-xs"
        >
          <Plus className="h-4 w-4" />
          <span>New Chat</span>
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={onClearChat}
          title="Clear messages"
          className="text-muted-foreground hover:text-destructive"
        >
          <Trash2 className="h-4.5 w-4.5" />
        </Button>
        <ThemeToggle />
      </div>
    </header>
  );
};
