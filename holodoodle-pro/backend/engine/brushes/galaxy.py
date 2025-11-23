import cv2
import numpy as np
import random

def galaxy_brush(canvas, x1, y1, x2, y2, t):
    """Galaxy brush with stars and nebula trails"""
    # Cosmic colors (purple, blue, pink)
    nebula1 = (int(255 * (0.5 + 0.5 * t)), int(100 + 155 * t), 255)
    nebula2 = (255, int(150 * t), int(200 + 55 * t))
    star_color = (255, 255, 255)
    
    # Convert to BGR
    nebula1_bgr = (int(nebula1[2]), int(nebula1[1]), int(nebula1[0]))
    nebula2_bgr = (int(nebula2[2]), int(nebula2[1]), int(nebula2[0]))
    
    # Nebula trail
    cv2.line(canvas, (x1, y1), (x2, y2), nebula1_bgr, 10)
    cv2.line(canvas, (x1, y1), (x2, y2), nebula2_bgr, 6)
    
    # Stars (glowing dots)
    for _ in range(8):
        star_x = x2 + random.randint(-20, 20)
        star_y = y2 + random.randint(-20, 20)
        size = random.randint(1, 3)
        cv2.circle(canvas, (star_x, star_y), size, star_color, -1)
        cv2.circle(canvas, (star_x, star_y), size + 2, star_color, 1)

