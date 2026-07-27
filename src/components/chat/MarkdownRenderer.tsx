import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CodeBlockProps extends React.HTMLAttributes<HTMLElement> {
  className?: string;
  children?: React.ReactNode;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ className, children, ...props }) => {
  const match = /language-(\w+)/.exec(className || '');
  const codeText = String(children).replace(/\n$/, '');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(codeText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (match) {
    return (
      <div className="my-3 overflow-hidden rounded-xl border border-border bg-card shadow-xs">
        <div className="flex items-center justify-between bg-muted/60 px-4 py-1.5 text-xs text-muted-foreground font-mono">
          <span>{match[1]}</span>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="h-7 px-2 text-xs gap-1.5 hover:bg-muted"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-500" />
                <span className="text-emerald-500">Copied</span>
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" />
                <span>Copy code</span>
              </>
            )}
          </Button>
        </div>
        <pre className="overflow-x-auto p-4 font-mono text-xs text-foreground bg-muted/20">
          <code className={className} {...props}>
            {children}
          </code>
        </pre>
      </div>
    );
  }

  return (
    <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono font-medium" {...props}>
      {children}
    </code>
  );
};

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="markdown-content text-sm leading-relaxed">
      <ReactMarkdown
        components={{
          code: CodeBlock,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
