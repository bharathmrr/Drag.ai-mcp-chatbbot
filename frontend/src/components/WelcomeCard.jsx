import { motion } from 'framer-motion'
import { Sparkles, Zap, Cpu } from 'lucide-react'

const WelcomeCard = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.2 }}
      className="glass-panel p-8 mb-6 relative overflow-hidden fade-in"
    >
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-violet-600/5 to-blue-600/10 animate-pulse" />
      
      <div className="relative">
        {/* Icon */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4, type: 'spring' }}
          className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#6b46c1] to-[#9f7aea] flex items-center justify-center mb-6 neon-glow"
        >
          <Sparkles className="w-8 h-8 text-white" />
        </motion.div>

        {/* Title */}
        <motion.h2
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="text-3xl font-bold gradient-text mb-4"
        >
          Welcome to AI-MCP Orchestrator
        </motion.h2>

        {/* Description */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-gray-300 text-lg leading-relaxed mb-6"
        >
          Your unified AI automation environment. Chat, execute, and orchestrate with 10+ integrated MCP tools.
        </motion.p>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="grid grid-cols-3 gap-4"
        >
          <div className="flex items-center gap-3 p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
            <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
              <Zap className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Fast</div>
              <div className="text-xs text-gray-400">Lightning speed</div>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
            <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Smart</div>
              <div className="text-xs text-gray-400">AI-powered</div>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 rounded-xl bg-violet-500/10 border border-violet-500/20">
            <div className="w-10 h-10 rounded-lg bg-violet-500/20 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-violet-400" />
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Powerful</div>
              <div className="text-xs text-gray-400">17+ tools</div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}

export default WelcomeCard
