import React, { useState } from 'react'
import { Sparkles } from 'lucide-react'
import { Button } from '../ui/Button'

/**
 * RefinePanel Component
 * Provides a text interface for users to submit natural language feedback
 * to adjust the current roadmap's structure or content.
 * 
 * @param {Object} props
 * @param {Function} props.onSubmit - Callback function triggered on form submission.
 * @param {boolean} props.isLoading - State indicating if a refinement request is in progress.
 */
export const RefinePanel = ({ onSubmit, isLoading }) => {
  const [feedback, setFeedback] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!feedback.trim()) return
    onSubmit(feedback)
    setFeedback('')
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-teal-500/10 p-2 rounded-lg">
          <Sparkles className="w-5 h-5 text-teal-400" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-slate-100 font-sora">Refine Roadmap</h3>
          <p className="text-sm text-slate-400">Add topics, adjust difficulty, or change focus</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="e.g. 'Add a section on GraphQL' or 'Make it more focused on beginners'"
          className="w-full h-32 px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50 transition-all resize-none"
          required
        />
        <div className="flex justify-end">
          <Button 
            type="submit" 
            isLoading={isLoading}
            variant="primary"
          >
            Update Roadmap
          </Button>
        </div>
      </form>
    </div>
  )
}
