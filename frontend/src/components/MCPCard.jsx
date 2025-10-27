import { motion } from 'framer-motion'
import { useMCP } from '../context/MCPContext'
import {
  Search,
  FileText,
  Database,
  Mail,
  Cloud,
  Zap,
  Brain,
  BarChart,
  BookOpen,
  Link,
  CloudRain,
  BookMarked,
  Code,
  Monitor,
  Activity,
  Calculator,
  Languages,
} from 'lucide-react'

const iconMap = {
  web_search: Search,
  file_manager: FileText,
  database: Database,
  email: Mail,
  drive: Cloud,
  automation: Zap,
  memory: Brain,
  analytics: BarChart,
  knowledgebase: BookOpen,
  api_integration: Link,
  climate: CloudRain,
  wikipedia: BookMarked,
  python_code: Code,
  screen_monitor: Monitor,
  system_monitor: Activity,
  calculator: Calculator,
  translator: Languages,
}

const MCPCard = ({ tool }) => {
  const { toggleTool } = useMCP()
  const Icon = iconMap[tool.name] || Zap

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      whileHover={{ scale: 1.02 }}
      className={`relative overflow-hidden rounded-2xl p-4 transition-all duration-300 ${
        tool.enabled
          ? 'bg-gradient-to-br from-purple-500/15 to-blue-500/15 border border-purple-500/40'
          : 'bg-[#1a1a2e]/50 border border-purple-500/10 hover:border-purple-500/20'
      }`}
    >
      {/* Animated Background Gradient */}
      {tool.enabled && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-purple-600/10 via-blue-600/10 to-purple-600/10"
          animate={{
            x: ['-100%', '100%'],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: 'linear',
          }}
        />
      )}

      <div className="relative flex items-start justify-between">
        <div className="flex items-start gap-3 flex-1">
          {/* Icon with Glow Effect */}
          <motion.div
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.6 }}
            className={`w-12 h-12 rounded-xl flex items-center justify-center relative ${
              tool.enabled
                ? 'bg-gradient-to-br from-green-500/30 to-emerald-500/30 shadow-lg shadow-green-500/30'
                : 'bg-gray-800/50'
            }`}
          >
            {tool.enabled && (
              <div className="absolute inset-0 bg-green-500/20 rounded-xl animate-pulse" />
            )}
            <Icon
              className={`w-6 h-6 relative z-10 ${
                tool.enabled ? 'text-green-400' : 'text-gray-500'
              }`}
            />
          </motion.div>

          {/* Tool Info */}
          <div className="flex-1">
            <h3
              className={`font-semibold text-sm mb-1 capitalize ${
                tool.enabled
                  ? 'text-white'
                  : 'text-gray-400'
              }`}
            >
              {tool.name.replace(/_/g, ' ')}
            </h3>
            <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed">
              {tool.description}
            </p>
          </div>
        </div>

        {/* Toggle Switch */}
        <div className="flex-shrink-0 ml-3">
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => toggleTool(tool.name)}
            className={`
              relative w-14 h-7 rounded-full transition-all duration-300
              ${tool.enabled 
                ? 'bg-gradient-to-r from-green-500 to-emerald-500' 
                : 'bg-gray-700'
              }
            `}
          >
            {/* Toggle knob */}
            <motion.div
              animate={{
                x: tool.enabled ? 28 : 2,
              }}
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              className={`
                absolute top-1 w-5 h-5 rounded-full shadow-lg
                ${tool.enabled ? 'bg-white' : 'bg-gray-400'}
              `}
            />
            
            {/* Status indicator */}
            {tool.enabled && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-green-400 border-2 border-[#1a1a2e]"
              >
                <span className="absolute inset-0 rounded-full bg-green-400 animate-ping" />
              </motion.div>
            )}
          </motion.button>
          
          {/* Status text */}
          <div className="text-center mt-1">
            <span className={`text-[10px] font-semibold ${
              tool.enabled ? 'text-green-400' : 'text-gray-500'
            }`}>
              {tool.enabled ? '🟢 ON' : '🔴 OFF'}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default MCPCard
