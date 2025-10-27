import { Menu, X, Settings, Zap, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

const Header = ({ onToggleMCPPanel }) => {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="relative px-8 py-6 border-b border-purple-500/20"
    >
      {/* Gradient Glow Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-900/20 via-violet-900/20 to-purple-900/20 backdrop-blur-xl" />
      <div className="absolute inset-0 bg-gradient-to-b from-purple-600/5 to-transparent animate-pulse" />
      
      <div className="relative flex items-center justify-between">
        {/* Left: Logo & Title with Gradient */}
        <div className="flex items-center gap-4">
          <motion.div
            whileHover={{ scale: 1.1, rotate: 360 }}
            transition={{ duration: 0.6 }}
            className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#6b46c1] via-[#9f7aea] to-[#6b46c1] flex items-center justify-center neon-glow"
          >
            <Sparkles className="w-8 h-8 text-white" />
          </motion.div>
          <div>
            <h1 className="text-3xl font-bold gradient-text tracking-tight">
              AI-MCP Orchestrator
            </h1>
            <p className="text-sm text-purple-300/80 flex items-center gap-2 mt-1">
              <Zap className="w-4 h-4" />
              Powered by Gemini 2.0 Flash
            </p>
          </div>
        </div>

        {/* Right: MCP Tools Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onToggleMCPPanel}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-[#6b46c1] to-[#9f7aea] hover:from-[#7c3aed] hover:to-[#a78bfa] transition-all duration-300 text-white font-semibold shadow-lg neon-glow"
        >
          <span className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            MCP Tools
          </span>
        </motion.button>
      </div>
    </motion.header>
  )
}

export default Header
