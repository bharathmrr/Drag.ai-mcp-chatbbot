import { useState } from 'react'
import Header from './components/Header'
import FuturisticSidebar from './components/FuturisticSidebar'
import WelcomeCard from './components/WelcomeCard'
import MCPPanel from './components/MCPPanel'
import StarfieldBackground from './components/StarfieldBackground'
import ChatBox from './components/ChatBox'
import LogsPanel from './components/LogsPanel'
import SettingsPanel from './components/SettingsPanel'
import { ChatProvider } from './context/ChatContext'
import { MCPProvider } from './context/MCPContext'

function App() {
  const [mcpPanelOpen, setMcpPanelOpen] = useState(true)
  const [currentView, setCurrentView] = useState('home')

  const handleNavigation = (viewId) => {
    setCurrentView(viewId)
  }

  return (
    <ChatProvider>
      <MCPProvider>
        <div className="min-h-screen bg-[#0b0b1f] relative overflow-hidden">
          {/* Animated Starfield Background */}
          <StarfieldBackground />
          
          {/* Main Layout */}
          <div className="relative z-10 flex flex-col h-screen">
            {/* Header */}
            <Header 
              onToggleMCPPanel={() => setMcpPanelOpen(!mcpPanelOpen)}
            />
            
            {/* Main Content */}
            <div className="flex flex-1 overflow-hidden">
              {/* Futuristic Sidebar */}
              <FuturisticSidebar onNavigate={handleNavigation} />
              
              {/* Main Panel */}
              <div className="flex-1 flex flex-col p-8 overflow-y-auto custom-scrollbar">
                {currentView === 'home' && <WelcomeCard />}
                {currentView === 'sessions' && <ChatBox />}
                {currentView === 'tools' && <SettingsPanel />}
                {currentView === 'logs' && <LogsPanel />}
                {currentView === 'settings' && <SettingsPanel />}
              </div>
              
              {/* MCP Panel */}
              {mcpPanelOpen && (
                <MCPPanel />
              )}
            </div>
          </div>
        </div>
      </MCPProvider>
    </ChatProvider>
  )
}

export default App
