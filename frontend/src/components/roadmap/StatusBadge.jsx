import React from 'react'

export const StatusBadge = ({ status }) => {
  const styles = {
    not_started: 'bg-slate-700/50 text-slate-400 border-slate-600/50',
    in_progress: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
    done: 'bg-teal-500/10 text-teal-500 border-teal-500/20'
  }

  const labels = {
    not_started: 'Not Started',
    in_progress: 'In Progress',
    done: 'Done'
  }

  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${styles[status]}`}>
      {labels[status]}
    </span>
  )
}
