import cv2
import numpy as np
import random

def chromatic_aberration(frame, intensity=3):
    """RGB split effect"""
    h, w = frame.shape[:2]
    b, g, r = cv2.split(frame)
    
    # Shift channels
    b_shifted = np.roll(b, intensity, axis=1)
    r_shifted = np.roll(r, -intensity, axis=1)
    
    return cv2.merge([b_shifted, g, r_shifted])

def glitch_distortion(frame, intensity=5):
    """Digital glitch effect"""
    h, w = frame.shape[:2]
    glitched = frame.copy()
    
    # Random horizontal slices
    for _ in range(5):
        y = random.randint(0, h - 10)
        height = random.randint(5, 20)
        offset = random.randint(-intensity, intensity)
        if 0 <= y + height < h and 0 <= offset < w:
            glitched[y:y+height, :] = np.roll(glitched[y:y+height, :], offset, axis=1)
    
    return glitched

def ripple_pulse(frame, center, radius, intensity=20):
    """Ripple pulse effect from center point"""
    h, w = frame.shape[:2]
    result = frame.copy()
    
    # Create ripple mask
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    mask = np.sin(dist / 10.0) * intensity
    mask = np.clip(mask, -intensity, intensity)
    
    # Apply ripple
    for c in range(3):
        result[:, :, c] = np.clip(result[:, :, c].astype(np.float32) + mask, 0, 255).astype(np.uint8)
    
    return result

def vhs_noise(frame, intensity=10):
    """VHS tape noise effect"""
    h, w = frame.shape[:2]
    noise = np.random.randint(-intensity, intensity, (h, w, 3), dtype=np.int16)
    noisy = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Scan lines
    for y in range(0, h, 4):
        noisy[y:y+1, :] = noisy[y:y+1, :] // 2
    
    return noisy

def apply_shader_effects(frame, effects_config):
    """Apply all shader effects based on config"""
    result = frame.copy()
    
    if effects_config.get('chromatic_aberration', False):
        result = chromatic_aberration(result, effects_config.get('chromatic_intensity', 3))
    
    if effects_config.get('glitch', False):
        result = glitch_distortion(result, effects_config.get('glitch_intensity', 5))
    
    if effects_config.get('vhs_noise', False):
        result = vhs_noise(result, effects_config.get('vhs_intensity', 10))
    
    return result

