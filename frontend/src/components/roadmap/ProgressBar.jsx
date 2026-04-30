import React from 'react'

/**
 * ProgressBar Component
 * A flexible progress indicator with optional labels and custom sizing/coloring.
 * Includes a subtle shimmer effect for a premium visual feel.
 * 
 * @param {Object} props
 * @param {number} props.progress - The percentage of completion (0-100).
 * @param {string} props.color - Tailwind background color class for the progress fill.
 * @param {string} props.size - Vertical size preset: 'sm' or 'md'.
 * @param {boolean} props.showLabel - Whether to display a text label with the percentage.
 */
export const ProgressBar = ({ 
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
          {/* Shimmer overlay for enhanced aesthetics */}
          <div className="absolute inset-0 bg-white/20 animate-[shimmer_2s_infinite] -skew-x-12" />
        </div>
      </div>
    </div>
  )
}
