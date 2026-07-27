import { useAppStore } from '@/store/useAppStore';

export function useSidebar() {
  const { sidebarOpen, toggleSidebar, setSidebarOpen } = useAppStore();
  return { sidebarOpen, toggleSidebar, setSidebarOpen };
}
