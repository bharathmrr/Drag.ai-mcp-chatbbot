import { motion } from 'framer-motion'
import { MessageSquare, Clock, Sparkles } from 'lucide-react'

const LogsPanel = () => {
  // Mock chat sessions data
  const chatSessions = [
    {
      id: 1,
      title: 'Weather Query',
      preview: 'What\'s the weather in Tokyo?',
      timestamp: '2 hours ago',
      toolsUsed: ['climate', 'web_search'],
      messageCount: 5
    },
    {
      id: 2,
      title: 'Wikipedia Search',
      preview: 'Tell me about quantum computing',
      timestamp: '5 hours ago',
      toolsUsed: ['wikipedia'],
      messageCount: 3
    },
    {
      id: 3,
      title: 'System Monitoring',
      preview: 'Show me my CPU usage',
      timestamp: '1 day ago',
      toolsUsed: ['system_monitor'],
      messageCount: 2
    },
    {
      id: 4,
      title: 'Calculator',
      preview: 'Calculate 25 * 4 + 10',
      timestamp: '2 days ago',
      toolsUsed: ['calculator'],
      messageCount: 1
    },
    {
      id: 5,
      title: 'File Management',
      preview: 'Create a new file with data',
      timestamp: '3 days ago',
      toolsUsed: ['file_manager'],
      messageCount: 4
    }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full h-full"
    >
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#6b46c1] to-[#9f7aea] flex items-center justify-center neon-glow">
            <Clock className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold gradient-text">Chat History</h2>
            <p className="text-sm text-gray-400">Previous conversation sessions</p>
          </div>
        </div>
      </div>

      {/* Sessions List */}
      <div className="space-y-4">
        {chatSessions.map((session, index) => (
          <motion.div
            key={session.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02, x: 5 }}
            className="glass-panel p-5 cursor-pointer group"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start gap-3 flex-1">
                <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center flex-shrink-0 group-hover:bg-purple-500/30 transition-colors">
                  <MessageSquare className="w-5 h-5 text-purple-400" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-white mb-1">{session.title}</h3>
                  <p className="text-sm text-gray-400 line-clamp-1">{session.preview}</p>
                </div>
              </div>
              <div className="text-xs text-gray-500">{session.timestamp}</div>
            </div>

            {/* Tools Used */}
            <div className="flex items-center gap-2 flex-wrap mb-2">
              <span className="text-xs text-gray-500">Tools:</span>
              {session.toolsUsed.map((tool) => (
                <span
                  key={tool}
                  className="px-2 py-1 rounded-lg bg-purple-500/10 border border-purple-500/30 text-xs text-purple-300"
                >
                  {tool}
                </span>
              ))}
            </div>

            {/* Message Count */}
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <Sparkles className="w-3 h-3" />
              <span>{session.messageCount} messages</span>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}

export default LogsPanel
