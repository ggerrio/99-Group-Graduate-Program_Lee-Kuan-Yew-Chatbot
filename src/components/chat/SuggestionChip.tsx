import React from 'react';
import { cn } from '@/lib/utils';

interface SuggestionChipProps {
  label: string;
  onClick: () => void;
  icon?: React.ReactNode;
  className?: string;
}

export const SuggestionChip: React.FC<SuggestionChipProps> = ({
  label,
  onClick,
  icon,
  className,
}) => {
  return (
    <button
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-2 rounded-full border border-border bg-card px-3.5 py-1.5 text-xs font-medium text-muted-foreground shadow-2xs transition-all hover:bg-accent hover:text-foreground hover:border-primary/40 active:scale-95 select-none',
        className
      )}
    >
      {icon && <span className="text-primary">{icon}</span>}
      <span>{label}</span>
    </button>
  );
};
