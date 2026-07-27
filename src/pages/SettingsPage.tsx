import React from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { SectionTitle } from '@/components/common/SectionTitle';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useTheme } from '@/hooks/useTheme';
import { Sun, Moon, Monitor, Cpu, Database, ShieldCheck } from 'lucide-react';
import { Theme } from '@/types';

export const SettingsPage: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const themes: { id: Theme; label: string; icon: React.ReactNode }[] = [
    { id: 'light', label: 'Light', icon: <Sun className="h-4 w-4 text-amber-500" /> },
    { id: 'dark', label: 'Dark', icon: <Moon className="h-4 w-4 text-indigo-400" /> },
    { id: 'system', label: 'System', icon: <Monitor className="h-4 w-4 text-muted-foreground" /> },
  ];

  return (
    <PageContainer maxWidth="md" className="overflow-y-auto">
      <SectionTitle
        title="Settings & Preferences"
        subtitle="Manage appearance, system parameters, and application configuration"
      />

      <div className="space-y-6">
        {/* Appearance Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Appearance & Theme</CardTitle>
            <CardDescription>Select your preferred visual mode for the interface.</CardDescription>
          </CardHeader>
          <CardContent className="flex items-center gap-3">
            {themes.map((t) => (
              <Button
                key={t.id}
                variant={theme === t.id ? 'default' : 'outline'}
                onClick={() => setTheme(t.id)}
                className="flex-1 gap-2 rounded-xl"
              >
                {t.icon}
                <span>{t.label}</span>
              </Button>
            ))}
          </CardContent>
        </Card>

        {/* AI Model & System Settings Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">AI Engine & Vector Config (Phase 2 Preview)</CardTitle>
            <CardDescription>Target RAG framework parameters configured for future phases.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center gap-2 text-sm font-medium">
                <Cpu className="h-4 w-4 text-primary" />
                <span>Primary LLM Provider</span>
              </div>
              <Badge variant="outline">Gemini 3.5 Flash Lite</Badge>
            </div>

            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center gap-2 text-sm font-medium">
                <Database className="h-4 w-4 text-primary" />
                <span>Vector Database Engine</span>
              </div>
              <Badge variant="outline">Qdrant Local / Cloud</Badge>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm font-medium">
                <ShieldCheck className="h-4 w-4 text-emerald-500" />
                <span>Fact Grounding Guardrails</span>
              </div>
              <Badge variant="success">Strict Context Only</Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </PageContainer>
  );
};
