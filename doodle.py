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

# -------------------------
# Brush Effects
# -------------------------
def neon_brush(img, x1, y1, x2, y2):
    cv2.line(img, (x1, y1), (x2, y2), (255, 20, 147), 8)   # pink neon
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)    # soft glow

def sparkle_brush(img, x, y):
    for _ in range(10):
        rx = x + np.random.randint(-10, 10)
        ry = y + np.random.randint(-10, 10)
        cv2.circle(img, (rx, ry), 2, (255, 255, 255), -1)

def fire_brush(img, x1, y1, x2, y2):
    cv2.line(img, (x1, y1), (x2, y2), (0, 140, 255), 12)   # orange core
    cv2.line(img, (x1, y1), (x2, y2), (0, 50, 255), 4)     # red outside

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
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        h, w, _ = frame.shape

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

        prev_x, prev_y = x, y

        # Draw skeleton on screen
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Mix canvas with webcam
    blended = cv2.addWeighted(frame, 0.5, canvas, 1, 0)

    # Show mode name
    cv2.putText(blended, f"Brush: {brush_mode.upper()}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Hand Doodle Camera", blended)

    # -------------------------
    # Keyboard controls
    # -------------------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord('m'):   # switch brush
        mode_i = (mode_i + 1) % len(MODES)
        brush_mode = MODES[mode_i]
    if key == ord('c'):   # clear
        canvas = np.zeros_like(frame)
        prev_x, prev_y = None, None
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

