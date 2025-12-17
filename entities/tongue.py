import pygame
import math
import random


class Tongue:
    """Frog's tongue that extends and retracts with realistic curves and visuals."""
    
    def __init__(self):
        self.color = (255, 100, 100)
        self.tip_color = (200, 50, 50)
        self.active = False
        self.length = 0
        self.max_length = 850
        self.extend_speed = 12
        self.retract_speed = 20
        self.width = 24
        self.dx = 0
        self.dy = 0
        self.retracting = False
        self.frog_center = (0, 0)
        
        # Curve mechanics
        self.has_curve = False
        self.curve_intensity = 0
        self.curve_direction = 1  # 1 for right, -1 for left
        self.curve_start_length = 0
        self.curve_decay = 0.95
        
        # Visual effects
        self.sticky_particles = []
        self.extension_wobble = 0
        
        # Caught mosquito
        self.has_caught_mosquito = False
        self.caught_mosquito_offset = (0, 0)  # Offset from tongue tip
        
    def shoot(self, frog_center, target_center):
        """Start shooting tongue towards target with possible curve."""
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
        
        # 65% chance to curve during extension for variety
        self.has_curve = random.random() < 0.67
        if self.has_curve:
            self.curve_intensity = random.uniform(0.2, 0.5)
            self.curve_direction = random.choice([-1, 1])
            self.curve_start_length = random.randint(50, 250)
            # Add random variation to make trajectories unpredictable
            self.dx += random.uniform(-0.15, 0.15)
            self.dy += random.uniform(-0.15, 0.15)
            # Renormalize direction
            mag = math.hypot(self.dx, self.dy)
            if mag > 0:
                self.dx /= mag
                self.dy /= mag
        else:
            self.curve_intensity = 0
        
        self.sticky_particles = []
        self.extension_wobble = 0
    
    def update(self):
        """Update tongue extension/retraction with curve mechanics."""
        if not self.active:
            return
            
        if not self.retracting:
            self.length += self.extend_speed
            self.extension_wobble = math.sin(self.length * 0.1) * 2
            
            # Apply curve decay as tongue extends
            if self.has_curve and self.length > self.curve_start_length:
                self.curve_intensity *= self.curve_decay
            
            if self.length >= self.max_length:
                self.retracting = True
        else:
            self.length -= self.retract_speed
            self.extension_wobble *= 0.9
            if self.length <= 0:
                self.active = False
                self.length = 0
                self.sticky_particles = []
    
    def get_curve_points(self, num_segments=20):
        """Calculate curved path points for the tongue."""
        points = []
        segment_length = self.length / num_segments
        
        for i in range(num_segments + 1):
            t = i / num_segments
            current_length = self.length * t
            
            # Calculate curve offset
            curve_offset = 0
            if self.has_curve and current_length > self.curve_start_length:
                # Smooth curve using sine wave
                curve_progress = (current_length - self.curve_start_length) / (self.length - self.curve_start_length + 1)
                curve_offset = math.sin(curve_progress * math.pi) * self.curve_intensity * current_length * self.curve_direction
            
            # Base position along straight line
            base_x = self.frog_center[0] + self.dx * current_length
            base_y = self.frog_center[1] + self.dy * current_length
            
            # Perpendicular direction for curve
            perp_dx = -self.dy
            perp_dy = self.dx
            
            # Apply curve offset perpendicular to tongue direction
            x = base_x + perp_dx * curve_offset + random.uniform(-self.extension_wobble, self.extension_wobble)
            y = base_y + perp_dy * curve_offset + random.uniform(-self.extension_wobble, self.extension_wobble)
            
            points.append((int(x), int(y)))
        
        return points
    
    def get_end_point(self):
        """Get current end position of tongue (with curve if active)."""
        if self.has_curve and self.length > self.curve_start_length:
            points = self.get_curve_points(20)
            return points[-1]
        else:
            end_x = self.frog_center[0] + self.dx * self.length
            end_y = self.frog_center[1] + self.dy * self.length
            return (end_x, end_y)
    
    def get_caught_mosquito_position(self):
        """Get position of caught mosquito (at tongue tip)."""
        if self.has_caught_mosquito:
            tip_pos = self.get_end_point()
            return (tip_pos[0] + self.caught_mosquito_offset[0],
                    tip_pos[1] + self.caught_mosquito_offset[1])
        return None
    
    def is_mosquito_eaten(self):
        """Check if mosquito has been pulled into mouth."""
        return self.has_caught_mosquito and self.length <= 5
    
    def check_collision(self, mosquito_center, mosquito_radius):
        """Check if tongue hits mosquito using curved path."""
        if not self.active:
            return False
        
        # Get all points along the curved path
        points = self.get_curve_points(30)
        
        # Check collision with each segment
        for i in range(len(points) - 1):
            distance = self._point_line_distance(
                mosquito_center[0], mosquito_center[1],
                points[i][0], points[i][1],
                points[i+1][0], points[i+1][1]
            )
            if distance < (self.width / 2 + mosquito_radius):
                # Catch the mosquito and start retracting
                self.has_caught_mosquito = True
                self.retracting = True
                
                # Calculate offset from current tongue tip
                tip_pos = self.get_end_point()
                self.caught_mosquito_offset = (mosquito_center[0] - tip_pos[0], 
                                               mosquito_center[1] - tip_pos[1])
                
                # Add sticky particle effect at hit point
                for _ in range(5):
                    self.sticky_particles.append({
                        'pos': (mosquito_center[0] + random.randint(-10, 10),
                               mosquito_center[1] + random.randint(-10, 10)),
                        'life': 20
                    })
                return True
        
        return False
    
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
        """Draw tongue with realistic curve and visuals."""
        if self.active:
            points = self.get_curve_points(25)
            
            # Draw tongue shadow/outline for depth
            if len(points) > 1:
                shadow_points = [(p[0] + 2, p[1] + 2) for p in points]
                pygame.draw.lines(screen, (100, 40, 40), False, shadow_points, self.width + 4)
            
            # Draw main tongue body with gradient effect
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Gradient from base to tip
                    progress = i / (len(points) - 1)
                    segment_color = (
                        int(self.color[0] - progress * 55),
                        int(self.color[1] - progress * 50),
                        int(self.color[2] - progress * 50)
                    )
                    
                    # Taper width from base to tip
                    segment_width = int(self.width * (1.0 - progress * 0.3))
                    
                    pygame.draw.line(screen, segment_color, points[i], points[i+1], segment_width)
                
                # Draw sticky tip
                tip_pos = points[-1]
                pygame.draw.circle(screen, self.tip_color, tip_pos, self.width // 2 + 2)
                pygame.draw.circle(screen, (255, 150, 150), tip_pos, self.width // 3)
                
                # Draw mouth connection point
                mouth_offset_y = 15  # Tongue comes from lower part of frog
                mouth_pos = (int(self.frog_center[0]), int(self.frog_center[1] + mouth_offset_y))
                pygame.draw.circle(screen, (220, 80, 80), mouth_pos, self.width // 2)
        
        # Draw sticky particles
        for particle in self.sticky_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.sticky_particles.remove(particle)
            else:
                alpha = int((particle['life'] / 20) * 255)
                particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, (255, 200, 200, alpha), (3, 3), 3)
                screen.blit(particle_surface, particle['pos'])
