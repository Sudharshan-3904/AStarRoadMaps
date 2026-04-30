import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Home } from './pages/Home'
import { Generate } from './pages/Generate'
import { Roadmap } from './pages/Roadmap'
import { MyRoadmaps } from './pages/MyRoadmaps'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generate/:roadmapId" element={<Generate />} />
          <Route path="/roadmap/:roadmapId" element={<Roadmap />} />
          <Route path="/my-roadmaps" element={<MyRoadmaps />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
