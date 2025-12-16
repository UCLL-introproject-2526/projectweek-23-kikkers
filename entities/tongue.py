import pygame
import math


class Tongue:
    """Frog's tongue that extends and retracts to catch the mosquito."""
    
    def __init__(self):
        self.color = (255, 100, 100)
        self.active = False
        self.length = 0
        self.max_length = 800
        self.extend_speed = 14
        self.retract_speed = 23
        self.width = 30
        self.dx = 0
        self.dy = 0
        self.retracting = False
        self.frog_center = (0, 0)
        
    def shoot(self, frog_center, target_center):
        """Start shooting tongue towards target."""
        self.active = True
        self.length = 0
        self.retracting = False
        self.frog_center = frog_center
        
        dx = target_center[0] - frog_center[0]
        dy = target_center[1] - frog_center[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.dx = dx / dist
        self.dy = dy / dist
    
    def update(self):
        """Update tongue extension/retraction."""
        if not self.active:
            return
            
        if not self.retracting:
            self.length += self.extend_speed
            if self.length >= self.max_length:
                self.retracting = True
        else:
            self.length -= self.retract_speed
            if self.length <= 0:
                self.active = False
                self.length = 0
    
    def get_end_point(self):
        """Get current end position of tongue."""
        end_x = self.frog_center[0] + self.dx * self.length
        end_y = self.frog_center[1] + self.dy * self.length
        return (end_x, end_y)
    
    def check_collision(self, mosquito_center, mosquito_radius):
        """Check if tongue hits mosquito using point-line distance."""
        if not self.active:
            return False
            
        end_x, end_y = self.get_end_point()
        distance = self._point_line_distance(
            mosquito_center[0], mosquito_center[1],
            self.frog_center[0], self.frog_center[1],
            end_x, end_y
        )
        return distance < (self.width / 2 + mosquito_radius)
    
    def _point_line_distance(self, px, py, x1, y1, x2, y2):
        """Calculate distance from point to line segment."""
        line_mag = math.hypot(x2 - x1, y2 - y1)
        if line_mag == 0:
            return math.hypot(px - x1, py - y1)
        u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
        u = max(min(u, 1), 0)
        closest_x = x1 + u * (x2 - x1)
        closest_y = y1 + u * (y2 - y1)
        return math.hypot(px - closest_x, py - closest_y)
    
    def draw(self, screen):
        """Draw tongue line."""
        if self.active:
            end_x, end_y = self.get_end_point()
            pygame.draw.line(
                screen, self.color,
                self.frog_center, (end_x, end_y),
                self.width
            )
