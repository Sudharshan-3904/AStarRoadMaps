import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import { useRoadmapStore } from '../store/useRoadmapStore'

interface RefineRequest {
  feedback: string
}

interface RefineResponse {
  roadmap_id: string
  feedback_type: string
  feedback: string
}

export const useRefine = (roadmapId: string | null) => {
  const resetAgentStatuses = useRoadmapStore((state) => state.resetAgentStatuses)

  return useMutation({
    mutationFn: async (data: RefineRequest) => {
      const response = await api.patch<RefineResponse>(`/roadmaps/${roadmapId}/refine`, data)
      return response.data
    },
    onSuccess: () => {
      resetAgentStatuses()
    }
  })
}
