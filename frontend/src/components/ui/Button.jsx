import React from 'react'
import { Loader2 } from 'lucide-react'

/**
 * Button Component
 * A highly customizable action button with built-in variants, sizes, and 
 * loading states. Includes micro-interactions like scale-down on click.
 * 
 * @param {Object} props
 * @param {string} props.variant - The visual style: 'primary', 'secondary', 'outline', 'ghost', 'danger'.
 * @param {string} props.size - The padding/font size: 'sm', 'md', 'lg'.
 * @param {boolean} props.isLoading - Whether to show a spinner and disable interaction.
 */
export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-bold transition-all duration-300 focus:outline-[none] active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed group'
  
  const variants = {
    primary: 'bg-teal-500 text-slate-950 hover:bg-teal-400 shadow-lg shadow-teal-500/10 hover:shadow-teal-500/30',
    secondary: 'bg-slate-800 text-slate-100 hover:bg-slate-700 shadow-lg shadow-slate-900/50',
    outline: 'border-2 border-slate-700 text-slate-300 hover:border-teal-500/50 hover:text-teal-400 hover:bg-teal-500/5',
    ghost: 'text-slate-400 hover:text-slate-100 hover:bg-slate-800',
    danger: 'bg-red-500/10 border border-red-500/20 text-red-500 hover:bg-red-500 hover:text-white'
  }

  const sizes = {
    sm: 'px-4 py-2 text-xs rounded-xl',
    md: 'px-6 py-3 text-sm rounded-xl',
    lg: 'px-8 py-4 text-lg rounded-2xl'
  }

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <Loader2 className="w-5 h-5 animate-spin mr-3 text-current" />
      )}
      <span className="relative z-10">{children}</span>
    </button>
  )
}
