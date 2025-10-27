import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const chatAPI = {
  sendMessage: async (query, sessionId, activeTools) => {
    const response = await api.post('/api/chat/send', {
      query,
      session_id: sessionId,
      active_tools: activeTools,
    })
    return response.data
  },

  getHistory: async (sessionId, limit = 50) => {
    const response = await api.get(`/api/chat/history/${sessionId}`, {
      params: { limit },
    })
    return response.data
  },

  clearSession: async (sessionId) => {
    const response = await api.delete(`/api/chat/session/${sessionId}`)
    return response.data
  },

  listSessions: async (limit = 20) => {
    const response = await api.get('/api/chat/sessions', {
      params: { limit },
    })
    return response.data
  },
}

// MCP Tools API
export const mcpAPI = {
  listTools: async () => {
    const response = await api.get('/api/mcp/tools')
    return response.data
  },

  getToolInfo: async (toolName) => {
    const response = await api.get(`/api/mcp/tools/${toolName}`)
    return response.data
  },

  toggleTool: async (toolName, enabled) => {
    const response = await api.post('/api/mcp/tools/toggle', {
      tool_name: toolName,
      enabled,
    })
    return response.data
  },

  executeTool: async (toolName, action, params = {}) => {
    const response = await api.post('/api/mcp/tools/execute', {
      tool_name: toolName,
      action,
      params,
    })
    return response.data
  },

  getActiveTools: async () => {
    const response = await api.get('/api/mcp/tools/active')
    return response.data
  },
}

// Memory API
export const memoryAPI = {
  getToolLogs: async (sessionId = null, toolName = null, limit = 50) => {
    const response = await api.get('/api/memory/logs', {
      params: { session_id: sessionId, tool_name: toolName, limit },
    })
    return response.data
  },

  getStats: async () => {
    const response = await api.get('/api/memory/stats')
    return response.data
  },
}

// WebSocket connection
export const createWebSocket = (sessionId, onMessage) => {
  const wsUrl = API_BASE_URL.replace('http', 'ws')
  const ws = new WebSocket(`${wsUrl}/api/ws/chat/${sessionId}`)

  ws.onopen = () => {
    console.log('🔌 WebSocket connected')
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }

  ws.onerror = (error) => {
    console.error('❌ WebSocket error:', error)
  }

  ws.onclose = () => {
    console.log('🔌 WebSocket disconnected')
  }

  return ws
}

export default api
