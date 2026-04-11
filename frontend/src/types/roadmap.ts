export type SkillLevel = 'beginner' | 'intermediate' | 'advanced'
export type TopicStatus = 'not_started' | 'in_progress' | 'done'
export type AgentName = 'analyst' | 'curriculum' | 'resources' | 'formatter'
export type SSEEventType = 'agent_start' | 'agent_done' | 'agent_error' | 'complete' | 'error'

export interface Resource {
  label: string
  url: string
  type: string // "docs" | "video" | "article" | "interactive"
}

export interface Topic {
  name: string
  subtopics: string[]
  resources: Resource[]
  project?: string
}

export interface Phase {
  phase_number: number
  title: string
  week_range: string
  topics: Topic[]
}

export interface UserSpec {
  goal: string
  skill_level: SkillLevel
  hours_per_week: number
  estimated_weeks: number
}

export interface Roadmap {
  id: string
  title: string
  spec: UserSpec
  phases: Phase[]
  created_at: string
  status: string // "pending" | "generating" | "complete" | "error"
}

export interface ProgressState {
  roadmap_id: string
  topics: Record<string, TopicStatus>
}

export interface SSEEvent {
  type: SSEEventType
  agent?: AgentName
  roadmap_id?: string
  message?: string
}

export interface RoadmapListItem {
  id: string
  title: string
  created_at: string
  status: string
  topic_count: number
}
