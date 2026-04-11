import { useEffect, useState, useCallback } from 'react'
import { useRoadmapStore } from '../store/useRoadmapStore'
import { SSEEvent } from '../types/roadmap'
import { useQueryClient } from '@tanstack/react-query'

export const useRoadmapStream = (roadmapId: string | null, feedback?: string, feedbackType?: string) => {
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const setAgentStatus = useRoadmapStore((state) => state.setAgentStatus)
  const queryClient = useQueryClient()

  const startStream = useCallback(() => {
    if (!roadmapId) return

    setIsStreaming(true)
    setError(null)

    let url = `/api/roadmaps/${roadmapId}/stream`
    const params = new URLSearchParams()
    if (feedback) params.append('feedback', feedback)
    if (feedbackType) params.append('feedback_type', feedbackType)
    
    const queryString = params.toString()
    if (queryString) url += `?${queryString}`

    const eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      const data: SSEEvent = JSON.parse(event.data)

      switch (data.type) {
        case 'agent_start':
          if (data.agent) setAgentStatus(data.agent, 'running')
          break
        case 'agent_done':
          if (data.agent) setAgentStatus(data.agent, 'done')
          break
        case 'agent_error':
          if (data.agent) setAgentStatus(data.agent, 'error')
          break
        case 'complete':
          setIsStreaming(false)
          eventSource.close()
          queryClient.invalidateQueries({ queryKey: ['roadmap', roadmapId] })
          break
        case 'error':
          setError(data.message || 'An unknown error occurred')
          setIsStreaming(false)
          eventSource.close()
          break
      }
    }

    eventSource.onerror = (err) => {
      console.error('SSE Error:', err)
      setError('Connection to server lost')
      setIsStreaming(false)
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [roadmapId, feedback, feedbackType, setAgentStatus, queryClient])

  useEffect(() => {
    const cleanup = startStream()
    return cleanup
  }, [startStream])

  return { isStreaming, error }
}
