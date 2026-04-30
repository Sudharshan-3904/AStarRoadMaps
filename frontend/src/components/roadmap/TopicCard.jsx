import React from 'react'
import { ResourceLink } from './ResourceLink'
import { CheckCircle2, Clock, Boxes, Lightbulb, Circle } from 'lucide-react'

/**
 * TopicCard Component
 * Represents an individual learning unit within a phase.
 * Features progress tracking, resource listings, and project suggestions.
 * 
 * @param {Object} props
 * @param {Object} props.topic - The topic data object including subtopics and resources.
 * @param {string} props.status - Current completion status: 'not_started', 'in_progress', or 'done'.
 * @param {Function} props.onStatusChange - Callback for updating the topic status.
 */
export const TopicCard = ({ topic, status = 'not_started', onStatusChange }) => {
  
  /**
   * Returns the appropriate visual style class based on the topic status.
   */
  const getStatusColor = () => {
    switch (status) {
      case 'done': return 'border-emerald-500/30 bg-emerald-500/5'
      case 'in_progress': return 'border-amber-500/30 bg-amber-500/5'
      default: return 'border-slate-800 bg-slate-900/50'
    }
  }

  return (
    <div className={`p-6 rounded-2xl border transition-all duration-300 ${getStatusColor()}`}>
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1">
          <h4 className="text-lg font-bold text-white mb-2 font-sora flex items-center gap-2">
            {topic.name}
            {status === 'done' && (
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 uppercase tracking-wider">
                Mastered
              </span>
            )}
          </h4>
          
          {topic.content && (
            <p className="text-slate-400 text-sm leading-relaxed mb-4 italic">
               {topic.content}
            </p>
          )}

          {/* Subtopic Chips */}
          <div className="flex flex-wrap gap-2">
            {topic.subtopics.map((sub, i) => (
              <span key={i} className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400 text-[10px] font-medium border border-slate-700/50">
                {sub}
              </span>
            ))}
          </div>
        </div>

        {/* Status Selector */}
        <select
          value={status}
          onChange={(e) => onStatusChange(e.target.value)}
          className="bg-slate-800 border-none rounded-lg text-xs font-bold text-slate-300 px-3 py-2 cursor-pointer hover:bg-slate-700 transition-colors focus:ring-1 focus:ring-teal-500"
        >
          <option value="not_started">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>

      {/* Resource Section */}
      {topic.resources && topic.resources.length > 0 && (
        <div className="space-y-3 pt-4 border-t border-slate-800/50">
          <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">
             <Boxes className="w-3 h-3" /> Learning Resources
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {topic.resources.map((res, i) => (
              <ResourceLink key={i} resource={res} />
            ))}
          </div>
        </div>
      )}

      {/* Project Highlight */}
      {topic.project && (
        <div className="mt-4 p-4 rounded-xl bg-teal-500/5 border border-teal-500/20">
          <div className="flex items-center gap-2 text-[10px] font-bold text-teal-400 uppercase tracking-widest mb-1.5">
            <Lightbulb className="w-3 h-3" /> Hands-on Project
          </div>
          <p className="text-slate-300 text-xs leading-relaxed">
            {topic.project}
          </p>
        </div>
      )}
    </div>
  )
}
