import cv2
import mediapipe as mp
import numpy as np
import math

# -------------------------
# Setup
# -------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Drawing canvas
canvas = None

# Brush modes
MODES = ["neon", "sparkle", "fire"]
mode_i = 0
brush_mode = MODES[mode_i]

# Smoothing
prev_x, prev_y = None, None

# Particle system
particles = []

# -------------------------
# UPGRADE 1: Neon Bloom Effect
# -------------------------
def apply_bloom(canvas):
    glow = cv2.GaussianBlur(canvas, (25, 25), 15)
    return cv2.addWeighted(canvas, 1.0, glow, 0.7, 0)

# -------------------------
# UPGRADE 2: Particle System
# -------------------------
def spawn_particles(x, y, color):
    for _ in range(10):
        particles.append([
            x,
            y,
            np.random.uniform(-3, 3),
            np.random.uniform(-3, 3),
            color,
            np.random.randint(5, 10)  # size
        ])

def update_particles(canvas):
    dead = []
    for i, p in enumerate(particles):
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.2  # gravity
        p[5] -= 0.2  # shrink
        
        if p[5] <= 0:
            dead.append(i)
            continue
        
        cv2.circle(canvas, (int(p[0]), int(p[1])), int(p[5]), p[4], -1)
    
    for i in reversed(dead):
        particles.pop(i)

# -------------------------
# UPGRADE 3: Cyberpunk Color Cycling
# -------------------------
def get_animated_colors():
    t = (cv2.getTickCount() % 10000) / 10000
    color1 = (int(255*t), int(80 + 175*t), 255)
    color2 = (255, int(255*t), int(255*(1-t)))
    return color1, color2

# -------------------------
# UPGRADE 4: Background Gradient + Vignette
# -------------------------
def gradient_bg(frame):
    h, w, _ = frame.shape
    bg = np.zeros_like(frame)
    for y in range(h):
        c = int(20 + 40 * (y / h))
        bg[y, :] = (c, c, c + 30)
    return bg

def apply_vignette(frame):
    h, w, _ = frame.shape
    mask = np.ones((h, w), np.uint8) * 255
    mask = cv2.GaussianBlur(mask, (451, 451), 200)
    mask = mask.astype(np.float32) / 255.0
    mask = 1.0 - (mask * 0.3)  # Subtle vignette
    mask = np.stack([mask] * 3, axis=2)
    frame = (frame.astype(np.float32) * mask).astype(np.uint8)
    return frame

# -------------------------
# Enhanced Brush Effects with Animated Colors
# -------------------------
def neon_brush(img, x1, y1, x2, y2):
    color1, color2 = get_animated_colors()
    # Convert RGB to BGR for OpenCV
    color1_bgr = (color1[2], color1[1], color1[0])
    color2_bgr = (color2[2], color2[1], color2[0])
    cv2.line(img, (x1, y1), (x2, y2), color1_bgr, 8)   # animated neon
    cv2.line(img, (x1, y1), (x2, y2), color2_bgr, 2)    # soft glow

def sparkle_brush(img, x, y):
    color1, color2 = get_animated_colors()
    for _ in range(10):
        rx = x + np.random.randint(-10, 10)
        ry = y + np.random.randint(-10, 10)
        # Use animated colors for sparkles
        sparkle_color = (
            int((color1[0] + color2[0]) / 2),
            int((color1[1] + color2[1]) / 2),
            int((color1[2] + color2[2]) / 2)
        )
        cv2.circle(img, (rx, ry), 2, sparkle_color, -1)

def fire_brush(img, x1, y1, x2, y2):
    color1, color2 = get_animated_colors()
    # Fire colors (orange-red spectrum)
    fire_core = (0, int(140 + 115 * ((cv2.getTickCount() % 10000) / 10000)), 255)
    fire_outside = (0, int(50 + 50 * ((cv2.getTickCount() % 10000) / 10000)), 255)
    cv2.line(img, (x1, y1), (x2, y2), fire_core, 12)   # animated orange core
    cv2.line(img, (x1, y1), (x2, y2), fire_outside, 4)     # animated red outside

# -------------------------
# Main App
# -------------------------
cap = cv2.VideoCapture(0)
print("\n🔥 Controls:")
print("Press 'm' to change brush (neon/sparkle/fire)")
print("Press 'c' to clear screen")
print("Press 'q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame, dtype=np.float32)

    # UPGRADE 5: Motion Blur
    canvas = (canvas * 0.88).astype(np.uint8)

    # UPGRADE 4: Apply gradient background to frame
    bg_frame = gradient_bg(frame)
    frame = cv2.addWeighted(frame, 0.3, bg_frame, 0.7, 0)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        # Index finger tip (landmark 8)
        x = int(hand.landmark[8].x * w)
        y = int(hand.landmark[8].y * h)

        if prev_x is not None:
            if brush_mode == "neon":
                neon_brush(canvas, prev_x, prev_y, x, y)
            elif brush_mode == "sparkle":
                sparkle_brush(canvas, x, y)
            elif brush_mode == "fire":
                fire_brush(canvas, prev_x, prev_y, x, y)
            
            # UPGRADE 2: Spawn particles
            color1, color2 = get_animated_colors()
            particle_color = (
                int((color1[0] + color2[0]) / 2),
                int((color1[1] + color2[1]) / 2),
                int((color1[2] + color2[2]) / 2)
            )
            spawn_particles(x, y, particle_color)

        prev_x, prev_y = x, y

        # Draw skeleton on screen
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # UPGRADE 2: Update particles
    update_particles(canvas)

    # UPGRADE 1: Apply bloom effect
    canvas = apply_bloom(canvas.astype(np.uint8))
    canvas = canvas.astype(np.float32)

    # Mix canvas with webcam
    blended = cv2.addWeighted(frame, 0.5, canvas.astype(np.uint8), 1, 0)

    # UPGRADE 4: Apply vignette
    blended = apply_vignette(blended)

    # Show mode name with style
    cv2.putText(blended, f"Brush: {brush_mode.upper()}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(blended, f"Particles: {len(particles)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Hand Doodle Camera - CYBERPUNK EDITION", blended)

    # -------------------------
    # Keyboard controls
    # -------------------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord('m'):   # switch brush
        mode_i = (mode_i + 1) % len(MODES)
        brush_mode = MODES[mode_i]
    if key == ord('c'):   # clear
        canvas = np.zeros_like(frame, dtype=np.float32)
        particles.clear()
        prev_x, prev_y = None, None
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
