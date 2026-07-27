import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { SuggestedPrompt } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface PromptCardProps {
  prompt: SuggestedPrompt;
  onClick: (promptText: string) => void;
}

export const PromptCard: React.FC<PromptCardProps> = ({ prompt, onClick }) => {
  return (
    <Card
      onClick={() => onClick(prompt.promptText)}
      className="group cursor-pointer transition-all duration-200 hover:border-primary/50 hover:shadow-md bg-card/80 backdrop-blur-xs"
    >
      <CardContent className="p-4 space-y-2">
        <div className="flex items-center justify-between">
          <Badge variant="outline" className="text-[10px]">
            {prompt.category}
          </Badge>
          <ArrowUpRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
        <h4 className="text-sm font-semibold group-hover:text-primary transition-colors">
          {prompt.title}
        </h4>
        <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
          {prompt.description}
        </p>
      </CardContent>
    </Card>
  );
};
