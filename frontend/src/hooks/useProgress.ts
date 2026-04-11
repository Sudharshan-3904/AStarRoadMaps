import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'
import { ProgressState, TopicStatus } from '../types/roadmap'

export const useProgress = (roadmapId: string | null) => {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: ['progress', roadmapId],
    queryFn: async () => {
      if (!roadmapId) return null
      const response = await api.get<ProgressState>(`/roadmaps/${roadmapId}/progress`)
      return response.data
    },
    enabled: !!roadmapId
  })

  const mutation = useMutation({
    mutationFn: async ({ topic_name, status }: { topic_name: string; status: TopicStatus }) => {
      const response = await api.patch<ProgressState>(`/roadmaps/${roadmapId}/progress`, {
        topic_name,
        status
      })
      return response.data
    },
    onSuccess: (data) => {
      queryClient.setQueryData(['progress', roadmapId], data)
    }
  })

  return { ...query, updateProgress: mutation.mutate }
}
