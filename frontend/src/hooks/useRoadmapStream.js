import { useEffect, useState, useCallback } from 'react'
import { useRoadmapStore } from '../store/useRoadmapStore'
import { useQueryClient } from '@tanstack/react-query'

export const useRoadmapStream = (roadmapId, feedback, feedbackType) => {
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState(null)
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

    console.log(`[SSE] Connecting to ${url}...`)
    const eventSource = new EventSource(url)

    eventSource.onopen = () => {
      console.log('[SSE] Connection established.')
    }

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log(`[SSE] Received event: ${data.type}`, data)

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
            console.log('[SSE] Pipeline complete.')
            setIsStreaming(false)
            eventSource.close()
            queryClient.invalidateQueries({ queryKey: ['roadmap', roadmapId] })
            break
          case 'error':
            console.error('[SSE] Server emitted error:', data.message)
            setError(data.message || 'An unknown error occurred')
            setIsStreaming(false)
            eventSource.close()
            break
        }
      } catch (err) {
        console.error('[SSE] Failed to parse event data:', err)
      }
    }

    eventSource.onerror = (err) => {
      // EventSource readyState: 0 = CONNECTING, 1 = OPEN, 2 = CLOSED
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log('[SSE] Connection closed cleanly.')
      } else if (eventSource.readyState === EventSource.CONNECTING) {
        console.warn('[SSE] Connection lost, attempting to reconnect...')
        // We don't necessarily want to show an error yet as EventSource retries automatically
      } else {
        console.error('[SSE] Fatal connection error.', err)
        setError('Connection to server lost')
        setIsStreaming(false)
        eventSource.close()
      }
    }

    return () => {
      console.log('[SSE] Cleaning up connection.')
      eventSource.close()
    }
  }, [roadmapId, feedback, feedbackType, setAgentStatus, queryClient])

  useEffect(() => {
    const cleanup = startStream()
    return cleanup
  }, [startStream])

  return { isStreaming, error }
}
