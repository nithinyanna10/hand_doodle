import { useEffect, useRef } from 'react'

export function VideoCanvas({ frame }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (frame && canvasRef.current) {
      const img = new Image()
      img.onload = () => {
        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img, 0, 0)
      }
      img.src = `data:image/jpeg;base64,${frame}`
    }
  }, [frame])

  return (
    <canvas
      ref={canvasRef}
      style={{
        width: '100%',
        height: '100%',
        objectFit: 'contain',
        borderRadius: '12px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
      }}
    />
  )
}

