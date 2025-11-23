import { useEffect, useRef, useState } from 'react'

export function useWebSocket(url) {
  const [frame, setFrame] = useState(null)
  const [brush, setBrush] = useState('neon')
  const [drawing, setDrawing] = useState(true)
  const [glow, setGlow] = useState(false)
  const [glitch, setGlitch] = useState(false)
  const [fps, setFps] = useState(0)
  const wsRef = useRef(null)
  const frameCountRef = useRef(0)
  const lastFpsTimeRef = useRef(Date.now())

  useEffect(() => {
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'frame') {
        setFrame(data.data)
        setBrush(data.brush)
        setDrawing(data.drawing)
        setGlow(data.glow)
        setGlitch(data.glitch)
        
        // Calculate FPS
        frameCountRef.current++
        const now = Date.now()
        if (now - lastFpsTimeRef.current >= 1000) {
          setFps(frameCountRef.current)
          frameCountRef.current = 0
          lastFpsTimeRef.current = now
        }
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    return () => {
      ws.close()
    }
  }, [url])

  return { frame, brush, drawing, glow, glitch, fps }
}

