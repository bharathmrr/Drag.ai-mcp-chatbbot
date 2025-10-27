import { motion } from 'framer-motion'
import { Settings, Info, Zap, CheckCircle } from 'lucide-react'
import { useMCP } from '../context/MCPContext'
import {
  Search, FileText, Database, Mail, Cloud, Brain,
  BarChart, BookOpen, Link, CloudRain, BookMarked,
  Code, Monitor, Activity, Calculator, Languages, Wrench
} from 'lucide-react'

const iconMap = {
  web_search: Search,
  file_manager: FileText,
  database: Database,
  email: Mail,
  drive: Cloud,
  automation: Wrench,
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

const toolDetails = {
  web_search: {
    usage: 'Search the web using DuckDuckGo',
    features: ['Real-time search', 'Web scraping', 'URL extraction'],
    example: '"Search for latest AI news"'
  },
  file_manager: {
    usage: 'Read, write, and manage files',
    features: ['Create files', 'Read content', 'Delete files', 'List directories'],
    example: '"Create a file called notes.txt"'
  },
  database: {
    usage: 'Query and manage MongoDB database',
    features: ['CRUD operations', 'Queries', 'Aggregations'],
    example: '"Find all users in database"'
  },
  email: {
    usage: 'Send emails via SMTP',
    features: ['Send emails', 'Attachments', 'Templates'],
    example: '"Send an email to team@example.com"'
  },
  climate: {
    usage: 'Get weather forecasts and climate data',
    features: ['Current weather', 'Forecasts', 'Climate info'],
    example: '"What\'s the weather in Tokyo?"'
  },
  wikipedia: {
    usage: 'Search Wikipedia and get summaries',
    features: ['Article search', 'Summaries', 'Full content'],
    example: '"Tell me about quantum computing"'
  },
  calculator: {
    usage: 'Perform mathematical calculations',
    features: ['Basic math', 'Complex equations', 'Unit conversion'],
    example: '"Calculate 25 * 4 + 10"'
  },
  system_monitor: {
    usage: 'Monitor system performance',
    features: ['CPU usage', 'Memory stats', 'Disk info', 'Network'],
    example: '"Show me my CPU usage"'
  },
  translator: {
    usage: 'Translate text between languages',
    features: ['12+ languages', 'Auto-detect', 'Bidirectional'],
    example: '"Translate \'Hello\' to Spanish"'
  },
  python_code: {
    usage: 'Execute Python code safely',
    features: ['Code execution', 'Syntax validation', 'Output capture'],
    example: '"Run: print(\'Hello World\')"'
  }
}

const SettingsPanel = () => {
  const { tools } = useMCP()

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
            <Settings className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold gradient-text">MCP Tools Information</h2>
            <p className="text-sm text-gray-400">Detailed usage and capabilities</p>
          </div>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 gap-4">
        {tools.map((tool, index) => {
          const Icon = iconMap[tool.name] || Zap
          const details = toolDetails[tool.name] || {
            usage: tool.description,
            features: ['Available'],
            example: 'Ask me to use this tool'
          }

          return (
            <motion.div
              key={tool.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass-panel p-6 hover:border-purple-500/40 transition-all"
            >
              {/* Tool Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    tool.enabled 
                      ? 'bg-gradient-to-br from-green-500/30 to-emerald-500/30' 
                      : 'bg-gray-700/30'
                  }`}>
                    <Icon className={`w-6 h-6 ${tool.enabled ? 'text-green-400' : 'text-gray-500'}`} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white capitalize">
                      {tool.name.replace(/_/g, ' ')}
                    </h3>
                    <p className="text-xs text-gray-400">{details.usage}</p>
                  </div>
                </div>
                {tool.enabled && (
                  <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-green-500/20 border border-green-500/30">
                    <CheckCircle className="w-3 h-3 text-green-400" />
                    <span className="text-xs text-green-400 font-medium">Active</span>
                  </div>
                )}
              </div>

              {/* Features */}
              <div className="mb-3">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="w-4 h-4 text-purple-400" />
                  <span className="text-sm font-medium text-purple-300">Features:</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {details.features.map((feature, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-xs text-gray-300"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>

              {/* Example Usage */}
              <div className="mt-4 p-3 rounded-lg bg-blue-500/10 border border-blue-500/20">
                <div className="flex items-center gap-2 mb-1">
                  <Info className="w-4 h-4 text-blue-400" />
                  <span className="text-xs font-medium text-blue-300">Example:</span>
                </div>
                <p className="text-sm text-gray-300 italic">{details.example}</p>
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}

export default SettingsPanel
