import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Loader2, User, Bot } from 'lucide-react'
import { useChat } from '../context/ChatContext'
import { useMCP } from '../context/MCPContext'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

// Streaming Text Component
const StreamingText = ({ text, isComplete }) => {
  const [displayedText, setDisplayedText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    if (isComplete) {
      setDisplayedText(text)
      return
    }

    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(text.slice(0, currentIndex + 1))
        setCurrentIndex(currentIndex + 1)
      }, 20) // Adjust speed here (lower = faster)

      return () => clearTimeout(timeout)
    }
  }, [text, currentIndex, isComplete])

  return (
    <div className="prose prose-invert max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {displayedText}
      </ReactMarkdown>
      {!isComplete && currentIndex < text.length && (
        <motion.span
          animate={{ opacity: [1, 0, 1] }}
          transition={{ duration: 0.8, repeat: Infinity }}
          className="inline-block w-2 h-4 bg-purple-400 ml-1"
        />
      )}
    </div>
  )
}

const ChatBox = () => {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)
  const { messages, isLoading, sendMessage } = useChat()
  const { activeTools } = useMCP()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    
    await sendMessage(input, activeTools)
    setInput('')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <motion.div
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="w-20 h-20 bg-gradient-to-br from-ai-purple to-ai-blue rounded-2xl mx-auto mb-4 flex items-center justify-center"
              >
                <Bot className="w-10 h-10 text-white" />
              </motion.div>
              <h2 className="text-2xl font-bold mb-2">Welcome to AI-MCP Orchestrator</h2>
              <p className="text-gray-400 max-w-md mx-auto">
                Start a conversation with your AI assistant. I can help you with web searches, 
                file management, database queries, and much more using 10+ integrated MCP tools.
              </p>
              <div className="mt-6 flex flex-wrap gap-2 justify-center">
                <span className="px-3 py-1 bg-ai-purple/20 border border-ai-purple/30 rounded-full text-xs">
                  {activeTools.length} tools active
                </span>
                <span className="px-3 py-1 bg-ai-blue/20 border border-ai-blue/30 rounded-full text-xs">
                  Gemini 2.0 Flash
                </span>
              </div>
            </div>
          </div>
        ) : (
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex gap-3 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 bg-gradient-to-br from-ai-purple to-ai-blue rounded-lg flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                )}

                <div
                  className={`max-w-2xl ${
                    message.role === 'user' ? 'message-user' : 'message-ai'
                  }`}
                >
                  {message.role === 'assistant' ? (
                    <StreamingText 
                      text={message.content} 
                      isComplete={index < messages.length - 1 || !isLoading}
                    />
                  ) : (
                    <div className="prose prose-invert max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  )}

                  {message.toolResults && (
                    <div className="mt-3 pt-3 border-t border-white/10">
                      <p className="text-xs text-gray-400 mb-2">Tool Results:</p>
                      <div className="space-y-1">
                        {Object.entries(message.toolResults).map(([tool, result]) => (
                          <div
                            key={tool}
                            className="text-xs bg-white/5 rounded px-2 py-1"
                          >
                            <span className="text-ai-purple font-medium">{tool}:</span>{' '}
                            <span className="text-gray-300">
                              {result.success ? '✓ Success' : '✗ Failed'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="text-xs text-gray-500 mt-2">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>

                {message.role === 'user' && (
                  <div className="w-8 h-8 bg-ai-purple/30 rounded-lg flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-white" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
        )}

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-3"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-ai-purple to-ai-blue rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="message-ai">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm text-gray-400">AI is thinking...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-white/10 glass-effect">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything... (Shift+Enter for new line)"
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 resize-none focus:outline-none focus:border-ai-purple/50 transition-colors"
            rows="2"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-6 bg-ai-purple hover:bg-ai-purple/80 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-xl transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>

        {activeTools.length > 0 && (
          <div className="mt-3 flex items-center gap-2 text-xs text-gray-400">
            <span>Active tools:</span>
            <div className="flex gap-1 flex-wrap">
              {activeTools.map((tool) => (
                <span
                  key={tool}
                  className="px-2 py-0.5 bg-ai-green/20 border border-ai-green/30 rounded text-ai-green"
                >
                  {tool}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatBox
