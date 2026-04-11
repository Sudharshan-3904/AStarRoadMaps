import React, { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { PageShell } from '../components/layout/PageShell'
import { AgentProgress } from '../components/generator/AgentProgress'
import { useRoadmapStream } from '../hooks/useRoadmapStream'
import { useRoadmapStore } from '../store/useRoadmapStore'
import { AlertCircle } from 'lucide-react'

export const Generate: React.FC = () => {
  const { roadmapId } = useParams<{ roadmapId: string }>()
  const navigate = useNavigate()
  const { error } = useRoadmapStream(roadmapId || null)
  const agentStatuses = useRoadmapStore((state) => state.agentStatuses)

  // Navigate when formatter is done
  useEffect(() => {
    if (agentStatuses.formatter === 'done') {
      const timer = setTimeout(() => {
        navigate(`/roadmap/${roadmapId}`)
      }, 1500) // Small delay to show completion checkmark
      return () => clearTimeout(timer)
    }
  }, [agentStatuses.formatter, navigate, roadmapId])

  return (
    <PageShell>
      <div className="max-w-xl mx-auto pt-24">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold font-sora text-slate-100 mb-4 tracking-tight">
            Assembling Your Roadmap
          </h1>
          <p className="text-slate-400">
            Our specialized AI agents are collaborating to build your personalized learning journey.
          </p>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 mb-8 flex items-center gap-3 text-red-400">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
          <AgentProgress />
        </div>
      </div>
    </PageShell>
  )
}
