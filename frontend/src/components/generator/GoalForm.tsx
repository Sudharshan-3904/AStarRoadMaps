import React, { useState } from 'react'
import { Button } from '../ui/Button'
import { SkillLevel } from '../../types/roadmap'
import { Target, BarChart, Clock } from 'lucide-react'

interface GoalFormProps {
  onSubmit: (data: { goal: string; skill_level: SkillLevel; hours_per_week: number }) => void
  isLoading: boolean
}

export const GoalForm: React.FC<GoalFormProps> = ({ onSubmit, isLoading }) => {
  const [goal, setGoal] = useState('')
  const [skillLevel, setSkillLevel] = useState<SkillLevel>('beginner')
  const [hoursPerWeek, setHoursPerWeek] = useState(10)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!goal.trim()) return
    onSubmit({ goal, skill_level: skillLevel, hours_per_week: hoursPerWeek })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <div className="space-y-3">
        <label htmlFor="goal" className="flex items-center gap-2 text-sm font-semibold text-slate-300 uppercase tracking-widest">
          <Target className="w-4 h-4 text-teal-500" />
          What do you want to learn?
        </label>
        <div className="relative group">
          <input
            id="goal"
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Backend Developer, Docker, React Native"
            className="w-full px-6 py-4 bg-slate-950/50 border border-slate-700/50 rounded-2xl text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50 transition-all text-lg font-medium"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-3">
          <label htmlFor="skill-level" className="flex items-center gap-2 text-sm font-semibold text-slate-300 uppercase tracking-widest">
            <BarChart className="w-4 h-4 text-emerald-500" />
            Current Skill Level
          </label>
          <select
            id="skill-level"
            value={skillLevel}
            onChange={(e) => setSkillLevel(e.target.value as SkillLevel)}
            className="w-full px-6 py-4 bg-slate-950/50 border border-slate-700/50 rounded-2xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 transition-all cursor-pointer appearance-none text-lg font-medium"
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className="space-y-3">
          <label htmlFor="hours" className="flex items-center gap-2 text-sm font-semibold text-slate-300 uppercase tracking-widest">
            <Clock className="w-4 h-4 text-blue-500" />
            Hours per week
          </label>
          <div className="relative">
            <input
              id="hours"
              type="number"
              min="1"
              max="168"
              value={hoursPerWeek}
              onChange={(e) => setHoursPerWeek(parseInt(e.target.value))}
              className="w-full px-6 py-4 bg-slate-950/50 border border-slate-700/50 rounded-2xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 transition-all text-lg font-medium"
              required
            />
            <span className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-600 font-bold">hrs</span>
          </div>
        </div>
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        className="w-full py-6 rounded-2xl text-xl font-bold font-sora shadow-lg shadow-teal-500/10 hover:shadow-teal-500/20 active:scale-[0.98] transition-all"
        isLoading={isLoading}
      >
        {isLoading ? 'Processing...' : 'Generate Roadmap'}
      </Button>
    </form>
  )
}
