import { motion } from 'framer-motion'

const gestures = [
  { emoji: '✌️', action: 'Next Brush' },
  { emoji: '👍', action: 'Toggle Glow' },
  { emoji: '👌', action: 'Start/Stop Drawing' },
  { emoji: '✊', action: 'Clear Canvas' },
  { emoji: '🤘', action: 'Glitch Mode' }
]

export function GestureGuide() {
  return (
    <motion.div
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '16px',
        background: 'rgba(0,0,0,0.4)',
        backdropFilter: 'blur(20px)',
        padding: '16px 24px',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.1)'
      }}
    >
      {gestures.map((gesture, index) => (
        <motion.div
          key={index}
          whileHover={{ scale: 1.1 }}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            minWidth: '80px'
          }}
        >
          <span style={{ fontSize: '32px' }}>{gesture.emoji}</span>
          <span style={{ color: '#fff', fontSize: '12px', textAlign: 'center' }}>
            {gesture.action}
          </span>
        </motion.div>
      ))}
    </motion.div>
  )
}

