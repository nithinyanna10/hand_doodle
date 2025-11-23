import cv2
import numpy as np

def fire_brush(canvas, x1, y1, x2, y2, t):
    """Fire brush with hot core and ember smoke"""
    # Fire gradient: orange -> red -> dark
    fire_core = (0, int(140 + 115 * t), 255)
    fire_mid = (0, int(50 + 50 * t), 255)
    fire_ash = (0, int(20 + 10 * t), 100)
    
    # Layered fire effect
    cv2.line(canvas, (x1, y1), (x2, y2), fire_core, 14)  # Hot core
    cv2.line(canvas, (x1, y1), (x2, y2), fire_mid, 8)   # Mid flame
    cv2.line(canvas, (x1, y1), (x2, y2), fire_ash, 4)   # Ash particles

