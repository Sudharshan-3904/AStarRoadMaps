import React from 'react'

export const Card = ({ children, className = '', onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-xl transition-all duration-300 ${onClick ? 'cursor-pointer hover:border-teal-500/50 hover:bg-slate-800/80' : ''} ${className}`}
    >
      {children}
    </div>
  )
}
