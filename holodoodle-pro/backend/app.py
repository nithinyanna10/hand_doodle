import cv2
import numpy as np
import base64
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import mediapipe as mp

from engine.gesture import GestureRecognizer
from engine.utils import Canvas
from engine.particles import ParticleSystem
from engine.brushes import (
    neon_glow_brush, lightning_brush, fire_brush, 
    galaxy_brush, energy_whirl_brush
)
from engine.shaders import apply_shader_effects, ripple_pulse

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
BRUSHES = ["neon", "lightning", "fire", "galaxy", "energy"]
brush_index = 0
drawing_enabled = True
glow_mode = False
glitch_mode = False
particle_intensity = 1.0

def frame_to_base64(frame):
    """Convert frame to base64 string"""
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buffer).decode('utf-8')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    global brush_index, drawing_enabled, glow_mode, glitch_mode, particle_intensity
    
    # Initialize components
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    gesture_recognizer = GestureRecognizer()
    canvas = None
    particle_system = ParticleSystem(max_particles=300)
    
    prev_x, prev_y = None, None
    time_counter = 0
    last_gesture = None
    gesture_cooldown = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            
            if canvas is None:
                canvas = Canvas(h, w)
            
            # Fade canvas
            canvas.fade()
            
            # Get hand landmarks
            landmarks = gesture_recognizer.get_landmarks(frame)
            
            # Detect gesture
            gesture = None
            if landmarks and gesture_cooldown == 0:
                gesture = gesture_recognizer.detect_gesture(landmarks)
                if gesture and gesture != last_gesture:
                    # Handle gestures
                    if gesture == "peace":
                        brush_index = (brush_index + 1) % len(BRUSHES)
                        # Ripple effect on brush change
                        center = (w // 2, h // 2)
                        frame = ripple_pulse(frame, center, 50, 30)
                    elif gesture == "thumbs_up":
                        glow_mode = not glow_mode
                    elif gesture == "pinch":
                        drawing_enabled = not drawing_enabled
                    elif gesture == "fist":
                        canvas.clear()
                        particle_system.clear()
                    elif gesture == "rock":
                        glitch_mode = not glitch_mode
                    
                    last_gesture = gesture
                    gesture_cooldown = 15
            
            if gesture_cooldown > 0:
                gesture_cooldown -= 1
            
            # Drawing logic
            if landmarks and drawing_enabled:
                x, y = gesture_recognizer.get_finger_tip(landmarks, 8)
                if x and y:
                    x_pixel = int(x * w)
                    y_pixel = int(y * h)
                    
                    if prev_x is not None:
                        # Get time for animation
                        t = (time_counter % 1000) / 1000.0
                        
                        # Apply brush
                        brush_name = BRUSHES[brush_index]
                        canvas_img = canvas.get_canvas()
                        
                        if brush_name == "neon":
                            neon_glow_brush(canvas_img, prev_x, prev_y, x_pixel, y_pixel, t)
                        elif brush_name == "lightning":
                            lightning_brush(canvas_img, prev_x, prev_y, x_pixel, y_pixel, t)
                        elif brush_name == "fire":
                            fire_brush(canvas_img, prev_x, prev_y, x_pixel, y_pixel, t)
                        elif brush_name == "galaxy":
                            galaxy_brush(canvas_img, prev_x, prev_y, x_pixel, y_pixel, t)
                        elif brush_name == "energy":
                            energy_whirl_brush(canvas_img, prev_x, prev_y, x_pixel, y_pixel, t, frame)
                        
                        canvas.set_canvas(canvas_img)
                        
                        # Spawn particles
                        if particle_intensity > 0:
                            color = (255, int(200 + 55 * t), int(100 + 155 * t))
                            particle_system.spawn_trail(x_pixel, y_pixel, color, int(3 * particle_intensity))
                    
                    prev_x, prev_y = x_pixel, y_pixel
                    
                    # Draw hand skeleton
                    mp_drawing = mp.solutions.drawing_utils
                    mp_hands = mp.solutions.hands
                    mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            else:
                prev_x, prev_y = None, None
            
            # Update particles
            canvas_img = canvas.get_canvas()
            particle_system.update(canvas_img)
            canvas.set_canvas(canvas_img)
            
            # Blend canvas with frame
            blended = cv2.addWeighted(frame, 0.5, canvas.get_canvas(), 1.0, 0)
            
            # Apply shader effects
            shader_config = {
                'chromatic_aberration': glow_mode,
                'glitch': glitch_mode,
                'vhs_noise': glitch_mode,
                'chromatic_intensity': 3,
                'glitch_intensity': 5,
                'vhs_intensity': 10
            }
            blended = apply_shader_effects(blended, shader_config)
            
            # Add UI text
            cv2.putText(blended, f"Brush: {BRUSHES[brush_index].upper()}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(blended, f"Drawing: {'ON' if drawing_enabled else 'OFF'}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if drawing_enabled else (0, 0, 255), 2)
            
            # Send frame
            frame_b64 = frame_to_base64(blended)
            await websocket.send_json({
                "type": "frame",
                "data": frame_b64,
                "brush": BRUSHES[brush_index],
                "drawing": drawing_enabled,
                "glow": glow_mode,
                "glitch": glitch_mode
            })
            
            time_counter += 1
            await asyncio.sleep(0.03)  # ~30 FPS
            
    except WebSocketDisconnect:
        pass
    finally:
        cap.release()

@app.get("/")
async def root():
    return {"message": "HoloDoodle Pro API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

