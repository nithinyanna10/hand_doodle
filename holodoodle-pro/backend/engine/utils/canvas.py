import numpy as np
import cv2

class Canvas:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.motion_blur_factor = 0.92
    
    def fade(self):
        """Apply motion blur fade"""
        self.canvas = (self.canvas * self.motion_blur_factor).astype(np.uint8)
    
    def clear(self):
        """Clear the canvas"""
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def get_canvas(self):
        return self.canvas.copy()
    
    def set_canvas(self, canvas):
        self.canvas = canvas

