import cv2
import numpy as np

def energy_whirl_brush(canvas, x1, y1, x2, y2, t, frame):
    """Energy whirl with distortion and ripple field"""
    # Energy colors (green/cyan)
    energy_color = (int(100 + 155 * t), 255, int(200 + 55 * t))
    energy_bgr = (int(energy_color[2]), int(energy_color[1]), int(energy_color[0]))
    
    # Main energy line
    cv2.line(canvas, (x1, y1), (x2, y2), energy_bgr, 10)
    
    # Ripple effect around finger
    center = (x2, y2)
    for radius in range(20, 60, 10):
        alpha = 1.0 - (radius / 60.0)
        color = tuple(int(c * alpha) for c in energy_bgr)
        cv2.circle(frame, center, radius, color, 2)
    
    # Distortion lines (warp effect)
    for angle in range(0, 360, 45):
        rad = np.radians(angle)
        end_x = int(x2 + 30 * np.cos(rad))
        end_y = int(y2 + 30 * np.sin(rad))
        cv2.line(canvas, (x2, y2), (end_x, end_y), energy_bgr, 2)

