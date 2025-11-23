import { useState } from 'react'
import { motion } from 'framer-motion'
import { VideoCanvas } from './components/VideoCanvas'
import { BrushPicker } from './components/BrushPicker'
import { ControlPanel } from './components/ControlPanel'
import { GestureGuide } from './components/GestureGuide'
import { useWebSocket } from './hooks/useWebSocket'

function App() {
  const { frame, brush, drawing, glow, glitch, fps } = useWebSocket('ws://localhost:8000/ws')
  const [particleIntensity, setParticleIntensity] = useState(1.0)

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      {/* Main Video Display */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        style={{
          width: '80%',
          maxWidth: '1200px',
          aspectRatio: '16/9',
          position: 'relative',
          background: 'rgba(0,0,0,0.3)',
          borderRadius: '20px',
          padding: '20px',
          backdropFilter: 'blur(10px)'
        }}
      >
        {frame ? (
          <VideoCanvas frame={frame} />
        ) : (
          <div style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontSize: '18px'
          }}>
            Connecting to camera...
          </div>
        )}
      </motion.div>

      {/* Brush Picker */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '50%',
        transform: 'translateX(-50%)'
      }}>
        <BrushPicker currentBrush={brush} />
      </div>

      {/* Control Panel */}
      <ControlPanel
        drawing={drawing}
        glow={glow}
        glitch={glitch}
        particleIntensity={particleIntensity}
        onDrawingChange={() => {}}
        onGlowChange={() => {}}
        onGlitchChange={() => {}}
        onParticleIntensityChange={setParticleIntensity}
        fps={fps}
      />

      {/* Gesture Guide */}
      <GestureGuide />

      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          color: '#fff',
          fontSize: '32px',
          fontWeight: 'bold',
          textShadow: '0 2px 20px rgba(0,0,0,0.5)'
        }}
      >
        HoloDoodle Pro
      </motion.h1>
    </div>
  )
}

export default App

