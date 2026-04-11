import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Box, Clock, Target } from 'lucide-react'
import { Phase, TopicStatus } from '../../types/roadmap'
import { TopicCard } from './TopicCard'
import { ProgressBar } from './ProgressBar'

interface PhaseCardProps {
  phase: Phase
  topicsProgress: Record<string, TopicStatus>
  onTopicStatusChange: (topicName: string, status: TopicStatus) => void
}

export const PhaseCard: React.FC<PhaseCardProps> = ({ 
  phase, 
  topicsProgress, 
  onTopicStatusChange 
}) => {
  const [isExpanded, setIsExpanded] = useState(phase.phase_number === 1)
  
  const topics = phase.topics
  const doneCount = topics.filter(t => topicsProgress[t.name] === 'done').length
  const progressPercent = (doneCount / topics.length) * 100

  // Border colors by phase as per design guidelines
  const phaseColors = [
    'border-l-blue-500 shadow-blue-500/5', 
    'border-l-yellow-500 shadow-yellow-500/5', 
    'border-l-orange-500 shadow-orange-500/5', 
    'border-l-red-500 shadow-red-500/5'
  ]
  const borderColorIndex = (phase.phase_number - 1) % phaseColors.length
  const cardStyle = phaseColors[borderColorIndex]

  return (
    <div className={`bg-slate-900/40 border border-slate-800/60 border-l-4 ${cardStyle} rounded-2xl overflow-hidden transition-all duration-500 hover:border-slate-700/60 group`}>
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-6 md:p-8 cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-6 hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-start md:items-center gap-6 flex-1">
          <div className="bg-slate-950 border border-slate-700/50 w-14 h-14 rounded-2xl flex items-center justify-center text-xl font-bold text-slate-400 shrink-0 group-hover:scale-110 transition-transform">
            {phase.phase_number}
          </div>
          <div className="flex-1 space-y-3">
            <div className="flex flex-wrap items-center gap-3">
              <h3 className="text-2xl font-bold text-white font-sora">{phase.title}</h3>
              <div className="flex items-center gap-1.5 px-3 py-1 bg-slate-950/50 border border-slate-700/30 rounded-full text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                <Clock className="w-3 h-3" />
                {phase.week_range}
              </div>
            </div>
            <div className="max-w-md">
              <ProgressBar progress={progressPercent} size="sm" showLabel />
            </div>
          </div>
        </div>
        
        <div className="flex items-center justify-between md:justify-end gap-6 border-t border-slate-800/50 md:border-t-0 pt-4 md:pt-0">
          <div className="flex flex-col items-end">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Status</span>
            <span className="text-sm font-semibold text-slate-300">
              {doneCount < topics.length ? `In Progress (${doneCount}/${topics.length})` : 'Completed ✨'}
            </span>
          </div>
          <div className={`p-2 rounded-xl transition-all duration-300 ${isExpanded ? 'bg-slate-800 text-white' : 'text-slate-600'}`}>
            {isExpanded ? <ChevronUp className="w-6 h-6" /> : <ChevronDown className="w-6 h-6" />}
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="p-6 md:p-8 pt-0 space-y-6 animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="h-px bg-slate-800/80 mb-8" />
          <div className="grid grid-cols-1 gap-6">
            {topics.map((topic, i) => (
              <TopicCard 
                key={i} 
                topic={topic} 
                status={topicsProgress[topic.name] || 'not_started'}
                onStatusChange={(status) => onTopicStatusChange(topic.name, status)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
