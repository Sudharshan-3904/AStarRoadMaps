import { create } from 'zustand'
import { AgentName } from '../types/roadmap'

interface RoadmapStore {
  activeRoadmapId: string | null
  agentStatuses: Record<AgentName, 'pending' | 'running' | 'done' | 'error'>
  setActiveRoadmapId: (id: string | null) => void
  setAgentStatus: (agent: AgentName, status: 'pending' | 'running' | 'done' | 'error') => void
  resetAgentStatuses: () => void
}

const initialAgentStatuses: Record<AgentName, 'pending' | 'running' | 'done' | 'error'> = {
  analyst: 'pending',
  curriculum: 'pending',
  resources: 'pending',
  formatter: 'pending'
}

export const useRoadmapStore = create<RoadmapStore>((set) => ({
  activeRoadmapId: null,
  agentStatuses: initialAgentStatuses,
  setActiveRoadmapId: (id) => set({ activeRoadmapId: id }),
  setAgentStatus: (agent, status) =>
    set((state) => ({
      agentStatuses: { ...state.agentStatuses, [agent]: status }
    })),
  resetAgentStatuses: () => set({ agentStatuses: initialAgentStatuses })
}))
