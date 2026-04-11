import React, { useState, useEffect } from 'react'
import { Button } from '../ui/Button'
import { SkillLevel } from '../../types/roadmap'
import { Target, BarChart, Clock, Settings, Cpu } from 'lucide-react'

interface GoalFormProps {
  onSubmit: (data: { 
    goal: string; 
    skill_level: SkillLevel; 
    hours_per_week: number;
    provider: string;
    model: string;
  }) => void
  isLoading: boolean
}

type Provider = 'anthropic' | 'openrouter' | 'ollama'

const PROVIDER_MODELS: Record<Provider, string[]> = {
  anthropic: ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"],
  openrouter: [
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4o",
    "meta-llama/llama-3.1-405b-instruct",
    "google/gemini-pro-1.5",
  ],
  ollama: ["llama3.2:latest", "qwen3.5:4b", "gemma4:e2b"],
};

export const GoalForm: React.FC<GoalFormProps> = ({ onSubmit, isLoading }) => {
  const [goal, setGoal] = useState('')
  const [skillLevel, setSkillLevel] = useState<SkillLevel>('beginner')
  const [hoursPerWeek, setHoursPerWeek] = useState(10)
  
  const [provider, setProvider] = useState<Provider>('openrouter')
  const [model, setModel] = useState(PROVIDER_MODELS.openrouter[0])
  const [showSettings, setShowSettings] = useState(false)

  // Sync model when provider changes
  useEffect(() => {
    setModel(PROVIDER_MODELS[provider][0])
  }, [provider])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!goal.trim()) return
    onSubmit({ 
      goal, 
      skill_level: skillLevel, 
      hours_per_week: hoursPerWeek,
      provider,
      model
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <div className="space-y-3">
        <label htmlFor="goal" className="flex items-center gap-2 text-sm font-semibold text-slate-300 uppercase tracking-widest">
          <Target className="w-4 h-4 text-teal-500" />
          What do you want to learn?
        </label>
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

      {/* AI Settings Toggle */}
      <div className="pt-4">
        <button
          type="button"
          onClick={() => setShowSettings(!showSettings)}
          className="flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-teal-400 uppercase tracking-[0.2em] transition-colors"
        >
          <Settings className={`w-4 h-4 transition-transform duration-300 ${showSettings ? 'rotate-90' : ''}`} />
          {showSettings ? 'Hide AI Settings' : 'Advanced AI Settings'}
        </button>

        {showSettings && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-8 p-6 bg-slate-950/30 border border-slate-800 rounded-3xl animate-in fade-in slide-in-from-top-2">
            <div className="space-y-3">
              <label className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-widest">
                AI Provider
              </label>
              <div className="grid grid-cols-3 gap-2">
                {(['anthropic', 'openrouter', 'ollama'] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setProvider(p)}
                    className={`px-3 py-2 rounded-xl text-[10px] font-bold uppercase transition-all border ${
                      provider === p 
                        ? 'bg-teal-500/10 border-teal-500 text-teal-400' 
                        : 'bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700'
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <label className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-widest">
                <Cpu className="w-4 h-4 text-teal-500" />
                Model Selection
              </label>
              <div className="relative">
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-2xl text-slate-300 text-sm font-medium focus:outline-none focus:ring-1 focus:ring-teal-500/50 appearance-none cursor-pointer"
                >
                  {PROVIDER_MODELS[provider].map((m) => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                  <option value="custom">Custom...</option>
                </select>
                {model === 'custom' && (
                  <input
                    type="text"
                    placeholder="Enter model identifier"
                    className="mt-2 w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-xl text-slate-300 text-sm focus:outline-none focus:ring-1 focus:ring-teal-500"
                    onBlur={(e) => setModel(e.target.value)}
                  />
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        className="w-full py-6 rounded-2xl text-xl font-bold font-sora shadow-lg shadow-teal-500/10 hover:shadow-teal-500/20"
        isLoading={isLoading}
      >
        {isLoading ? 'Processing...' : 'Generate Roadmap'}
      </Button>
    </form>
  )
}
