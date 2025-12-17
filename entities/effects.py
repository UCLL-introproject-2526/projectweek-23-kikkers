import pygame
import random
import math


class Particle:
    """Single particle for effects."""
    
    def __init__(self, x, y, color, vx=None, vy=None, lifetime=60, size=3, gravity=0):
        self.x = x
        self.y = y
        self.vx = vx if vx is not None else random.uniform(-2, 2)
        self.vy = vy if vy is not None else random.uniform(-3, -1)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = gravity
        
    def update(self):
        """Update particle position."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        
    def is_alive(self):
        """Check if particle should still be drawn."""
        return self.lifetime > 0
    
    def draw(self, screen):
        """Draw particle with fading alpha."""
        if self.is_alive():
            alpha = int((self.lifetime / self.max_lifetime) * 255)
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, alpha), 
                             (self.size, self.size), self.size)
            screen.blit(particle_surface, (self.x - self.size, self.y - self.size))


class ParticleSystem:
    """Manages multiple particle effects."""
    
    def __init__(self):
        self.particles = []
        
    def add_explosion(self, x, y, color=(255, 200, 100), count=20):
        """Create explosion effect."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.randint(2, 5)
            lifetime = random.randint(30, 60)
            self.particles.append(Particle(x, y, color, vx, vy, lifetime, size, 0.1))
    
    def add_trail(self, x, y, color=(100, 200, 255), count=5):
        """Create trail effect."""
        for _ in range(count):
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0.5)
            self.particles.append(Particle(x, y, color, vx, vy, 20, 2, 0))
    
    def add_sparkle(self, x, y, color=(255, 255, 100)):
        """Create sparkle effect."""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, color, vx, vy, 40, 3, 0))
    
    def add_collect_effect(self, x, y, color=(0, 255, 150)):
        """Effect when collecting items."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2  # Upward bias
            self.particles.append(Particle(x, y, color, vx, vy, 45, 4, 0.15))
    
    def update(self):
        """Update all particles."""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(screen)


class ScorePopup:
    """Floating score indicator."""
    
    def __init__(self, x, y, text, color=(255, 255, 255), size=32):
        self.x = x
        self.y = y
        self.start_y = y
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", size, bold=True)
        self.lifetime = 90  # 1.5 seconds
        self.max_lifetime = 90
        
    def update(self):
        """Update popup animation."""
        self.lifetime -= 1
        # Float upward
        progress = 1 - (self.lifetime / self.max_lifetime)
        self.y = self.start_y - (progress * 60)
    
    def is_alive(self):
        """Check if popup should still be shown."""
        return self.lifetime > 0
    
    def draw(self, screen):
        """Draw score popup with fade."""
        if self.is_alive():
            alpha = int((self.lifetime / self.max_lifetime) * 255)
            # Render text
            text_surface = self.font.render(self.text, True, self.color)
            
            # Create surface with alpha
            popup_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            popup_surface.fill((0, 0, 0, 0))
            
            # Draw outline
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                outline = self.font.render(self.text, True, (0, 0, 0))
                outline.set_alpha(alpha)
                popup_surface.blit(outline, (dx, dy))
            
            # Draw main text
            text_surface.set_alpha(alpha)
            popup_surface.blit(text_surface, (0, 0))
            
            screen.blit(popup_surface, (self.x - text_surface.get_width() // 2, self.y))


class ScreenShake:
    """Camera shake effect."""
    
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        
    def start(self, amount=10, duration=15):
        """Start screen shake."""
        self.shake_amount = amount
        self.shake_duration = duration
    
    def update(self):
        """Update shake effect."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            if self.shake_duration == 0:
                self.shake_amount = 0
    
    def get_offset(self):
        """Get current shake offset."""
        if self.shake_duration > 0:
            x = random.randint(-self.shake_amount, self.shake_amount)
            y = random.randint(-self.shake_amount, self.shake_amount)
            return (x, y)
        return (0, 0)


class ComboSystem:
    """Manages combo multipliers and streaks."""
    
    def __init__(self):
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 3000  # 3 seconds to maintain combo
        self.multiplier = 1.0
        self.total_score = 0
        self.score_popups = []
        
    def add_catch(self, x, y, base_points=1):
        """Add a catch to the combo."""
        self.combo_count += 1
        self.combo_timer = self.combo_timeout
        
        # Calculate multiplier (caps at 10x)
        self.multiplier = min(1.0 + (self.combo_count - 1) * 0.5, 10.0)
        
        # Calculate points
        points = int(base_points * self.multiplier)
        self.total_score += points
        
        # Create popup
        if self.combo_count > 1:
            text = f"+{points} x{self.multiplier:.1f}"
            color = self._get_combo_color()
        else:
            text = f"+{points}"
            color = (255, 255, 255)
        
        self.score_popups.append(ScorePopup(x, y, text, color))
        
        return points
    
    def update(self, delta_time):
        """Update combo timer and popups."""
        if self.combo_count > 0:
            self.combo_timer -= delta_time
            if self.combo_timer <= 0:
                self.combo_count = 0
                self.multiplier = 1.0
        
        # Update popups
        for popup in self.score_popups[:]:
            popup.update()
            if not popup.is_alive():
                self.score_popups.remove(popup)
    
    def _get_combo_color(self):
        """Get color based on combo level."""
        if self.multiplier >= 8:
            return (255, 50, 255)  # Purple - insane!
        elif self.multiplier >= 5:
            return (255, 100, 100)  # Red - great!
        elif self.multiplier >= 3:
            return (255, 200, 0)  # Orange - good!
        else:
            return (100, 255, 100)  # Green - nice!
    
    def draw(self, screen):
        """Draw combo popups."""
        for popup in self.score_popups:
            popup.draw(screen)
    
    def get_combo_text(self):
        """Get combo display text."""
        if self.combo_count > 1:
            return f"{self.combo_count} COMBO! x{self.multiplier:.1f}"
        return ""
