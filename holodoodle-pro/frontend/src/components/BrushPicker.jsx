import { motion } from 'framer-motion'
import { Sparkles, Zap, Flame, Sparkles as Galaxy, Orbit } from 'lucide-react'

const brushes = [
  { name: 'neon', icon: Sparkles, color: '#ff00ff' },
  { name: 'lightning', icon: Zap, color: '#00ffff' },
  { name: 'fire', icon: Flame, color: '#ff6600' },
  { name: 'galaxy', icon: Galaxy, color: '#9d4edd' },
  { name: 'energy', icon: Orbit, color: '#00ff00' }
]

export function BrushPicker({ currentBrush, onBrushChange }) {
  return (
    <div style={{
      display: 'flex',
      gap: '12px',
      padding: '20px',
      background: 'rgba(0,0,0,0.3)',
      borderRadius: '16px',
      backdropFilter: 'blur(10px)'
    }}>
      {brushes.map((brush, index) => {
        const Icon = brush.icon
        const isActive = brush.name === currentBrush
        
        return (
          <motion.button
            key={brush.name}
            onClick={() => onBrushChange(index)}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '12px',
              border: isActive ? `3px solid ${brush.color}` : '3px solid transparent',
              background: isActive ? `rgba(255,255,255,0.2)` : 'rgba(255,255,255,0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.3s'
            }}
          >
            <Icon 
              size={28} 
              color={isActive ? brush.color : '#ffffff'} 
            />
          </motion.button>
        )
      })}
    </div>
  )
}

