import { motion } from 'framer-motion'
import { Home, MessageSquare, Wrench, FileText, Settings, LogOut } from 'lucide-react'
import { useState } from 'react'

const FuturisticSidebar = ({ onNavigate }) => {
  const [activeItem, setActiveItem] = useState('home')

  const menuItems = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'sessions', icon: MessageSquare, label: 'Sessions' },
    { id: 'tools', icon: Wrench, label: 'Tools' },
    { id: 'logs', icon: FileText, label: 'Logs' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ]

  const handleClick = (itemId) => {
    setActiveItem(itemId)
    if (onNavigate) {
      onNavigate(itemId)
    }
  }

  return (
    <motion.aside
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="w-20 glass-panel border-r border-purple-500/20 flex flex-col items-center py-8 gap-6"
    >
      {/* Menu Items */}
      <div className="flex flex-col gap-4">
        {menuItems.map((item, index) => {
          const Icon = item.icon
          const isActive = activeItem === item.id
          
          return (
            <motion.button
              key={item.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleClick(item.id)}
              className={`
                relative w-14 h-14 rounded-2xl flex items-center justify-center
                transition-all duration-300 group
                ${isActive 
                  ? 'bg-gradient-to-br from-[#6b46c1] to-[#9f7aea] neon-glow' 
                  : 'bg-[#1a1a2e]/50 hover:bg-[#1a1a2e] border border-purple-500/20'
                }
              `}
              title={item.label}
            >
              {/* Neon hover effect */}
              {!isActive && (
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-purple-500/0 to-blue-500/0 group-hover:from-purple-500/20 group-hover:to-blue-500/20 transition-all duration-300" />
              )}
              
              <Icon className={`w-6 h-6 relative z-10 ${isActive ? 'text-white' : 'text-purple-300'}`} />
              
              {/* Active indicator */}
              {isActive && (
                <motion.div
                  layoutId="activeIndicator"
                  className="absolute -right-1 w-1 h-8 bg-gradient-to-b from-purple-400 to-violet-500 rounded-full"
                />
              )}
            </motion.button>
          )
        })}
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Logout Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        className="w-14 h-14 rounded-2xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 flex items-center justify-center transition-all duration-300 group"
        title="Logout"
      >
        <LogOut className="w-6 h-6 text-red-400 group-hover:text-red-300" />
      </motion.button>
    </motion.aside>
  )
}

export default FuturisticSidebar
