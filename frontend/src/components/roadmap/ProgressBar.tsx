import React from 'react'

interface ProgressBarProps {
  progress: number // 0 to 100
  color?: string
  size?: 'sm' | 'md'
  showLabel?: boolean
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ 
  progress, 
  color = 'bg-teal-500', 
  size = 'sm',
  showLabel = false 
}) => {
  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Progress</span>
          <span className="text-xs font-bold text-teal-400">{Math.round(progress)}%</span>
        </div>
      )}
      <div className={`w-full ${size === 'sm' ? 'h-1' : 'h-2'} bg-slate-700 rounded-full overflow-hidden`}>
        <div 
          className={`h-full ${color} transition-all duration-1000 ease-out relative`}
          style={{ width: `${progress}%` }}
        >
          {/* Shimmer effect while generating or just as a premium touch */}
          <div className="absolute inset-0 bg-white/20 animate-[shimmer_2s_infinite] -skew-x-12" />
        </div>
      </div>
    </div>
  )
}
