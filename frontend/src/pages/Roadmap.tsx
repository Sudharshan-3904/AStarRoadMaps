import React, { useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { PageShell } from '../components/layout/PageShell'
import { RoadmapHeader } from '../components/roadmap/RoadmapHeader'
import { PhaseCard } from '../components/roadmap/PhaseCard'
import { ProgressBar } from '../components/roadmap/ProgressBar'
import { RefinePanel } from '../components/roadmap/RefinePanel'
import { AgentProgress } from '../components/generator/AgentProgress'
import { useRoadmap } from '../hooks/useRoadmap'
import { useProgress } from '../hooks/useProgress'
import { useRefine } from '../hooks/useRefine'
import { useRoadmapStream } from '../hooks/useRoadmapStream'
import { Spinner } from '../components/ui/Spinner'

export const Roadmap: React.FC = () => {
  const { roadmapId } = useParams<{ roadmapId: string }>()
  const location = useLocation()
  
  const { data: roadmap, isLoading: roadmapLoading } = useRoadmap(roadmapId || null)
  const { data: progress, updateProgress } = useProgress(roadmapId || null)
  const { mutate: refine, isPending: refinementSending, data: refinementData } = useRefine(roadmapId || null)

  // Feedback state for SSE stream if refining
  const [activeFeedback, setActiveFeedback] = useState<string | undefined>(undefined)
  const [activeFeedbackType, setActiveFeedbackType] = useState<string | undefined>(undefined)
  
  const { isStreaming } = useRoadmapStream(
    activeFeedback ? (roadmapId || null) : null,
    activeFeedback,
    activeFeedbackType
  )

  const handleRefine = (feedback: string) => {
    refine({ feedback }, {
      onSuccess: (data) => {
        setActiveFeedback(data.feedback)
        setActiveFeedbackType(data.feedback_type)
      }
    })
  }

  // Clear streaming state once done
  React.useEffect(() => {
    if (!isStreaming && activeFeedback) {
      setActiveFeedback(undefined)
      setActiveFeedbackType(undefined)
    }
  }, [isStreaming, activeFeedback])

  if (roadmapLoading || !roadmap) {
    return (
      <PageShell>
        <div className="h-[70vh] flex flex-col items-center justify-center space-y-4">
          <Spinner size="lg" />
          <p className="text-slate-500 font-medium">Loading your roadmap...</p>
        </div>
      </PageShell>
    )
  }

  // Calculate overall progress
  const totalTopics = roadmap.phases.flatMap(p => p.topics).length
  const doneTopics = progress ? Object.values(progress.topics).filter(s => s === 'done').length : 0
  const totalProgress = totalTopics > 0 ? (doneTopics / totalTopics) * 100 : 0

  return (
    <PageShell>
      {/* Refinement Overlay */}
      {isStreaming && (
        <div className="fixed inset-0 z-[60] bg-slate-950/90 backdrop-blur-xl flex items-center justify-center p-6 animate-in fade-in duration-300">
          <div className="w-full max-w-xl">
            <div className="text-center mb-12">
              <h2 className="text-2xl font-bold font-sora text-slate-100 mb-2">Refining Your Roadmap</h2>
              <p className="text-slate-400">Updating modules based on your feedback...</p>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
              <AgentProgress />
            </div>
          </div>
        </div>
      )}

      <RoadmapHeader roadmap={roadmap} />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-12">
        <div className="lg:col-span-3 space-y-8">
          <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6 lg:p-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold font-sora text-slate-100">Learning Path</h2>
              <div className="flex items-center gap-4 text-sm font-medium">
                <span className="text-slate-400">Overall Progress</span>
                <span className="text-teal-400 font-bold">{Math.round(totalProgress)}%</span>
              </div>
            </div>
            
            <div className="mb-12">
              <ProgressBar progress={totalProgress} size="md" />
            </div>

            <div className="space-y-6">
              {roadmap.phases.map((phase) => (
                <PhaseCard 
                  key={phase.phase_number} 
                  phase={phase} 
                  topicsProgress={progress?.topics || {}}
                  onTopicStatusChange={(name, status) => updateProgress({ topic_name: name, status })}
                />
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <div className="sticky top-24">
            <RefinePanel onSubmit={handleRefine} isLoading={refinementSending} />
            
            <div className="mt-8 p-6 bg-slate-900/30 border border-slate-800 rounded-2xl">
              <h4 className="text-sm font-bold text-slate-300 uppercase tracking-widest mb-4">Pro Tips</h4>
              <ul className="space-y-3 text-sm text-slate-500 leading-relaxed">
                <li className="flex gap-2">
                  <span className="text-teal-500 font-bold">•</span>
                  Focus on one topic at a time to maximize retention.
                </li>
                <li className="flex gap-2">
                  <span className="text-teal-500 font-bold">•</span>
                  Complete all sub-tasks before moving to the next topic.
                </li>
                <li className="flex gap-2">
                  <span className="text-teal-500 font-bold">•</span>
                  The hands-on project is key to mastering the concepts.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </PageShell>
  )
}
