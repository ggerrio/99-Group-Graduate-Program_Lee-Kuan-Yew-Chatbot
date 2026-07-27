import React from 'react';
import { Sparkles, Shield, Landmark, Globe } from 'lucide-react';
import { SuggestedPrompt } from '@/types';
import { PromptCard } from './PromptCard';

const SAMPLE_PROMPTS: SuggestedPrompt[] = [
  {
    id: 'p-1',
    category: 'Leadership',
    title: 'Principles of Effective Governance',
    description: 'What key leadership principles were critical during Singapore’s foundational years?',
    promptText: 'What key leadership principles guided your administration in building Singapore into a global financial center?',
  },
  {
    id: 'p-2',
    category: 'Economics',
    title: 'Economic Transformation Strategy',
    description: 'How did Singapore transition from a third-world port to a first-world economy?',
    promptText: 'Explain the economic strategy Singapore used to attract foreign investment and build world-class infrastructure.',
  },
  {
    id: 'p-3',
    category: 'Diplomacy',
    title: 'Small State Geopolitics',
    description: 'How should a small nation navigate rivalry between major global superpowers?',
    promptText: 'How can a small state maintain sovereignty and economic relevance amidst geopolitical competition?',
  },
  {
    id: 'p-4',
    category: 'Philosophy',
    title: 'Pragmatism & Meritocracy',
    description: 'Why is meritocracy essential for anti-corruption and institutional excellence?',
    promptText: 'Why did you consider meritocracy and pragmatism non-negotiable for public service?',
  },
];

interface EmptyStateProps {
  onSelectPrompt: (promptText: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectPrompt }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center max-w-3xl mx-auto space-y-8 animate-in fade-in-0 duration-300">
      <div className="space-y-3">
        <div className="mx-auto inline-flex items-center justify-center p-3.5 bg-primary/10 rounded-2xl text-primary">
          <Sparkles className="h-8 w-8" />
        </div>
        <h2 className="text-2xl md:text-3xl font-bold tracking-tight">
          Lee Kuan Yew AI Persona
        </h2>
        <p className="text-sm md:text-base text-muted-foreground max-w-xl mx-auto leading-relaxed">
          Ask questions regarding governance, economic strategy, diplomacy, and nation-building based on Lee Kuan Yew’s memoirs and public speeches.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full text-left">
        {SAMPLE_PROMPTS.map((prompt) => (
          <PromptCard key={prompt.id} prompt={prompt} onClick={onSelectPrompt} />
        ))}
      </div>

      <div className="flex items-center gap-6 text-xs text-muted-foreground border-t pt-6 w-full justify-center">
        <div className="flex items-center gap-1.5">
          <Shield className="h-4 w-4 text-primary" />
          <span>Factually Grounded</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Landmark className="h-4 w-4 text-primary" />
          <span>Historical Speeches</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Globe className="h-4 w-4 text-primary" />
          <span>Global Geopolitics</span>
        </div>
      </div>
    </div>
  );
};
