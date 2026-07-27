import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { PageContainer } from '@/components/common/PageContainer';
import { AlertTriangle, ArrowLeft } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <PageContainer maxWidth="sm" className="flex flex-col items-center justify-center text-center">
      <div className="p-4 bg-amber-500/10 rounded-full mb-4">
        <AlertTriangle className="h-10 w-10 text-amber-500" />
      </div>
      <h1 className="text-3xl font-bold tracking-tight mb-2">404 - Page Not Found</h1>
      <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
        The route you accessed does not exist in the Lee Kuan Yew Chatbot application.
      </p>
      <Button asChild variant="default" className="gap-2 rounded-xl">
        <Link to="/">
          <ArrowLeft className="h-4 w-4" />
          <span>Return to Chat Interface</span>
        </Link>
      </Button>
    </PageContainer>
  );
};
