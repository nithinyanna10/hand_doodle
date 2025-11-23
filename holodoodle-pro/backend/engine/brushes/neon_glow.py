import cv2
import numpy as np

def neon_glow_brush(canvas, x1, y1, x2, y2, t):
    """Neon glow with HDR-like bloom effect"""
    # Animated colors
    color1 = (int(255 * t), int(80 + 175 * t), 255)
    color2 = (255, int(255 * t), int(255 * (1 - t)))
    
    # Convert RGB to BGR
    color1_bgr = (int(color1[2]), int(color1[1]), int(color1[0]))
    color2_bgr = (int(color2[2]), int(color2[1]), int(color2[0]))
    
    # Triple-layer glow
    cv2.line(canvas, (x1, y1), (x2, y2), color1_bgr, 12)  # Core
    cv2.line(canvas, (x1, y1), (x2, y2), color2_bgr, 8)   # Mid
    cv2.line(canvas, (x1, y1), (x2, y2), (255, 255, 255), 4)  # Outer glow
    
    # Apply bloom effect
    glow = cv2.GaussianBlur(canvas, (21, 21), 10)
    canvas[:] = cv2.addWeighted(canvas, 1.0, glow, 0.4, 0)

