import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'

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

export const useRoadmapsList = () => {
  return useQuery({
    queryKey: ['roadmaps'],
    queryFn: async () => {
      const response = await api.get('/roadmaps')
      return response.data
    }
  })
}

export const useDeleteRoadmap = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (roadmapId) => {
      await api.delete(`/roadmaps/${roadmapId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roadmaps'] })
    }
  })
}
