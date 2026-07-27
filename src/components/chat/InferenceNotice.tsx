import React from 'react';
import { Sparkles } from 'lucide-react';

export const InferenceNotice: React.FC = () => {
  return (
    <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-sky-500/10 text-sky-700 dark:text-sky-300 border border-sky-500/20 text-xs font-medium mb-2">
      <Sparkles className="h-3.5 w-3.5 shrink-0 text-sky-500" />
      <span>Inference — Based on documented principles, not a direct historical statement</span>
    </div>
  );
};
