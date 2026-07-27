import React from 'react';
import { Sun, Moon, Monitor } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { Button } from '@/components/ui/button';
import { Theme } from '@/types';

export const ThemeToggle: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const cycleTheme = () => {
    const themes: Theme[] = ['light', 'dark', 'system'];
    const nextIndex = (themes.indexOf(theme) + 1) % themes.length;
    setTheme(themes[nextIndex]);
  };

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={cycleTheme}
      title={`Current theme: ${theme}. Click to switch.`}
    >
      {theme === 'light' && <Sun className="h-5 w-5 text-amber-500" />}
      {theme === 'dark' && <Moon className="h-5 w-5 text-indigo-400" />}
      {theme === 'system' && <Monitor className="h-5 w-5 text-muted-foreground" />}
    </Button>
  );
};
