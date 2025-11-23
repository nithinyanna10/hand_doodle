import numpy as np
import cv2
import random

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.size = float(size)
        self.lifetime = float(lifetime)
        self.age = 0.0
    
    def update(self, gravity=0.2, friction=0.98):
        self.x += self.vx
        self.y += self.vy
        self.vy += gravity
        self.vx *= friction
        self.vy *= friction
        self.age += 1.0
        self.size = max(0, self.size - 0.1)
    
    def is_alive(self, width, height):
        return (self.age < self.lifetime and 
                self.size > 0 and 
                0 <= self.x < width and 
                0 <= self.y < height)
    
    def draw(self, canvas):
        if self.size > 0:
            alpha = 1.0 - (self.age / self.lifetime)
            color = tuple(int(c * alpha) for c in self.color)
            cv2.circle(canvas, (int(self.x), int(self.y)), int(self.size), color, -1)

class ParticleSystem:
    def __init__(self, max_particles=500):
        self.particles = []
        self.max_particles = max_particles
    
    def spawn_explosion(self, x, y, color, count=20):
        """Spawn explosion particles"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(2, 8)
            vx = np.cos(angle) * speed
            vy = np.sin(angle) * speed
            size = random.uniform(3, 8)
            lifetime = random.uniform(30, 60)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))
    
    def spawn_trail(self, x, y, color, count=3):
        """Spawn trail particles"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            size = random.uniform(2, 4)
            lifetime = random.uniform(10, 20)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))
    
    def update(self, canvas):
        """Update and draw all particles"""
        h, w = canvas.shape[:2]
        alive_particles = []
        for p in self.particles:
            p.update()
            if p.is_alive(w, h):
                p.draw(canvas)
                alive_particles.append(p)
        self.particles = alive_particles
    
    def clear(self):
        self.particles.clear()

