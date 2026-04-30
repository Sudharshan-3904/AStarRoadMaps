import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'

export const useGenerateRoadmap = () => {
  return useMutation({
    mutationFn: async (data) => {
      const response = await api.post('/roadmaps/generate', data)
      return response.data
    }
  })
}
