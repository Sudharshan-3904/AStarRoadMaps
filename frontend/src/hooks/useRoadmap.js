import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'

/**
 * Fetches detailed data for a specific roadmap.
 */
export const useRoadmap = (roadmapId) => {
  return useQuery({
    queryKey: ['roadmap', roadmapId],
    queryFn: async () => {
      if (!roadmapId) return null
      const response = await api.get(`/roadmaps/${roadmapId}`)
      return response.data
    },
    enabled: !!roadmapId
  })
}

/**
 * Fetches a summary list of all roadmaps for the library view.
 */
export const useRoadmapsList = () => {
  return useQuery({
    queryKey: ['roadmaps'],
    queryFn: async () => {
      const response = await api.get('/roadmaps')
      return response.data
    }
  })
}

/**
 * Mutation hook to delete a roadmap and refresh the library list.
 */
export const useDeleteRoadmap = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (roadmapId) => {
      await api.delete(`/roadmaps/${roadmapId}`)
    },
    onSuccess: () => {
      // Refresh the library list after successful deletion
      queryClient.invalidateQueries({ queryKey: ['roadmaps'] })
    }
  })
}
