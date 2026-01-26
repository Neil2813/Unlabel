import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Header } from '@/components/layout/Header';
import { AIInput } from '@/components/ui/AIInput';
import { FoodScanner } from '@/components/ui/FoodScanner';
import { GlassCard } from '@/components/ui/GlassCard';
import { DecisionCard } from '@/components/ui/DecisionCard';
import AutonomousAgentCard from '@/components/ui/AutonomousAgentCard';
import { cn } from '@/lib/utils';
import api from '@/lib/api';

// Types
interface TradeOffs {
  pros: string[];
  cons: string[];
}

interface AnalysisResult {
  insight: string;
  detailed_reasoning: string;
  trade_offs: TradeOffs;
  uncertainty_note?: string;
}

// New Decision Engine Types - Matching Backend Schemas
interface IngredientTranslation {
  term: string;
  simple_explanation: string;
  category: string;
}

interface QuickInsight {
  summary: string;
  uncertainty_reason?: string | null;
}

interface ConsumerExplanation {
  why_this_matters: string[]; // Max 3 bullet points
  when_it_makes_sense: string;
  what_to_know: string;
}

// Structured Analysis Types (for technical details)
interface IngredientSummary {
  primary_components: string[];
  added_sugars_present: boolean;
  sweetener_type: "none" | "natural" | "added" | "mixed";
  fiber_level: "none" | "low" | "moderate" | "high";
  protein_level: "none" | "low" | "moderate" | "high";
  fat_level: "none" | "low" | "moderate" | "high";
  processing_level: "low" | "moderate" | "high";
  ultra_processed_markers: string[];
  ingredient_count: number;
}

interface FoodProperties {
  sugar_dominant: boolean;
  fiber_protein_support: "none" | "weak" | "moderate" | "strong";
  energy_release_pattern: "rapid" | "mixed" | "slow";
  satiety_support: "low" | "moderate" | "high";
  formulation_complexity: "simple" | "moderate" | "complex";
}

interface ConfidenceNotes {
  data_completeness: "high" | "medium" | "low";
  ambiguity_flags: string[];
}

interface StructuredIngredientAnalysis {
  ingredient_summary: IngredientSummary;
  food_properties: FoodProperties;
  confidence_notes: ConfidenceNotes;
}

interface DecisionRequest {
  text: string;
  user_intent?: "quick_yes_no" | "comparison" | "risk_check" | "curiosity" | null;
  include_nutrition?: string | null;
  conversation_context?: string | null;
}

interface DecisionEngineResponse {
  // Instant understanding (show first)
  quick_insight: QuickInsight;

  // Consumer-facing (primary)
  explanation: ConsumerExplanation;

  // Supporting information
  intent_classified: "quick_yes_no" | "comparison" | "risk_check" | "curiosity" | string;
  key_signals: string[]; // Top signals that influenced the decision

  // Ingredient translation (explain complex terms)
  ingredient_translations: IngredientTranslation[];

  // Uncertainty flags
  uncertainty_flags: string[];

  // Technical details (optional, for transparency/debugging)
  structured_analysis?: StructuredIngredientAnalysis | null;
}

// Autonomous Agent Types
interface AgentStep {
  action: string;
  description: string;
  result: any;
  reasoning: string;
}

interface Synthesis {
  executive_summary: string;
  key_takeaways: string[];
  confidence_level: 'high' | 'medium' | 'low';
  next_steps: string[];
}

interface InitialAnalysis {
  insight: string;
  detailed_reasoning: string;
  trade_offs: {
    pros: string[];
    cons: string[];
  };
  key_takeaways?: string[];  // New field from backend
  uncertainty_note?: string;
  extracted_text?: string;
}

interface AutonomousAgentResponse {
  initial_analysis: InitialAnalysis;
  workflow_steps: AgentStep[];
  synthesis: Synthesis;
  total_steps: number;
}

interface Message {
  id: string;
  role: 'user' | 'ai';
  type: 'text' | 'image' | 'analysis' | 'decision' | 'autonomous';
  content?: string;
  imagePreview?: string;
  analysis?: AnalysisResult; // Legacy format
  decision?: DecisionEngineResponse; // New decision engine format
  autonomousResponse?: AutonomousAgentResponse; // Autonomous agent format
  timestamp: Date;
}

