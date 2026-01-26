import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { ChevronDown, ChevronUp, Sparkles, Brain, CheckCircle2, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

// Types for Autonomous Agent Response
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

interface AutonomousAgentCardProps {
  response: AutonomousAgentResponse;
}

const AutonomousAgentCard: React.FC<AutonomousAgentCardProps> = ({ response }) => {
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);

  const toggleStep = (index: number) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSteps(newExpanded);
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'analyze_image':
      case 'analyze_text':
        return <Sparkles className="w-4 h-4" />;
      case 'decision_engine':
        return <Brain className="w-4 h-4" />;
      case 'complete':
        return <CheckCircle2 className="w-4 h-4" />;
      default:
        return <Loader2 className="w-4 h-4 animate-spin" />;
    }
  };

  const getConfidenceColor = (level: string) => {
    switch (level) {
      case 'high':
        return 'text-green-400';
      case 'medium':
        return 'text-yellow-400';
      case 'low':
        return 'text-red-400';
      default:
        return 'text-muted-foreground';
    }
  };

  return (
    <div className="space-y-4 w-full">
      {/* Executive Summary - Hero Section */}
      <GlassCard variant="green" className="p-6 border-2 border-primary/30">
        <div className="flex items-start gap-3 mb-4">
          <div className="p-2 bg-primary/20 rounded-lg">
            <Sparkles className="w-6 h-6 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="font-display text-xl font-bold text-primary mb-1">
              Autonomous Analysis Complete
            </h3>
            <p className="text-sm text-muted-foreground">
              {response.total_steps} steps executed autonomously
            </p>
          </div>
          <div className={cn("text-sm font-bold uppercase", getConfidenceColor(response.synthesis.confidence_level))}>
            {response.synthesis.confidence_level} confidence
          </div>
        </div>

        <p className="font-body text-base leading-relaxed text-foreground mb-4">
          {response.synthesis.executive_summary}
        </p>

        {/* Key Takeaways */}
        <div className="space-y-2">
          <h4 className="text-sm font-bold uppercase text-muted-foreground">Key Takeaways</h4>
          <div className="space-y-2">
            {response.synthesis.key_takeaways.map((takeaway, i) => (
              <div key={i} className="flex items-start gap-2 text-base">
                <CheckCircle2 className="w-5 h-5 text-primary mt-0.5 shrink-0" />
                <span className="text-foreground">{takeaway}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Next Steps */}
        {response.synthesis.next_steps && response.synthesis.next_steps.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border/50">
            <h4 className="text-sm font-bold uppercase text-muted-foreground mb-2">Recommended Actions</h4>
            <div className="space-y-1">
              {response.synthesis.next_steps.map((step, i) => (
                <div key={i} className="text-base text-muted-foreground">
                  {i + 1}. {step}
                </div>
              ))}
            </div>
          </div>
        )}
      </GlassCard>

      {/* Initial Analysis */}
      <GlassCard className="p-4">
        <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-primary" />
          Initial Analysis
        </h4>
        <p className="text-base font-semibold text-foreground mb-2">
          {response.initial_analysis.insight}
        </p>
        <p className="text-sm text-muted-foreground">
          {response.initial_analysis.detailed_reasoning}
        </p>

        {/* Key Takeaways (if available) */}
        {response.initial_analysis.key_takeaways && response.initial_analysis.key_takeaways.length > 0 && (
          <div className="mt-3 space-y-1">
            <div className="text-xs font-bold uppercase text-muted-foreground mb-1">Quick Takeaways</div>
            {response.initial_analysis.key_takeaways.map((takeaway, i) => (
              <div key={i} className="text-xs text-foreground flex items-start gap-1">
                <span>{takeaway}</span>
              </div>
            ))}
          </div>
        )}

        {/* Trade-offs in compact format */}
        {(response.initial_analysis.trade_offs.pros.length > 0 ||
          response.initial_analysis.trade_offs.cons.length > 0) && (
            <div className="mt-3 grid grid-cols-2 gap-2">
              {response.initial_analysis.trade_offs.pros.length > 0 && (
                <div className="border border-green-500/30 bg-green-500/5 p-2 rounded">
                  <div className="text-xs font-bold text-green-400 mb-1">Benefits</div>
                  <ul className="space-y-0.5">
                    {response.initial_analysis.trade_offs.pros.slice(0, 2).map((pro, i) => (
                      <li key={i} className="text-xs text-muted-foreground">• {pro}</li>
                    ))}
                  </ul>
                </div>
              )}
              {response.initial_analysis.trade_offs.cons.length > 0 && (
                <div className="border border-red-500/30 bg-red-500/5 p-2 rounded">
                  <div className="text-xs font-bold text-red-400 mb-1">Trade-offs</div>
                  <ul className="space-y-0.5">
                    {response.initial_analysis.trade_offs.cons.slice(0, 2).map((con, i) => (
                      <li key={i} className="text-xs text-muted-foreground">• {con}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
      </GlassCard>

      {/* Workflow Steps - Collapsible */}
      <div className="space-y-2">
        <button
          onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
          className="w-full flex items-center justify-between p-3 border border-border bg-muted/20 hover:bg-muted/40 transition-colors"
        >
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold">Agent Workflow ({response.workflow_steps.length} steps)</span>
          </div>
          {showTechnicalDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showTechnicalDetails && (
          <div className="space-y-2 pl-4 border-l-2 border-primary/30">
            {response.workflow_steps.map((step, index) => (
              <div key={index} className="border border-border bg-background/50">
                <button
                  onClick={() => toggleStep(index)}
                  className="w-full flex items-center justify-between p-3 hover:bg-muted/20 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="text-primary">{getActionIcon(step.action)}</div>
                    <div className="text-left">
                      <div className="text-sm font-semibold">Step {index + 1}: {step.description}</div>
                      <div className="text-xs text-muted-foreground">{step.action}</div>
                    </div>
                  </div>
                  {expandedSteps.has(index) ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>

                {expandedSteps.has(index) && (
                  <div className="p-4 border-t border-border bg-muted/10 space-y-3">
                    {step.reasoning && (
                      <div>
                        <div className="text-xs font-bold uppercase text-muted-foreground mb-1">Reasoning</div>
                        <p className="text-xs text-foreground">{step.reasoning}</p>
                      </div>
                    )}

                    {step.result && (
                      <div>
                        <div className="text-xs font-bold uppercase text-muted-foreground mb-1">Result</div>
                        {step.action === 'decision_engine' && step.result.quick_insight ? (
                          <div className="space-y-2">
                            <p className="text-sm font-semibold text-primary">{step.result.quick_insight.summary}</p>
                            {step.result.key_signals && step.result.key_signals.length > 0 && (
                              <div>
                                <div className="text-xs font-bold text-muted-foreground mb-1">Key Signals:</div>
                                <div className="flex flex-wrap gap-1">
                                  {step.result.key_signals.map((signal: string, i: number) => (
                                    <span key={i} className="text-xs px-2 py-1 bg-primary/10 border border-primary/30 rounded">
                                      {signal}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        ) : step.action === 'generate_recommendations' && step.result.recommendations ? (
                          <div className="space-y-2">
                            {step.result.recommendations.map((rec: any, i: number) => (
                              <div key={i} className="border border-border p-2 rounded">
                                <div className="text-xs font-semibold">{rec.title}</div>
                                <div className="text-xs text-muted-foreground">{rec.description}</div>
                                <div className={cn(
                                  "text-xs font-bold mt-1",
                                  rec.priority === 'high' ? 'text-red-400' :
                                    rec.priority === 'medium' ? 'text-yellow-400' : 'text-green-400'
                                )}>
                                  Priority: {rec.priority}
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <pre className="text-xs bg-background/50 p-2 rounded overflow-x-auto">
                            {JSON.stringify(step.result, null, 2)}
                          </pre>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Uncertainty Note */}
      {response.initial_analysis.uncertainty_note && (
        <div className="border border-yellow-500/30 bg-yellow-500/5 p-3 rounded">
          <p className="text-xs italic text-yellow-200/80">
            ⚠️ {response.initial_analysis.uncertainty_note}
          </p>
        </div>
      )}
    </div>
  );
};

export default AutonomousAgentCard;
