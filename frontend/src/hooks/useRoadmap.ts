import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import { Roadmap } from '../types/roadmap'

export const useRoadmap = (roadmapId: string | null) => {
  return useQuery({
    queryKey: ['roadmap', roadmapId],
    queryFn: async () => {
      if (!roadmapId) return null
      const response = await api.get<Roadmap>(`/roadmaps/${roadmapId}`)
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
