import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import { useRoadmapStore } from '../store/useRoadmapStore'

export const useRefine = (roadmapId) => {
  const resetAgentStatuses = useRoadmapStore((state) => state.resetAgentStatuses)

  return useMutation({
    mutationFn: async (data) => {
      const response = await api.patch(`/roadmaps/${roadmapId}/refine`, data)
      return response.data
    },
    onSuccess: () => {
      resetAgentStatuses()
    }
  })
}
