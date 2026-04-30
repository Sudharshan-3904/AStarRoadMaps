import { create } from 'zustand'

/**
 * Default states for AI agents involved in the roadmap generation pipeline.
 */
const initialAgentStatuses = {
  analyst: 'pending',
  curriculum: 'pending',
  resources: 'pending',
  formatter: 'pending'
}

/**
 * useRoadmapStore
 * Global state management for tracking the active roadmap session and 
 * the real-time status of the multi-agent generation process.
 */
export const useRoadmapStore = create((set) => ({
  activeRoadmapId: null,
  agentStatuses: initialAgentStatuses,
  
  /**
   * Sets the ID of the roadmap currently being generated or viewed.
   */
  setActiveRoadmapId: (id) => set({ activeRoadmapId: id }),
  
  /**
   * Updates the status of a specific AI agent in the pipeline.
   */
  setAgentStatus: (agent, status) =>
    set((state) => ({
      agentStatuses: { ...state.agentStatuses, [agent]: status }
    })),
  
  /**
   * Resets all agent statuses to 'pending' for a new generation cycle.
   */
  resetAgentStatuses: () => set({ agentStatuses: initialAgentStatuses })
}))
