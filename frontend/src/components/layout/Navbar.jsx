import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Compass, List } from 'lucide-react'

/**
 * Navbar Component
 * The global navigation bar with backdrop blur and sticky positioning.
 * Features a dynamic logo and breadcrumb-style navigation links.
 */
export const Navbar = () => {
  const location = useLocation()

  return (
    <nav className="h-20 border-b border-slate-800/50 bg-[#020617]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
        {/* Logo and Branding */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="bg-teal-500 rounded-xl p-2 group-hover:rotate-12 transition-all duration-300 shadow-lg shadow-teal-500/20">
            <Compass className="w-6 h-6 text-slate-900" />
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-bold font-sora text-white leading-tight tracking-tight">
              AStar<span className="text-teal-400">RoadMaps</span>
            </span>
            <span className="text-[10px] text-slate-500 uppercase font-bold tracking-[0.2em]">Next-Gen Learning</span>
          </div>
        </Link>
        
        {/* Navigation Actions */}
        <div className="flex items-center gap-2">
          <NavLink 
            to="/" 
            active={location.pathname === '/'}
            label="Create"
          />
          <NavLink 
            to="/my-roadmaps" 
            active={location.pathname === '/my-roadmaps'}
            label="My Library"
            icon={<List className="w-4 h-4" />}
          />
        </div>
      </div>
    </nav>
  )
}

/**
 * Individual navigation link with active state styling.
 */
const NavLink = ({ to, active, label, icon }) => (
  <Link 
    to={to} 
    className={`px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-all duration-200 ${
      active 
        ? 'text-teal-400 bg-teal-400/10' 
        : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800'
    }`}
  >
    {icon}
    {label}
  </Link>
)
