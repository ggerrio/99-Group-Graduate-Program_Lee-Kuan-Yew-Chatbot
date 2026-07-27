import React from 'react';
import { NavLink } from 'react-router-dom';
import { cn } from '@/lib/utils';

interface NavigationItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
  className?: string;
}

export const NavigationItem: React.FC<NavigationItemProps> = ({
  to,
  icon,
  label,
  className,
}) => {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        cn(
          'flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition-colors select-none',
          isActive
            ? 'bg-primary text-primary-foreground font-semibold shadow-xs'
            : 'text-muted-foreground hover:bg-muted hover:text-foreground',
          className
        )
      }
    >
      <span className="h-4 w-4 shrink-0">{icon}</span>
      <span className="truncate">{label}</span>
    </NavLink>
  );
};
