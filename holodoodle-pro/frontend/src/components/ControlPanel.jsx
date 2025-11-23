import { motion } from 'framer-motion'

export function ControlPanel({ 
  drawing, 
  glow, 
  glitch, 
  particleIntensity, 
  onDrawingChange,
  onGlowChange,
  onGlitchChange,
  onParticleIntensityChange,
  fps 
}) {
  return (
    <motion.div
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      style={{
        position: 'absolute',
        left: '20px',
        top: '50%',
        transform: 'translateY(-50%)',
        background: 'rgba(0,0,0,0.4)',
        backdropFilter: 'blur(20px)',
        padding: '24px',
        borderRadius: '20px',
        minWidth: '280px',
        border: '1px solid rgba(255,255,255,0.1)'
      }}
    >
      <h3 style={{ color: '#fff', marginBottom: '20px', fontSize: '18px' }}>
        Controls
      </h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <Toggle
          label="Drawing"
          enabled={drawing}
          onChange={onDrawingChange}
        />
        
        <Toggle
          label="Glow Mode"
          enabled={glow}
          onChange={onGlowChange}
        />
        
        <Toggle
          label="Glitch Mode"
          enabled={glitch}
          onChange={onGlitchChange}
        />
        
        <Slider
          label="Particle Intensity"
          value={particleIntensity}
          onChange={onParticleIntensityChange}
          min={0}
          max={2}
          step={0.1}
        />
        
        <div style={{ 
          marginTop: '10px', 
          padding: '12px', 
          background: 'rgba(255,255,255,0.1)', 
          borderRadius: '8px' 
        }}>
          <div style={{ color: '#fff', fontSize: '14px' }}>
            FPS: <span style={{ color: '#00ff00', fontWeight: 'bold' }}>{fps}</span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

function Toggle({ label, enabled, onChange }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ color: '#fff', fontSize: '14px' }}>{label}</span>
      <button
        onClick={onChange}
        style={{
          width: '48px',
          height: '24px',
          borderRadius: '12px',
          background: enabled ? '#00ff00' : '#666',
          border: 'none',
          cursor: 'pointer',
          position: 'relative',
          transition: 'all 0.3s'
        }}
      >
        <motion.div
          animate={{ x: enabled ? 24 : 2 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          style={{
            width: '20px',
            height: '20px',
            borderRadius: '50%',
            background: '#fff',
            position: 'absolute',
            top: '2px'
          }}
        />
      </button>
    </div>
  )
}

function Slider({ label, value, onChange, min, max, step }) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ color: '#fff', fontSize: '14px' }}>{label}</span>
        <span style={{ color: '#00ff00', fontSize: '14px', fontWeight: 'bold' }}>
          {value.toFixed(1)}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{
          width: '100%',
          height: '6px',
          borderRadius: '3px',
          background: 'rgba(255,255,255,0.2)',
          outline: 'none'
        }}
      />
    </div>
  )
}

