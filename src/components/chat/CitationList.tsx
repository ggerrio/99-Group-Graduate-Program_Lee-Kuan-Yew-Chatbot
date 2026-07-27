import React from 'react';
import { BookOpen, FileText, Calendar, Hash } from 'lucide-react';
import { CitationItem } from '@/types';

interface CitationListProps {
  citations: CitationItem[];
}

export const CitationList: React.FC<CitationListProps> = ({ citations }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className="mt-3 pt-3 border-t border-border/60 space-y-2">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
        <BookOpen className="h-3.5 w-3.5 text-primary/80" />
        <span>Source Citations ({citations.length})</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {citations.map((cite, index) => (
          <div
            key={`${cite.document_title}-${cite.page_number}-${index}`}
            className="flex flex-col p-2.5 rounded-xl bg-muted/40 border border-border/50 text-xs transition-colors hover:bg-muted/70"
          >
            <div className="font-medium text-foreground line-clamp-1" title={cite.document_title}>
              {cite.document_title}
            </div>

            <div className="flex flex-wrap items-center gap-2 mt-1.5 text-[11px] text-muted-foreground">
              <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md bg-secondary text-secondary-foreground font-medium capitalize">
                <FileText className="h-3 w-3" />
                {cite.document_type}
              </span>

              {cite.year && (
                <span className="inline-flex items-center gap-1">
                  <Calendar className="h-3 w-3 opacity-70" />
                  {cite.year}
                </span>
              )}

              <span className="inline-flex items-center gap-0.5 ml-auto text-muted-foreground/80 font-mono">
                <Hash className="h-3 w-3 opacity-70" />
                p. {cite.page_number}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
