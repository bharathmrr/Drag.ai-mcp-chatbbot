import { motion, AnimatePresence } from 'framer-motion'
import { useMCP } from '../context/MCPContext'
import MCPCard from './MCPCard'
import { Loader2, Sparkles, Zap, Activity } from 'lucide-react'

const MCPPanel = () => {
  const { tools, isLoading } = useMCP()
  const activeCount = tools.filter(t => t.enabled).length

  return (
    <motion.aside
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="w-96 glass-panel border-l border-purple-500/20 flex flex-col shadow-2xl"
    >
      {/* Header with Gradient */}
      <div className="relative p-6 border-b border-purple-500/20 bg-gradient-to-r from-purple-900/20 to-blue-900/20">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/5 to-blue-600/5 animate-pulse" />
        <div className="relative">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <Sparkles className="w-5 h-5 text-purple-400" />
            </div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              MCP Tools
            </h2>
          </div>
          <p className="text-sm text-gray-400 ml-11">
            {tools.filter((t) => t.enabled).length} of {tools.length} tools active
          </p>
        </div>
      </div>

      {/* Tools Grid with Scroll */}
      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center h-full"
            >
              <Loader2 className="w-12 h-12 animate-spin text-purple-500 mb-4" />
              <p className="text-gray-400 text-sm">Loading tools...</p>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ staggerChildren: 0.05 }}
              className="grid grid-cols-1 gap-3"
            >
              {tools.map((tool, index) => (
                <motion.div
                  key={tool.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <MCPCard tool={tool} />
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Summary Stats */}
      <div className="p-6 border-t border-purple-500/20 bg-gradient-to-r from-purple-900/10 to-blue-900/10">
        <div className="grid grid-cols-2 gap-4">
          {/* Active Tools */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="relative overflow-hidden rounded-2xl p-5 group cursor-pointer"
            style={{
              background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%)',
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}
          >
            <div className="absolute inset-0 neon-glow-green opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <div className="relative">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-green-400" />
                <span className="text-xs font-medium text-green-300">Active Tools</span>
              </div>
              <div className="text-3xl font-bold text-green-400">{activeCount}</div>
            </div>
          </motion.div>
          
          {/* Total Tools */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="relative overflow-hidden rounded-2xl p-5 group cursor-pointer"
            style={{
              background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%)',
              border: '1px solid rgba(59, 130, 246, 0.3)'
            }}
          >
            <div className="absolute inset-0 neon-glow-blue opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <div className="relative">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-5 h-5 text-blue-400" />
                <span className="text-xs font-medium text-blue-300">Total Tools</span>
              </div>
              <div className="text-3xl font-bold text-blue-400">{tools.length}</div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.aside>
  )
}

export default MCPPanel
