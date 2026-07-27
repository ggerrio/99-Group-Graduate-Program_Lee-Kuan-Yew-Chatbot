import React from 'react';
import { Bot } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';

export const LoadingSkeleton: React.FC = () => {
  return (
    <div className="flex gap-4 p-4 rounded-2xl bg-card border shadow-xs animate-pulse">
      <Avatar
        fallback={<Bot className="h-4 w-4 text-primary" />}
        className="h-8 w-8 bg-primary/10"
      />
      <div className="flex-1 space-y-2 py-1">
        <div className="h-3 w-1/4 rounded bg-muted" />
        <div className="h-3 w-3/4 rounded bg-muted/80" />
        <div className="h-3 w-1/2 rounded bg-muted/60" />
      </div>
    </div>
  );
};