const Copilot = () => {

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'ai',
      type: 'text',
      content:
        "I'm your Unlabel Co-pilot. Show me a label or ask about ingredients, and I'll help you understand the trade-offs.",
      timestamp: new Date(),
    },
  ]);

  const [isTyping, setIsTyping] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState<{
    step: number;
    total: number;
    message: string;
    status: string;
  } | null>(null);
  const [showScanner, setShowScanner] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const addMessage = (msg: Message) => {
    setMessages((prev) => [...prev, msg]);
  };

  const handleTextSubmit = async (text: string) => {
    addMessage({
      id: Date.now().toString(),
      role: 'user',
      type: 'text',
      content: text,
      timestamp: new Date(),
    });

    setIsTyping(true);
    setLoadingProgress({ step: 1, total: 3, message: 'Starting analysis...', status: 'in_progress' });

    try {
      // Build conversation context from previous messages (last 3 messages for context)
      const recentMessages = messages
        .filter(msg => msg.role === 'user' || msg.role === 'ai')
        .slice(-3)
        .map(msg => {
          if (msg.role === 'user') {
            return `User: ${msg.content || 'Analyzed an image'}`;
          } else if (msg.autonomousResponse) {
            return `AI: ${msg.autonomousResponse.synthesis.executive_summary || 'Product analysis'}`;
          } else if (msg.decision) {
            return `AI: Analyzed product - ${msg.decision.quick_insight?.summary || 'Product analysis'}`;
          } else {
            return `AI: ${msg.content || ''}`;
          }
        })
        .join('\n');

      // Use STREAMING endpoint for real-time progressive results
      const endpoint = '/analyze/autonomous/text/stream';
      const contextParam = recentMessages ? `?user_query=${encodeURIComponent(recentMessages)}` : '';
      const textParam = `${contextParam ? '&' : '?'}text=${encodeURIComponent(text)}`;

      const url = `${api.defaults.baseURL}${endpoint}${contextParam}${textParam}`;

      console.log('Calling STREAMING AUTONOMOUS AGENT endpoint:', endpoint);
      console.log('Stream URL:', url);

      // Temporary storage for progressive results
      let partialResult: Partial<AutonomousAgentResponse> = {
        initial_analysis: undefined,
        workflow_steps: [],
        synthesis: undefined,
        total_steps: 0
      };

      // Create EventSource for streaming
      const eventSource = new EventSource(url);

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          console.log('Stream event received:', data.event, data);

          switch (data.event) {
            case 'step_start':
              setLoadingProgress({
                step: data.step,
                total: 3,
                message: data.message,
                status: 'in_progress'
              });
              console.log(`Starting step ${data.step}: ${data.name}`);
              break;

            case 'step_complete':
              console.log(`Completed step: ${data.name}`, data.result);

              // Store the completed step
              if (data.name === 'initial_analysis') {
                partialResult.initial_analysis = data.result;
              } else if (data.name === 'decision_engine') {
                partialResult.workflow_steps!.push({
                  action: 'decision_engine',
                  description: 'Deep analysis with multi-agent decision engine',
                  result: data.result,
                  reasoning: 'Complete ingredient interpretation and intent classification'
                });
              } else if (data.name === 'synthesis') {
                partialResult.synthesis = data.result;
              }
              break;

            case 'complete':
              // Final result received
              eventSource.close();

              console.log('Stream complete! Final result:', data.result);

              const autonomousData: AutonomousAgentResponse = data.result;


              // Ensure required fields exist (with fallbacks)
              if (!autonomousData.initial_analysis) {
                autonomousData.initial_analysis = {
                  insight: 'Analysis complete.',
                  detailed_reasoning: 'Product analyzed.',
                  trade_offs: { pros: [], cons: [] }
                };
              }

              if (!autonomousData.workflow_steps) {
                autonomousData.workflow_steps = [];
              }

              if (!autonomousData.synthesis) {
                autonomousData.synthesis = {
                  executive_summary: 'Analysis completed.',
                  key_takeaways: [],
                  confidence_level: 'medium',
                  next_steps: []
                };
              }

              addMessage({
                id: (Date.now() + 1).toString(),
                role: 'ai',
                type: 'autonomous',
                autonomousResponse: autonomousData,
                timestamp: new Date(),
              });

              setIsTyping(false);
              setLoadingProgress(null);
              break;

            case 'error':
              eventSource.close();
              console.error('Stream error event:', data.error);

              addMessage({
                id: (Date.now() + 1).toString(),
                role: 'ai',
                type: 'text',
                content: `Analysis error: ${data.error.error || 'Unknown error'}`,
                timestamp: new Date(),
              });

              setIsTyping(false);
              setLoadingProgress(null);
              break;

            default:
              console.log('Unknown event type:', data.event);
          }
        } catch (parseError) {
          console.error('Error parsing stream event:', parseError);
        }
      };

      eventSource.onerror = (error) => {
        console.error('EventSource connection error:', error);
        eventSource.close();

        addMessage({
          id: (Date.now() + 1).toString(),
          role: 'ai',
          type: 'text',
          content: 'Connection error. Please try again.',
          timestamp: new Date(),
        });

        setIsTyping(false);
        setLoadingProgress(null);
      };

    } catch (error: any) {
      console.error('Streaming setup error:', error);

      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'ai',
        type: 'text',
        content: `I'm having trouble analyzing that right now. Error: ${error.message || 'Unknown error'}`,
        timestamp: new Date(),
      });

      setIsTyping(false);
      setLoadingProgress(null);
    }
  };

  const handleImageCapture = async (file: File, preview: string) => {
    setShowScanner(false);

    addMessage({
      id: Date.now().toString(),
      role: 'user',
      type: 'image',
      imagePreview: preview,
      content: 'Analyze this label',
      timestamp: new Date(),
    });

    setIsTyping(true);
    setLoadingProgress({ step: 1, total: 3, message: 'Starting analysis...', status: 'in_progress' });

    try {
      // Use new decision engine endpoint for images
      const formData = new FormData();
      formData.append('file', file);

      // CRITICAL: Use decision engine endpoint, NOT legacy /analyze/image
      // Build conversation context from previous messages (last 3 messages for context)
      const recentMessages = messages
        .filter(msg => msg.role === 'user' || msg.role === 'ai')
        .slice(-3)
        .map(msg => {
          if (msg.role === 'user') {
            return `User: ${msg.content || 'Analyzed an image'}`;
          } else if (msg.decision) {
            return `AI: Analyzed product - ${msg.decision.quick_insight?.summary || 'Product analysis'}`;
          } else {
            return `AI: ${msg.content || ''}`;
          }
        })
        .join('\n');

      const endpoint = '/analyze/autonomous/image';
      const fullUrl = `${api.defaults.baseURL}${endpoint}`;

      console.log('Calling AUTONOMOUS AGENT endpoint:', endpoint);
      console.log('Full URL:', fullUrl);
      console.log('If you see /api/analyze/image in logs, browser cache needs clearing!');

      // Explicitly prevent calling old endpoint
      if (endpoint.includes('/analyze/image') && !endpoint.includes('/autonomous') && !endpoint.includes('/decision')) {
        throw new Error('ERROR: Attempted to call legacy endpoint! This should never happen.');
      }

      // Add conversation context as query parameter for image uploads
      const contextParam = recentMessages ? `?user_query=${encodeURIComponent(recentMessages)}` : '';

      setLoadingProgress({ step: 2, total: 3, message: 'Uploading image...', status: 'in_progress' });

      const response = await api.post<AutonomousAgentResponse>(endpoint + contextParam, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setLoadingProgress({ step: 3, total: 3, message: 'Processing results...', status: 'in_progress' });

      console.log('Response received from:', response.config.url);
      console.log('Autonomous agent response:', response.data);

      // Ensure response data matches expected structure
      const autonomousData: AutonomousAgentResponse = response.data;

      // Log for debugging
      console.log('Autonomous agent response keys:', Object.keys(autonomousData));

      // Validate that we have the required fields
      if (!autonomousData) {
        console.error('No response data received');
        throw new Error('No response from autonomous agent');
      }

      // Ensure required fields exist (with fallbacks)
      if (!autonomousData.initial_analysis) {
        autonomousData.initial_analysis = {
          insight: 'Analysis complete.',
          detailed_reasoning: 'Product analyzed.',
          trade_offs: { pros: [], cons: [] }
        };
      }

      if (!autonomousData.workflow_steps) {
        autonomousData.workflow_steps = [];
      }

      if (!autonomousData.synthesis) {
        autonomousData.synthesis = {
          executive_summary: 'Analysis completed.',
          key_takeaways: [],
          confidence_level: 'medium',
          next_steps: []
        };
      }

      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'ai',
        type: 'autonomous',
        autonomousResponse: autonomousData,
        timestamp: new Date(),
      });
    } catch (error: any) {
      console.error('Autonomous agent error:', error);
      console.error('Error details:', error.response?.data || error.message);

      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'ai',
        type: 'text',
        content:
          `I'm having trouble analyzing that image. Error: ${error.message || 'Unknown error'}. Please check the console for details.`,
        timestamp: new Date(),
      });
    } finally {
      setIsTyping(false);
      setLoadingProgress(null);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background overflow-hidden">
      <Header />

      {/* Chat Area */}
      <div
        ref={scrollRef}
        className="flex-1 min-h-0 overflow-y-auto overflow-x-hidden pt-20 sm:pt-24 pb-24 sm:pb-28 px-2 sm:px-4 space-y-4 sm:space-y-6"
        style={{
          scrollBehavior: 'smooth',
          WebkitOverflowScrolling: 'touch' // Smooth scrolling on iOS
        }}
      >
        <div className="max-w-3xl mx-auto space-y-4 sm:space-y-8">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                'flex gap-4',
                msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              )}
            >
              {/* Avatar */}
              <div className="w-7 h-7 sm:w-8 sm:h-8 border border-border flex items-center justify-center shrink-0">
                {msg.role === 'ai' ? (
                  <img
                    src="/Logo.png"
                    alt="AI"
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-xs font-medium text-foreground">
                    U
                  </span>
                )}
              </div>

              {/* Content */}
              <div className={cn('max-w-[85%] sm:max-w-[85%]', (msg.type === 'analysis' || msg.type === 'decision') && 'w-full max-w-full')}>
                {msg.type === 'text' && (
                  <div
                    className={cn(
                      'p-3 sm:p-4 text-sm font-body leading-relaxed border break-words',
                      msg.role === 'user'
                        ? 'border-primary/30 bg-primary/5'
                        : 'border-border bg-muted/30'
                    )}
                  >
                    {msg.content}
                  </div>
                )}

                {msg.type === 'image' && msg.imagePreview && (
                  <div className="border border-border w-full sm:w-48 max-w-full">
                    <img src={msg.imagePreview} alt="Upload" className="w-full h-auto" />
                  </div>
                )}

                {/* New Decision Engine Response - AI-Native Design */}
                {msg.type === 'decision' && msg.decision ? (
                  <DecisionCard decision={msg.decision} />
                ) : msg.type === 'decision' && (
                  <div className="p-4 border border-border bg-muted/30 text-sm text-muted-foreground">
                    Decision data is loading...
                  </div>
                )}

                {/* Autonomous Agent Response - Multi-step Workflow */}
                {msg.type === 'autonomous' && msg.autonomousResponse ? (
                  <AutonomousAgentCard response={msg.autonomousResponse} />
                ) : msg.type === 'autonomous' && (
                  <div className="p-4 border border-border bg-muted/30 text-sm text-muted-foreground">
                    Autonomous analysis in progress...
                  </div>
                )}

                {/* Legacy Analysis Format (for backward compatibility) */}
                {msg.type === 'analysis' && msg.analysis && (
                  <GlassCard variant="green" className="p-6">
                    <h3 className="font-display text-xl mb-3">
                      {msg.analysis.insight}
                    </h3>
                    <p className="font-body text-sm text-muted-foreground mb-6">
                      {msg.analysis.detailed_reasoning}
                    </p>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="border border-border p-4">
                        <h4 className="text-xs font-bold uppercase mb-2">
                          Benefits
                        </h4>
                        <ul className="space-y-2">
                          {msg.analysis.trade_offs.pros.map((p, i) => (
                            <li key={i} className="text-xs text-muted-foreground">
                              • {p}
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="border border-border p-4">
                        <h4 className="text-xs font-bold uppercase mb-2">
                          Trade-offs
                        </h4>
                        <ul className="space-y-2">
                          {msg.analysis.trade_offs.cons.map((c, i) => (
                            <li key={i} className="text-xs text-muted-foreground">
                              • {c}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {msg.analysis.uncertainty_note && (
                      <div className="mt-4 pt-4 border-t border-border">
                        <p className="text-xs italic text-muted-foreground">
                          {msg.analysis.uncertainty_note}
                        </p>
                      </div>
                    )}
                  </GlassCard>
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-2 sm:gap-4">
              <div className="w-7 h-7 sm:w-8 sm:h-8 border border-border shrink-0" />
              <div className="border border-border px-3 sm:px-4 py-2 sm:py-3 min-w-[200px]">
                {loadingProgress ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-foreground font-medium">
                        {loadingProgress.message}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        Step {loadingProgress.step}/{loadingProgress.total}
                      </span>
                    </div>
                    {/* Progress bar */}
                    <div className="w-full bg-muted/30 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-primary h-full transition-all duration-500 ease-out"
                        style={{
                          width: `${(loadingProgress.step / loadingProgress.total) * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                ) : (
                  <span className="text-sm text-muted-foreground">Thinking…</span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="flex-shrink-0 w-full p-2 sm:p-4 bg-background z-20 border-t border-border/30">
        <AIInput
          onSubmit={handleTextSubmit}
          onCameraClick={() => setShowScanner(true)}
          placeholder="Ask about ingredients or show me a label..."
        />
      </div>

      {showScanner && (
        <FoodScanner
          onCapture={handleImageCapture}
          onClose={() => setShowScanner(false)}
        />
      )}
    </div>
  );
};

export default Copilot;
