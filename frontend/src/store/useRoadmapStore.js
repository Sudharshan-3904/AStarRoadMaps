import { create } from 'zustand'

const initialAgentStatuses = {
  analyst: 'pending',
  curriculum: 'pending',
  resources: 'pending',
  formatter: 'pending'
}

export const useRoadmapStore = create((set) => ({
  activeRoadmapId: null,
  agentStatuses: initialAgentStatuses,
  setActiveRoadmapId: (id) => set({ activeRoadmapId: id }),
  setAgentStatus: (agent, status) =>
    set((state) => ({
      agentStatuses: { ...state.agentStatuses, [agent]: status }
    })),
  resetAgentStatuses: () => set({ agentStatuses: initialAgentStatuses })
}))
