import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const RefusalNotice: React.FC = () => {
  return (
    <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 text-xs font-medium mb-2">
      <ShieldAlert className="h-3.5 w-3.5 shrink-0" />
      <span>No Documented Historical Record</span>
    </div>
  );
};
