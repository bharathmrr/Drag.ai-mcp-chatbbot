import { motion } from 'framer-motion'
import { MessageSquare, Plus, Trash2, Clock } from 'lucide-react'
import { useChat } from '../context/ChatContext'
import { useEffect } from 'react'

const Sidebar = () => {
  const { sessions, loadSessions, clearSession, sessionId } = useChat()

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  return (
    <motion.aside
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      className="w-80 glass-effect border-r border-white/10 flex flex-col"
    >
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <button className="w-full px-4 py-3 bg-ai-purple hover:bg-ai-purple/80 rounded-xl transition-colors flex items-center justify-center gap-2 font-medium">
          <Plus className="w-5 h-5" />
          New Chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        <div className="flex items-center gap-2 text-sm text-gray-400 mb-3">
          <Clock className="w-4 h-4" />
          <span>Recent Sessions</span>
        </div>

        {sessions.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No chat history yet</p>
          </div>
        ) : (
          sessions.map((session) => (
            <motion.div
              key={session.session_id}
              whileHover={{ scale: 1.02 }}
              className={`p-3 rounded-lg cursor-pointer transition-colors ${
                session.session_id === sessionId
                  ? 'bg-ai-purple/20 border border-ai-purple/30'
                  : 'bg-white/5 hover:bg-white/10'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <MessageSquare className="w-4 h-4 text-ai-purple" />
                    <span className="text-sm font-medium truncate">
                      Session {session.session_id.slice(-8)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400">
                    {session.message_count} messages
                  </p>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-white/10">
        <button
          onClick={clearSession}
          className="w-full px-4 py-2 bg-ai-red/20 hover:bg-ai-red/30 border border-ai-red/30 rounded-lg transition-colors flex items-center justify-center gap-2 text-sm"
        >
          <Trash2 className="w-4 h-4" />
          Clear Current Session
        </button>
      </div>
    </motion.aside>
  )
}

export default Sidebar
