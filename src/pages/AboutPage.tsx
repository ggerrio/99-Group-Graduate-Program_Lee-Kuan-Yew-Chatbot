import React from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { SectionTitle } from '@/components/common/SectionTitle';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Award, FileText, Globe, Layers, User } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <PageContainer maxWidth="md" className="overflow-y-auto">
      <SectionTitle
        title="About Lee Kuan Yew AI Chatbot"
        subtitle="An interactive RAG application trained on official memoirs, speeches, and archival records."
      />

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Award className="h-5 w-5 text-primary" />
              <span>Project Vision</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground leading-relaxed space-y-3">
            <p>
              This application offers an AI-powered conversational experience preserving the governance philosophy, strategic economic decisions, and foreign policy perspectives of Singapore’s founding Prime Minister, <strong>Lee Kuan Yew</strong>.
            </p>
            <p>
              By combining high-density Retrieval-Augmented Generation (RAG) with Google Gemini, the chatbot delivers factually grounded answers anchored directly in historical literature.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              <span>Project Author & Submission</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground leading-relaxed space-y-2">
            <p>
              Developed by <strong>Gerrio Pratama</strong> for the <em>"What Would Lee Kuan Yew Do?"</em> challenge.
            </p>
            <p>
              Built with a production-ready RAG architecture combining FastAPI, custom vector retrieval over 5,772 ingested document chunks, and an evaluation metrics framework.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-primary" />
              <span>Knowledge Base Corpus</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-3 rounded-xl border bg-muted/30 flex items-center gap-3">
              <FileText className="h-5 w-5 text-primary shrink-0" />
              <div>
                <div className="font-semibold text-xs">Memoirs</div>
                <div className="text-[11px] text-muted-foreground">The Singapore Story & From Third World to First</div>
              </div>
            </div>

            <div className="p-3 rounded-xl border bg-muted/30 flex items-center gap-3">
              <Globe className="h-5 w-5 text-primary shrink-0" />
              <div>
                <div className="font-semibold text-xs">Speeches & Addresses</div>
                <div className="text-[11px] text-muted-foreground">Parliamentary debates and international summits</div>
              </div>
            </div>

            <div className="p-3 rounded-xl border bg-muted/30 flex items-center gap-3">
              <Layers className="h-5 w-5 text-primary shrink-0" />
              <div>
                <div className="font-semibold text-xs">Transcribed Interviews</div>
                <div className="text-[11px] text-muted-foreground">Global media & diplomatic conversations</div>
              </div>
            </div>

            <div className="p-3 rounded-xl border bg-muted/30 flex items-center gap-3">
              <FileText className="h-5 w-5 text-primary shrink-0" />
              <div>
                <div className="font-semibold text-xs">Published Essays</div>
                <div className="text-[11px] text-muted-foreground">Articles on governance & international affairs</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex items-center justify-between text-xs text-muted-foreground border-t pt-4">
          <span>Built by Gerrio Pratama</span>
          <Badge variant="outline">Version 1.0.0</Badge>
        </div>
      </div>
    </PageContainer>
  );
};
