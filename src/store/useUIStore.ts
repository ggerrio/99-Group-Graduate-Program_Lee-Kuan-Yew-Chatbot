import { create } from 'zustand';

interface UIState {
  searchQuery: string;
  isShortcutHelpOpen: boolean;
  setSearchQuery: (query: string) => void;
  setShortcutHelpOpen: (open: boolean) => void;
  toggleShortcutHelp: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  searchQuery: '',
  isShortcutHelpOpen: false,
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  setShortcutHelpOpen: (isShortcutHelpOpen) => set({ isShortcutHelpOpen }),
  toggleShortcutHelp: () =>
    set((state) => ({ isShortcutHelpOpen: !state.isShortcutHelpOpen })),
}));
