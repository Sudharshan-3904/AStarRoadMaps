import React from 'react'
import { Topic, TopicStatus } from '../../types/roadmap'
import { ResourceLink } from './ResourceLink'
import { StatusBadge } from './StatusBadge'
import { Code, Layers, FileSearch, CheckCircle2 } from 'lucide-react'

interface TopicCardProps {
  topic: Topic
  status: TopicStatus
  onStatusChange: (status: TopicStatus) => void
}

export const TopicCard: React.FC<TopicCardProps> = ({ topic, status, onStatusChange }) => {
  const isDone = status === 'done'

  return (
    <div className={`group relative bg-slate-950/40 border rounded-2xl p-6 transition-all duration-300 ${
      isDone ? 'border-teal-500/30' : 'border-slate-800/80 hover:border-slate-700'
    }`}>
      {isDone && (
        <div className="absolute top-4 right-4 text-teal-500 animate-in zoom-in duration-300">
          <CheckCircle2 className="w-6 h-6" />
        </div>
      )}
      
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <div className={`p-1.5 rounded-lg ${isDone ? 'bg-teal-500/10 text-teal-400' : 'bg-slate-800 text-slate-400'}`}>
              <Layers className="w-5 h-5" />
            </div>
            <h4 className="text-xl font-bold text-white font-sora">{topic.name}</h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {topic.subtopics.map((sub, i) => (
              <span key={i} className="text-xs font-medium text-slate-500 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-800/50">
                {sub}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex items-center gap-4 shrink-0">
          <div className="hidden sm:block">
            <StatusBadge status={status} />
          </div>
          <select 
            value={status} 
            onChange={(e) => onStatusChange(e.target.value as TopicStatus)}
            className="bg-slate-900 border border-slate-700 text-sm font-bold text-slate-300 rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-teal-500/50 cursor-pointer hover:bg-slate-800 transition-all appearance-none pr-10 relative bg-[url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20fill%3D%27none%27%20viewBox%3D%270%200%2020%2020%27%3E%3Cpath%20stroke%3D%27%236b7280%27%20stroke-linecap%3D%27round%27%20stroke-linejoin%3D%27round%27%20stroke-width%3D%271.5%27%20d%3D%27m6%208%204%204%204-4%27%2F%3E%3C%2Fsvg%3E')] bg-[position:right_0.5rem_center] bg-[length:1.5em_1.5em] bg-no-repeat"
          >
            <option value="not_started">Not Started</option>
            <option value="in_progress">Learning</option>
            <option value="done">Completed</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
            <FileSearch className="w-3.5 h-3.5" /> Learning Resources
          </div>
          <div className="space-y-2">
            {topic.resources.map((res, i) => (
              <ResourceLink key={i} resource={res} />
            ))}
          </div>
        </div>

        {topic.project && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
              <Code className="w-3.5 h-3.5" /> Hands-on Project
            </div>
            <div className="bg-slate-950/50 border border-slate-800/50 rounded-2xl p-5 text-sm md:text-base text-slate-400 leading-relaxed font-mono">
              <span className="text-teal-500/50 mr-2">$</span>
              {topic.project}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
