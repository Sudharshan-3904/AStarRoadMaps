import React from 'react'
import { Download, Calendar, Target, Clock, Trophy } from 'lucide-react'
import { Button } from '../ui/Button'

export const RoadmapHeader = ({ roadmap }) => {
  const downloadMarkdown = () => {
    window.location.href = `/api/roadmaps/${roadmap.id}/markdown`
  }

  return (
    <div className="space-y-6 pt-8 pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold font-sora text-slate-100 mb-2">
            {roadmap.title}
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl">
            A personalized path from {roadmap.spec.skill_level} to mastery.
          </p>
        </div>
        <Button variant="outline" onClick={downloadMarkdown} className="w-fit">
          <Download className="w-4 h-4 mr-2" />
          Export Markdown
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon={<Target className="w-4 h-4 text-teal-400" />} label="Goal" value={roadmap.spec.goal} />
        <StatCard icon={<Trophy className="w-4 h-4 text-teal-400" />} label="Level" value={roadmap.spec.skill_level} />
        <StatCard icon={<Clock className="w-4 h-4 text-teal-400" />} label="Weekly" value={`${roadmap.spec.hours_per_week}h`} />
        <StatCard icon={<Calendar className="w-4 h-4 text-teal-400" />} label="Duration" value={`${roadmap.spec.estimated_weeks} Weeks`} />
      </div>
    </div>
  )
}

const StatCard = ({ icon, label, value }) => (
  <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4 flex items-center space-x-3">
    <div className="bg-slate-900/50 p-2 rounded-lg">
      {icon}
    </div>
    <div>
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">{label}</p>
      <p className="text-sm font-medium text-slate-200 capitalize">{value}</p>
    </div>
  </div>
)
