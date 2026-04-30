import React from 'react'
import { Link } from 'react-router-dom'
import { PageShell } from '../components/layout/PageShell'
import { useRoadmapsList, useDeleteRoadmap } from '../hooks/useRoadmap'
import { Card } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'
import { Calendar, Layers, ArrowRight, Trash2 } from 'lucide-react'
import { Spinner } from '../components/ui/Spinner'

/**
 * MyRoadmaps Page
 * Displays a grid of all roadmaps the user has generated, with options 
 * to view details or delete them.
 */
export const MyRoadmaps = () => {
  const { data: roadmaps, isLoading } = useRoadmapsList()

  if (isLoading) {
    return (
      <PageShell>
        <div className="h-[50vh] flex items-center justify-center">
          <Spinner size="lg" />
        </div>
      </PageShell>
    )
  }

  return (
    <PageShell>
      <div className="pt-20 pb-12">
        <div className="mb-12">
          <h1 className="text-3xl font-bold font-sora text-slate-100 mb-2">My Roadmaps</h1>
          <p className="text-slate-400">Manage all your personalized learning paths in one place.</p>
        </div>

        {roadmaps && roadmaps.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {roadmaps.map((roadmap) => (
              <RoadmapItemCard key={roadmap.id} roadmap={roadmap} />
            ))}
          </div>
        ) : (
          <EmptyState />
        )}
      </div>
    </PageShell>
  )
}

/**
 * Component for displaying a placeholder when no roadmaps exist.
 */
const EmptyState = () => (
  <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-3xl p-20 text-center">
    <div className="bg-slate-800 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
      <Layers className="w-8 h-8 text-slate-600" />
    </div>
    <h3 className="text-xl font-bold text-slate-300 mb-2">No roadmaps yet</h3>
    <p className="text-slate-500 mb-8 max-w-xs mx-auto">
      Ready to start something new? Generate your first roadmap today.
    </p>
    <Link 
      to="/" 
      className="inline-flex items-center gap-2 px-6 py-3 bg-teal-500 text-slate-900 rounded-xl font-bold hover:bg-teal-400 transition-colors"
    >
      Get Started
    </Link>
  </div>
)

/**
 * Individual roadmap preview card with status, date, and deletion action.
 */
const RoadmapItemCard = ({ roadmap }) => {
  const { mutate: deleteRoadmap } = useDeleteRoadmap()

  const date = new Date(roadmap.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })

  const handleDelete = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (window.confirm('Are you sure you want to delete this roadmap? Permanently?')) {
      deleteRoadmap(roadmap.id)
    }
  }

  return (
    <Link to={`/roadmap/${roadmap.id}`} className="block h-full">
      <Card className="group h-full flex flex-col justify-between relative overflow-hidden">
        <div className="absolute -inset-1 bg-gradient-to-r from-teal-500/20 to-blue-500/20 opacity-0 group-hover:opacity-100 transition-opacity blur-2xl -z-10" />
        
        <div>
          <div className="flex items-center justify-between mb-4">
            <Badge variant="teal">{roadmap.status}</Badge>
            <div className="flex items-center gap-3">
              <div className="flex items-center text-[10px] text-slate-500 uppercase tracking-widest font-bold">
                <Calendar className="w-3 h-3 mr-1" />
                {date}
              </div>
              <button 
                onClick={handleDelete}
                className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors z-10"
                aria-label="Delete Roadmap"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
          <h3 className="text-xl font-bold text-slate-100 mb-2 group-hover:text-teal-400 transition-colors line-clamp-2">
            {roadmap.title}
          </h3>
          <div className="flex items-center text-sm text-slate-500 gap-4 mb-6">
            <span className="flex items-center">
              <Layers className="w-4 h-4 mr-1.5 opacity-50" />
              {roadmap.topic_count} Topics
            </span>
          </div>
        </div>
        
        <div className="flex items-center text-teal-500 text-sm font-bold pt-4 border-t border-slate-700/50">
          View Roadmap
          <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
        </div>
      </Card>
    </Link>
  )
}
