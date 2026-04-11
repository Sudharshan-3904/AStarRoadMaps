import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import { SkillLevel } from '../types/roadmap'

interface GenerateRequest {
  goal: string
  skill_level: SkillLevel
  hours_per_week: number
  provider: string
  model: string
}

interface GenerateResponse {
  roadmap_id: string
}

export const useGenerateRoadmap = () => {
  return useMutation({
    mutationFn: async (data: GenerateRequest) => {
      const response = await api.post<GenerateResponse>('/roadmaps/generate', data)
      return response.data
    }
  })
}
