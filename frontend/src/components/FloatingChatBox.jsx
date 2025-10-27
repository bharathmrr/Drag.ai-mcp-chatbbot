import { motion } from 'framer-motion'
import { Send, Sparkles } from 'lucide-react'
import { useState } from 'react'

const FloatingChatBox = ({ onSendMessage }) => {
  const [message, setMessage] = useState('')
  const [isFocused, setIsFocused] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim()) {
      onSendMessage(message)
      setMessage('')
    }
  }

  return (
    <motion.div
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.5, type: 'spring' }}
      className="fixed bottom-8 left-1/2 transform -translate-x-1/2 w-full max-w-3xl px-4 z-50"
    >
      <form onSubmit={handleSubmit} className="relative">
        {/* Glow effect */}
        <div className={`absolute inset-0 rounded-2xl transition-all duration-300 ${
          isFocused ? 'neon-glow' : ''
        }`} />
        
        {/* Input container */}
        <div className="relative glass-panel p-2 flex items-center gap-3">
          {/* Icon */}
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#6b46c1] to-[#9f7aea] flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-6 h-6 text-white" />
          </div>

          {/* Input */}
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask me anything..."
            className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-lg px-4 py-3 box-border"
            style={{
              lineHeight: '1.5',
              verticalAlign: 'middle',
              height: '48px'
            }}
          />

          {/* Send button */}
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!message.trim()}
            className={`
              w-12 h-12 rounded-xl flex items-center justify-center
              transition-all duration-300
              ${message.trim()
                ? 'bg-gradient-to-br from-[#6b46c1] to-[#9f7aea] neon-glow cursor-pointer'
                : 'bg-gray-700/50 cursor-not-allowed'
              }
            `}
          >
            <Send className={`w-5 h-5 ${message.trim() ? 'text-white' : 'text-gray-500'}`} />
          </motion.button>
        </div>
      </form>
    </motion.div>
  )
}

export default FloatingChatBox
