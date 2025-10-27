import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { mcpAPI } from '../utils/api'

const MCPContext = createContext()

export const useMCP = () => {
  const context = useContext(MCPContext)
  if (!context) {
    throw new Error('useMCP must be used within MCPProvider')
  }
  return context
}

export const MCPProvider = ({ children }) => {
  const [tools, setTools] = useState([])
  const [activeTools, setActiveTools] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const loadTools = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await mcpAPI.listTools()
      if (response.success) {
        setTools(response.tools)
        // Update active tools
        const active = response.tools
          .filter((tool) => tool.enabled)
          .map((tool) => tool.name)
        setActiveTools(active)
      }
    } catch (error) {
      console.error('Error loading tools:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const toggleTool = useCallback(async (toolName) => {
    try {
      const tool = tools.find((t) => t.name === toolName)
      if (!tool) return

      const newEnabled = !tool.enabled
      const response = await mcpAPI.toggleTool(toolName, newEnabled)

      if (response.success) {
        // Update local state
        setTools((prev) =>
          prev.map((t) =>
            t.name === toolName ? { ...t, enabled: newEnabled } : t
          )
        )

        // Update active tools
        if (newEnabled) {
          setActiveTools((prev) => [...prev, toolName])
        } else {
          setActiveTools((prev) => prev.filter((name) => name !== toolName))
        }
      }
    } catch (error) {
      console.error('Error toggling tool:', error)
    }
  }, [tools])

  const executeTool = useCallback(async (toolName, action, params = {}) => {
    try {
      const response = await mcpAPI.executeTool(toolName, action, params)
      return response
    } catch (error) {
      console.error('Error executing tool:', error)
      return { success: false, error: error.message }
    }
  }, [])

  useEffect(() => {
    loadTools()
  }, [loadTools])

  const value = {
    tools,
    activeTools,
    isLoading,
    loadTools,
    toggleTool,
    executeTool,
  }

  return <MCPContext.Provider value={value}>{children}</MCPContext.Provider>
}
