import pygame
import math
import random


class Mosquito:
    """Player-controlled mosquito that must avoid the frog's tongue."""
    
    def __init__(self, x, y, size=70):
        self.size = size
        self.color = (200, 50, 50)
        self.rect = pygame.Rect(x, y, size, size)
        self.image = None
        
        # Physics-based movement
        self.vx = 0  # Velocity X
        self.vy = 0  # Velocity Y
        self.acceleration = 0.8  # How fast it speeds up
        self.friction = 0.92  # Air resistance (0.92 = slow down by 8% per frame)
        self.max_speed = 7  # Maximum velocity
        
        # Realistic flying wobble
        self.wobble_timer = 0
        self.wobble_offset_x = 0
        self.wobble_offset_y = 0
        
    def set_image(self, image):
        """Set sprite image for mosquito."""
        self.image = image
        
    def handle_input(self, keys):
        """Handle WASD movement with realistic physics."""
        # Input direction
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        
        # Normalize diagonal movement so speed is consistent
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2) ≈ 0.707
            dy *= 0.707
        
        # Apply acceleration
        self.vx += dx * self.acceleration
        self.vy += dy * self.acceleration
        
        # Limit to max speed
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed
        
        # Apply friction (air resistance)
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Stop if moving very slowly
        if abs(self.vx) < 0.1:
            self.vx = 0
        if abs(self.vy) < 0.1:
            self.vy = 0
        
        # Update wobble for realistic flying motion
        self.wobble_timer += 0.15
        self.wobble_offset_x = math.sin(self.wobble_timer) * 0.5
        self.wobble_offset_y = math.cos(self.wobble_timer * 1.3) * 0.3
        
        # Apply velocity to position
        self.rect.x += self.vx + self.wobble_offset_x
        self.rect.y += self.vy + self.wobble_offset_y
    
    def clamp_to_area(self, play_area):
        """Keep mosquito within playable bounds."""
        self.rect.clamp_ip(play_area)
    
    def draw(self, screen):
        """Draw mosquito to screen."""
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
    
    @property
    def centerx(self):
        return self.rect.centerx
    
    @property
    def centery(self):
        return self.rect.centery
