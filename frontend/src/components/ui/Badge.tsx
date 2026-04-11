import React from 'react'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'blue' | 'yellow' | 'orange' | 'red' | 'teal' | 'slate'
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'slate' }) => {
  const variants = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    orange: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
    teal: 'bg-teal-500/10 text-teal-400 border-teal-500/20',
    slate: 'bg-slate-500/10 text-slate-400 border-slate-500/20'
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${variants[variant]}`}>
      {children}
    </span>
  )
}
