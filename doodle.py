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

# Particle system (limited for performance)
particles = []
MAX_PARTICLES = 100  # Limit particle count

# Cached effects (computed once)
vignette_mask = None
gradient_bg = None

# -------------------------
# UPGRADE 1: Optimized Neon Bloom Effect
# -------------------------
def apply_bloom(canvas):
    # Smaller, faster blur
    glow = cv2.GaussianBlur(canvas, (15, 15), 8)
    return cv2.addWeighted(canvas, 1.0, glow, 0.5, 0)

# -------------------------
# UPGRADE 2: Optimized Particle System
# -------------------------
def spawn_particles(x, y, color):
    # Spawn fewer particles
    if len(particles) < MAX_PARTICLES:
        for _ in range(5):  # Reduced from 10
            particles.append([
                float(x),
                float(y),
                np.random.uniform(-2, 2),
                np.random.uniform(-2, 2),
                color,
                float(np.random.randint(3, 7))  # size
            ])

def update_particles(canvas):
    dead = []
    for i, p in enumerate(particles):
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.15  # gravity
        p[5] -= 0.15  # shrink
        
        if p[5] <= 0 or p[0] < 0 or p[0] >= canvas.shape[1] or p[1] < 0 or p[1] >= canvas.shape[0]:
            dead.append(i)
            continue
        
        cv2.circle(canvas, (int(p[0]), int(p[1])), int(p[5]), p[4], -1)
    
    for i in reversed(dead):
        particles.pop(i)

# -------------------------
# UPGRADE 3: Optimized Cyberpunk Color Cycling
# -------------------------
def get_animated_colors():
    t = (cv2.getTickCount() % 10000) / 10000
    color1 = (int(255*t), int(80 + 175*t), 255)
    color2 = (255, int(255*t), int(255*(1-t)))
    return color1, color2

# -------------------------
# UPGRADE 4: Pre-computed Background Gradient + Vignette
# -------------------------
def init_gradient_bg(h, w):
    """Pre-compute gradient background once"""
    bg = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        c = int(20 + 40 * (y / h))
        bg[y, :] = (c, c, c + 30)
    return bg

def init_vignette(h, w):
    """Pre-compute vignette mask once"""
    mask = np.ones((h, w), np.uint8) * 255
    mask = cv2.GaussianBlur(mask, (301, 301), 150)  # Smaller, faster
    mask = mask.astype(np.float32) / 255.0
    mask = 1.0 - (mask * 0.2)  # Subtle vignette
    return np.stack([mask] * 3, axis=2)

# -------------------------
# Enhanced Brush Effects with Animated Colors
# -------------------------
def neon_brush(img, x1, y1, x2, y2):
    color1, color2 = get_animated_colors()
    # Convert RGB to BGR for OpenCV
    color1_bgr = (int(color1[2]), int(color1[1]), int(color1[0]))
    color2_bgr = (int(color2[2]), int(color2[1]), int(color2[0]))
    cv2.line(img, (x1, y1), (x2, y2), color1_bgr, 8)   # animated neon
    cv2.line(img, (x1, y1), (x2, y2), color2_bgr, 2)    # soft glow

def sparkle_brush(img, x, y):
    color1, color2 = get_animated_colors()
    sparkle_color = (
        int((color1[0] + color2[0]) / 2),
        int((color1[1] + color2[1]) / 2),
        int((color1[2] + color2[2]) / 2)
    )
    for _ in range(8):  # Slightly reduced
        rx = x + np.random.randint(-10, 10)
        ry = y + np.random.randint(-10, 10)
        cv2.circle(img, (rx, ry), 2, sparkle_color, -1)

def fire_brush(img, x1, y1, x2, y2):
    # Fire colors (orange-red spectrum) - cached calculation
    t = (cv2.getTickCount() % 10000) / 10000
    fire_core = (0, int(140 + 115 * t), 255)
    fire_outside = (0, int(50 + 50 * t), 255)
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

frame_initialized = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Initialize canvas and cached effects once
    if canvas is None:
        canvas = np.zeros_like(frame, dtype=np.uint8)
    
    # Initialize cached effects once
    if not frame_initialized:
        gradient_bg = init_gradient_bg(h, w)
        vignette_mask = init_vignette(h, w)
        frame_initialized = True

    # UPGRADE 5: Lighter Motion Blur (faster)
    canvas = (canvas * 0.92).astype(np.uint8)  # Less fade = faster

    # UPGRADE 4: Apply pre-computed gradient background
    frame = cv2.addWeighted(frame, 0.4, gradient_bg, 0.6, 0)

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
            
            # UPGRADE 2: Spawn particles (only if under limit)
            if len(particles) < MAX_PARTICLES:
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
    if particles:
        update_particles(canvas)

    # UPGRADE 1: Apply bloom effect (optimized)
    canvas = apply_bloom(canvas)

    # Mix canvas with webcam
    blended = cv2.addWeighted(frame, 0.5, canvas, 1, 0)

    # UPGRADE 4: Apply pre-computed vignette (fast)
    blended = (blended.astype(np.float32) * vignette_mask).astype(np.uint8)

    # Show mode name with style
    cv2.putText(blended, f"Brush: {brush_mode.upper()}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Hand Doodle Camera - CYBERPUNK EDITION", blended)

    # -------------------------
    # Keyboard controls
    # -------------------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord('m'):   # switch brush
        mode_i = (mode_i + 1) % len(MODES)
        brush_mode = MODES[mode_i]
    if key == ord('c'):   # clear
        canvas = np.zeros_like(frame, dtype=np.uint8)
        particles.clear()
        prev_x, prev_y = None, None
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
