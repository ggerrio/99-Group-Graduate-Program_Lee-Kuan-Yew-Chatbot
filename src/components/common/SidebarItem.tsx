import React from 'react';
import { cn } from '@/lib/utils';

interface SidebarItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick?: () => void;
  badge?: string | number;
  className?: string;
}

export const SidebarItem: React.FC<SidebarItemProps> = ({
  icon,
  label,
  active,
  onClick,
  badge,
  className,
}) => {
  return (
    <button
      onClick={onClick}
      className={cn(
        'group flex w-full items-center justify-between rounded-xl px-3 py-2 text-sm font-medium transition-all duration-150 text-left select-none',
        active
          ? 'bg-primary/10 text-primary font-semibold'
          : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground',
        className
      )}
    >
      <div className="flex items-center gap-3 min-w-0">
        <span
          className={cn(
            'h-4 w-4 shrink-0 transition-colors',
            active ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'
          )}
        >
          {icon}
        </span>
        <span className="truncate">{label}</span>
      </div>
      {badge !== undefined && (
        <span className="ml-2 shrink-0 rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
          {badge}
        </span>
      )}
    </button>
  );
};
