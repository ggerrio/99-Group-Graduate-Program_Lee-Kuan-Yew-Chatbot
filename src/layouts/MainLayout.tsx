import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageSquare,
  Plus,
  Settings,
  Info,
  Sparkles,
  ChevronLeft,
  Search,
  BookOpen,
  Menu,
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { useChatStore } from '@/store/useChatStore';
import { useMobile } from '@/hooks/useMobile';
import { Button } from '@/components/ui/button';
import { SidebarItem } from '@/components/common/SidebarItem';

export const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isMobile = useMobile();
  const { sidebarOpen, toggleSidebar, setSidebarOpen } = useAppStore();
  const { conversations, activeConversationId, selectConversation, createNewChat } =
    useChatStore();

  const handleSelectConv = (id: string) => {
    selectConversation(id);
    navigate('/');
    if (isMobile) {
      setSidebarOpen(false);
    }
  };

  const handleNewChat = () => {
    createNewChat();
    navigate('/');
    if (isMobile) {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground">
      {/* Mobile Drawer Overlay Backdrop */}
      <AnimatePresence>
        {isMobile && sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-xs"
          />
        )}
      </AnimatePresence>

      {/* Responsive Sidebar (Desktop Fixed / Mobile Drawer) */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex flex-col bg-card transition-all duration-300 md:static overflow-hidden ${
          sidebarOpen ? 'w-72 translate-x-0 border-r' : '-translate-x-full md:w-0 md:translate-x-0'
        }`}
      >
        {/* Sidebar Header */}
        <div className="flex h-16 items-center justify-between border-b px-4 shrink-0">
          <div
            onClick={() => navigate('/')}
            className="flex items-center gap-2.5 font-bold text-base cursor-pointer select-none"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-xs">
              <Sparkles className="h-4 w-4" />
            </div>
            <div className="flex flex-col">
              <span className="leading-none">LKY AI</span>
              <span className="text-[10px] font-normal text-muted-foreground mt-0.5">
                Chatbot Foundation
              </span>
            </div>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="h-8 w-8 text-muted-foreground"
            title="Collapse Sidebar"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
        </div>

        {/* New Chat Trigger */}
        <div className="p-3 shrink-0">
          <Button
            onClick={handleNewChat}
            className="w-full justify-start gap-2.5 rounded-xl bg-primary text-primary-foreground shadow-xs hover:bg-primary/90"
          >
            <Plus className="h-4.5 w-4.5" />
            <span className="font-semibold text-sm">New Conversation</span>
          </Button>
        </div>

        {/* Recent Conversations List */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-4">
          <div>
            <div className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground flex items-center justify-between">
              <span>Recent Conversations</span>
              <Search className="h-3 w-3 text-muted-foreground/60" />
            </div>
            <div className="space-y-1 mt-1">
              {conversations.map((conv) => (
                <SidebarItem
                  key={conv.id}
                  icon={<MessageSquare className="h-4 w-4" />}
                  label={conv.title}
                  active={location.pathname === '/' && activeConversationId === conv.id}
                  onClick={() => handleSelectConv(conv.id)}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Navigation & Footer Links */}
        <div className="border-t p-3 space-y-1 shrink-0 bg-muted/20">
          <SidebarItem
            icon={<BookOpen className="h-4 w-4" />}
            label="Chat Interface"
            active={location.pathname === '/'}
            onClick={() => {
              navigate('/');
              if (isMobile) setSidebarOpen(false);
            }}
          />
          <SidebarItem
            icon={<Settings className="h-4 w-4" />}
            label="Settings"
            active={location.pathname === '/settings'}
            onClick={() => {
              navigate('/settings');
              if (isMobile) setSidebarOpen(false);
            }}
          />
          <SidebarItem
            icon={<Info className="h-4 w-4" />}
            label="About"
            active={location.pathname === '/about'}
            onClick={() => {
              navigate('/about');
              if (isMobile) setSidebarOpen(false);
            }}
          />
          <div className="pt-2 pb-1 text-center text-[11px] font-medium text-muted-foreground/70 border-t border-border/40 mt-1">
            Built by <span className="font-semibold text-foreground/80">Gerrio Pratama</span>
          </div>
        </div>
      </aside>

      {/* Main Viewport Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden relative">
        {!sidebarOpen && location.pathname !== '/' && (
          <Button
            variant="outline"
            size="icon"
            onClick={toggleSidebar}
            className="absolute top-4 left-4 z-40 h-9 w-9 rounded-xl shadow-xs bg-card border hover:bg-muted shrink-0 hidden md:flex items-center justify-center"
            title="Expand Sidebar"
          >
            <Menu className="h-4 w-4" />
          </Button>
        )}
        <Outlet />
      </div>
    </div>
  );
};
