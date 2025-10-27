import { createContext, useContext, useState, useCallback } from 'react'
import { chatAPI } from '../utils/api'

const ChatContext = createContext()

export const useChat = () => {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within ChatProvider')
  }
  return context
}

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('sessionId') || `session_${Date.now()}`
  })
  const [isLoading, setIsLoading] = useState(false)
  const [sessions, setSessions] = useState([])

  const sendMessage = useCallback(async (query, activeTools) => {
    if (!query.trim()) return

    // Add user message
    const userMessage = {
      role: 'user',
      content: query,
      timestamp: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await chatAPI.sendMessage(query, sessionId, activeTools)

      // Add AI response
      const aiMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        toolResults: response.tool_results,
      }
      setMessages((prev) => [...prev, aiMessage])

      // Update session ID if new
      if (response.session_id !== sessionId) {
        setSessionId(response.session_id)
        localStorage.setItem('sessionId', response.session_id)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.message}`,
        timestamp: new Date().toISOString(),
        isError: true,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const loadHistory = useCallback(async () => {
    try {
      const response = await chatAPI.getHistory(sessionId)
      if (response.success && response.history) {
        setMessages(response.history)
      }
    } catch (error) {
      console.error('Error loading history:', error)
    }
  }, [sessionId])

  const clearSession = useCallback(async () => {
    try {
      await chatAPI.clearSession(sessionId)
      setMessages([])
      const newSessionId = `session_${Date.now()}`
      setSessionId(newSessionId)
      localStorage.setItem('sessionId', newSessionId)
    } catch (error) {
      console.error('Error clearing session:', error)
    }
  }, [sessionId])

  const loadSessions = useCallback(async () => {
    try {
      const response = await chatAPI.listSessions()
      if (response.success) {
        setSessions(response.sessions)
      }
    } catch (error) {
      console.error('Error loading sessions:', error)
    }
  }, [])

  const value = {
    messages,
    sessionId,
    isLoading,
    sessions,
    sendMessage,
    loadHistory,
    clearSession,
    loadSessions,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}
