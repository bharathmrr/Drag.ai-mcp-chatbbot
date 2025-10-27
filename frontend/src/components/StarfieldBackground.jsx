import { useEffect, useRef } from 'react'

const StarfieldBackground = () => {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const stars = []
    const shootingStars = []
    const starCount = 200

    class Star {
      constructor() {
        this.x = Math.random() * canvas.width
        this.y = Math.random() * canvas.height
        this.size = Math.random() * 2 + 0.5
        this.speedX = Math.random() * 0.3 - 0.15
        this.speedY = Math.random() * 0.3 - 0.15
        this.opacity = Math.random() * 0.8 + 0.2
        this.twinkleSpeed = Math.random() * 0.02 + 0.01
        this.twinkleDirection = 1
      }

      update() {
        this.x += this.speedX
        this.y += this.speedY

        // Twinkling effect
        this.opacity += this.twinkleSpeed * this.twinkleDirection
        if (this.opacity >= 1 || this.opacity <= 0.2) {
          this.twinkleDirection *= -1
        }

        // Wrap around screen
        if (this.x > canvas.width) this.x = 0
        if (this.x < 0) this.x = canvas.width
        if (this.y > canvas.height) this.y = 0
        if (this.y < 0) this.y = canvas.height
      }

      draw() {
        // Draw star with glow effect
        ctx.shadowBlur = 10
        ctx.shadowColor = `rgba(139, 92, 246, ${this.opacity})`
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
        ctx.shadowBlur = 0
      }
    }

    class ShootingStar {
      constructor() {
        this.reset()
      }

      reset() {
        this.x = Math.random() * canvas.width
        this.y = Math.random() * canvas.height * 0.5
        this.length = Math.random() * 80 + 40
        this.speed = Math.random() * 10 + 15
        this.opacity = 1
        this.angle = Math.PI / 4 // 45 degrees
      }

      update() {
        this.x += Math.cos(this.angle) * this.speed
        this.y += Math.sin(this.angle) * this.speed
        this.opacity -= 0.01

        if (this.opacity <= 0 || this.x > canvas.width || this.y > canvas.height) {
          this.reset()
        }
      }

      draw() {
        ctx.save()
        ctx.translate(this.x, this.y)
        ctx.rotate(this.angle)
        
        const gradient = ctx.createLinearGradient(0, 0, this.length, 0)
        gradient.addColorStop(0, `rgba(255, 255, 255, ${this.opacity})`)
        gradient.addColorStop(1, `rgba(139, 92, 246, 0)`)
        
        ctx.strokeStyle = gradient
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.moveTo(0, 0)
        ctx.lineTo(this.length, 0)
        ctx.stroke()
        ctx.restore()
      }
    }

    // Create stars
    for (let i = 0; i < starCount; i++) {
      stars.push(new Star())
    }

    // Create shooting stars
    for (let i = 0; i < 3; i++) {
      shootingStars.push(new ShootingStar())
    }

    const animate = () => {
      // Create gradient background
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
      gradient.addColorStop(0, '#0a0a0f')
      gradient.addColorStop(0.5, '#1a1a2e')
      gradient.addColorStop(1, '#16213e')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw and update stars
      stars.forEach((star) => {
        star.update()
        star.draw()
      })

      // Draw and update shooting stars
      shootingStars.forEach((star) => {
        star.update()
        star.draw()
      })

      requestAnimationFrame(animate)
    }

    animate()

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ background: 'transparent' }}
    />
  )
}

export default StarfieldBackground
