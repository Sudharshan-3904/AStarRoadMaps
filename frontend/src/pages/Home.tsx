import React from 'react'
import { useNavigate } from 'react-router-dom'
import { PageShell } from '../components/layout/PageShell'
import { GoalForm } from '../components/generator/GoalForm'
import { useGenerateRoadmap } from '../hooks/useGenerateRoadmap'
import { Sparkles, Brain, Rocket, Shield, Zap } from 'lucide-react'

export const Home: React.FC = () => {
  const navigate = useNavigate()
  const { mutate: generate, isPending } = useGenerateRoadmap()

  const handleSubmit = (data: any) => {
    generate(data, {
      onSuccess: ({ roadmap_id }) => {
        navigate(`/generate/${roadmap_id}`)
      }
    })
  }

  return (
    <PageShell>
      {/* Hero Section */}
      <section className="text-center mb-20">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/50 border border-slate-700/50 text-teal-400 text-xs font-bold uppercase tracking-widest mb-8 animate-in fade-in slide-in-from-top-4 duration-1000">
          <Sparkles className="w-4 h-4" />
          Choose the model that suits you best
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight tracking-tight px-4 font-sora">
          Master Any Skill <br className="hidden md:block" />
          with{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-emerald-400">
            Precision.
          </span>
        </h1>

        <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
          The ultimate AI-powered roadmap generator. Go from zero to mastery
          with expert-curated modules and specialized resources.
        </p>
      </section>

      {/* Main Input Section */}
      <section className="max-w-3xl mx-auto mb-32 relative">
        <div className="absolute -inset-1 bg-gradient-to-r from-teal-500 to-blue-500 rounded-3xl blur opacity-20" />
        <div className="relative bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 md:p-12 shadow-2xl">
          <GoalForm onSubmit={handleSubmit} isLoading={isPending} />
        </div>
      </section>

      {/* Features Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard
          icon={<Brain className="w-8 h-8 text-teal-400" />}
          title="Intelligent Analysis"
          description="Advanced reasoning models analyze your goal to create a perfectly structured study path."
        />
        <FeatureCard
          icon={<Zap className="w-8 h-8 text-emerald-400" />}
          title="Optimized Path"
          description="Focus on what truly matters. We skip the fluff and direct you to the most efficient learning route."
        />
        <FeatureCard
          icon={<Shield className="w-8 h-8 text-blue-400" />}
          title="Verified Resources"
          description="Every link is checked for quality. Get official docs, top tutorials, and project ideas."
        />
      </section>
    </PageShell>
  );
}

const FeatureCard: React.FC<{ icon: React.ReactNode; title: string, description: string }> = ({ icon, title, description }) => (
  <div className="p-8 bg-slate-900/40 border border-slate-800/50 rounded-2xl hover:bg-slate-800/40 transition-all duration-300 hover:scale-[1.02] group">
    <div className="mb-6 p-4 bg-slate-950 rounded-2xl w-fit group-hover:rotate-6 transition-transform">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-slate-100 mb-3 font-sora">{title}</h3>
    <p className="text-slate-400 leading-relaxed text-sm">{description}</p>
  </div>
)
