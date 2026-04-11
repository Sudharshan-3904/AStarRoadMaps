import React from 'react'
import { CheckCircle2, Circle, Loader2, XCircle } from 'lucide-react'
import { useRoadmapStore } from '../../store/useRoadmapStore'
import { AgentName } from '../../types/roadmap'

const agentsOrder: { id: AgentName; label: string; description: string }[] = [
  { id: 'analyst', label: 'Analyst Agent', description: 'Personalizing your learning path...' },
  { id: 'curriculum', label: 'Curriculum Agent', description: 'Designing study modules...' },
  { id: 'resources', label: 'Resource Agent', description: 'Finding the best tutorials...' },
  { id: 'formatter', label: 'Formatter Agent', description: 'Preparing your interactive view...' }
]

export const AgentProgress: React.FC = () => {
  const agentStatuses = useRoadmapStore((state) => state.agentStatuses)

  return (
    <div className="max-w-md mx-auto py-12">
      <div className="space-y-8">
        {agentsOrder.map((agent, index) => {
          const status = agentStatuses[agent.id]
          const isActive = status === 'running'
          const isDone = status === 'done'
          const isError = status === 'error'

          return (
            <div key={agent.id} className="relative flex items-start group">
              {/* Connector Line */}
              {index < agentsOrder.length - 1 && (
                <div 
                  className={`absolute left-4 top-10 w-0.5 h-12 transition-colors duration-500 ${
                    isDone ? 'bg-teal-500' : 'bg-slate-700'
                  }`}
                />
              )}

              {/* Icon */}
              <div className="relative z-10 flex items-center justify-center">
                {isDone ? (
                  <div className="bg-teal-500 rounded-full p-1 animate-in fade-in zoom-in duration-500">
                    <CheckCircle2 className="w-6 h-6 text-slate-900" />
                  </div>
                ) : isActive ? (
                  <div className="relative">
                    <div className="absolute inset-0 bg-teal-500 rounded-full animate-pulse opacity-20 scale-150" />
                    <Loader2 className="w-8 h-8 text-teal-500 animate-spin" />
                  </div>
                ) : isError ? (
                  <XCircle className="w-8 h-8 text-red-500" />
                ) : (
                  <Circle className="w-8 h-8 text-slate-700" />
                )}
              </div>

              {/* Text */}
              <div className="ml-6">
                <h3 className={`font-semibold text-lg transition-colors ${
                  isActive ? 'text-teal-400 font-sora' : isDone ? 'text-slate-200' : 'text-slate-500'
                }`}>
                  {agent.label}
                </h3>
                <p className={`text-sm transition-colors ${
                  isActive ? 'text-slate-300' : 'text-slate-600'
                }`}>
                  {status === 'pending' ? 'Waiting...' : agent.description}
                </p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
