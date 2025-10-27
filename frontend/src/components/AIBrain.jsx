import { motion } from 'framer-motion'

const AIBrain = () => {
  const particles = Array.from({ length: 20 }, (_, i) => i)

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Gradient Orbs */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-ai-purple/30 rounded-full blur-3xl"
      />

      <motion.div
        animate={{
          scale: [1.2, 1, 1.2],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-ai-blue/30 rounded-full blur-3xl"
      />

      {/* Floating Particles */}
      {particles.map((i) => (
        <motion.div
          key={i}
          initial={{
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
          }}
          animate={{
            x: [
              Math.random() * window.innerWidth,
              Math.random() * window.innerWidth,
            ],
            y: [
              Math.random() * window.innerHeight,
              Math.random() * window.innerHeight,
            ],
          }}
          transition={{
            duration: 10 + Math.random() * 10,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "linear",
          }}
          className="absolute w-1 h-1 bg-ai-purple/50 rounded-full"
          style={{
            boxShadow: '0 0 10px rgba(139, 92, 246, 0.5)',
          }}
        />
      ))}

      {/* Grid Lines */}
      <div className="absolute inset-0 opacity-10">
        <div className="grid grid-cols-12 h-full">
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="border-r border-ai-purple/30" />
          ))}
        </div>
      </div>
    </div>
  )
}

export default AIBrain
