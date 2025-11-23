import cv2
import numpy as np
import random

def lightning_brush(canvas, x1, y1, x2, y2, t):
    """Electric lightning bolts with branches"""
    # Electric blue/cyan colors
    color = (255, int(200 + 55 * t), int(100 + 155 * t))
    color_bgr = (int(color[2]), int(color[1]), int(color[0]))
    
    # Main bolt
    cv2.line(canvas, (x1, y1), (x2, y2), color_bgr, 6)
    
    # Branches
    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if dist > 10:
        for _ in range(3):
            branch_t = random.uniform(0.3, 0.7)
            bx = int(x1 + (x2 - x1) * branch_t)
            by = int(y1 + (y2 - y1) * branch_t)
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            cv2.line(canvas, (bx, by), (bx + offset_x, by + offset_y), color_bgr, 3)
    
    # Sparks on fast movement
    if dist > 30:
        for _ in range(5):
            spark_x = x2 + random.randint(-10, 10)
            spark_y = y2 + random.randint(-10, 10)
            cv2.circle(canvas, (spark_x, spark_y), 2, (255, 255, 255), -1)

