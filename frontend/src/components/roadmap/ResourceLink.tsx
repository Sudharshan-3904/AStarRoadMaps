import React from 'react'
import { BookOpen, Video, FileText, Wrench, ExternalLink } from 'lucide-react'
import { Resource } from '../../types/roadmap'

interface ResourceLinkProps {
  resource: Resource
}

export const ResourceLink: React.FC<ResourceLinkProps> = ({ resource }) => {
  const getIcon = () => {
    switch (resource.type) {
      case 'docs': return <BookOpen className="w-4 h-4" />
      case 'video': return <Video className="w-4 h-4" />
      case 'article': return <FileText className="w-4 h-4" />
      case 'interactive': return <Wrench className="w-4 h-4" />
      default: return <ExternalLink className="w-4 h-4" />
    }
  }

  return (
    <a 
      href={resource.url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="flex items-center gap-2 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-300 hover:text-teal-400 hover:border-teal-500/30 transition-all group"
    >
      <span className="text-slate-500 group-hover:text-teal-500 transition-colors">
        {getIcon()}
      </span>
      <span className="line-clamp-1">{resource.label}</span>
      <ExternalLink className="w-3 h-3 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
    </a>
  )
}
