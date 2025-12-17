import pygame
import random
import math


class PowerUp(pygame.sprite.Sprite):
    """Power-up items that spawn and provide temporary bonuses."""
    
    TYPES = {
        'speed': {'color': (100, 200, 255), 'duration': 5000, 'name': 'SPEED BOOST!'},
        'shield': {'color': (255, 215, 0), 'duration': 8000, 'name': 'SHIELD!'},
        'slow_motion': {'color': (200, 100, 255), 'duration': 6000, 'name': 'SLOW-MO!'},
        'magnet': {'color': (255, 100, 100), 'duration': 7000, 'name': 'MAGNET!'},
        'invincibility': {'color': (255, 255, 100), 'duration': 4000, 'name': 'INVINCIBLE!'},
        'double_points': {'color': (0, 255, 150), 'duration': 10000, 'name': '2X POINTS!'}
    }
    
    def __init__(self, x, y, powerup_type=None):
        super().__init__()
        self.type = powerup_type or random.choice(list(PowerUp.TYPES.keys()))
        self.info = PowerUp.TYPES[self.type]
        
        # Visual properties
        self.size = 40
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Animation
        self.pulse_timer = 0
        self.rotation = 0
        self.float_offset = 0
        self.spawn_y = y
        
        # Particle effect
        self.particles = []
        
    def update(self):
        """Animate power-up."""
        # Pulsing effect
        self.pulse_timer += 0.1
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7
        
        # Rotation
        self.rotation += 2
        
        # Floating motion
        self.float_offset = math.sin(self.pulse_timer * 0.5) * 5
        self.rect.centery = self.spawn_y + self.float_offset
        
        # Create particles
        if random.random() < 0.3:
            self.particles.append({
                'x': self.rect.centerx + random.randint(-10, 10),
                'y': self.rect.centery + random.randint(-10, 10),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, -0.5),
                'life': 30,
                'size': random.randint(2, 5)
            })
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Redraw image
        self.image.fill((0, 0, 0, 0))
        
        # Draw glow
        glow_radius = int(self.size * pulse)
        glow_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        for i in range(3):
            alpha = int(80 - i * 25)
            radius = glow_radius + i * 5
            pygame.draw.circle(glow_surface, (*self.info['color'], alpha), 
                             (self.size, self.size), radius)
        self.image.blit(glow_surface, (-self.size // 2, -self.size // 2))
        
        # Draw icon based on type
        icon_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        if self.type == 'speed':
            # Lightning bolt
            points = [(20, 5), (25, 20), (30, 20), (15, 35), (20, 22), (15, 22)]
            pygame.draw.polygon(icon_surface, self.info['color'], points)
        elif self.type == 'shield':
            # Shield shape
            pygame.draw.polygon(icon_surface, self.info['color'], 
                              [(20, 5), (35, 10), (35, 25), (20, 35), (5, 25), (5, 10)])
        elif self.type == 'slow_motion':
            # Clock
            pygame.draw.circle(icon_surface, self.info['color'], (20, 20), 15, 3)
            pygame.draw.line(icon_surface, self.info['color'], (20, 20), (20, 10), 3)
            pygame.draw.line(icon_surface, self.info['color'], (20, 20), (28, 20), 3)
        elif self.type == 'magnet':
            # Magnet U-shape
            pygame.draw.rect(icon_surface, self.info['color'], (8, 8, 6, 24))
            pygame.draw.rect(icon_surface, self.info['color'], (26, 8, 6, 24))
            pygame.draw.rect(icon_surface, self.info['color'], (8, 26, 24, 6))
        elif self.type == 'invincibility':
            # Star
            for i in range(5):
                angle1 = i * 72 - 90
                angle2 = (i * 72 + 36) - 90
                x1 = 20 + math.cos(math.radians(angle1)) * 15
                y1 = 20 + math.sin(math.radians(angle1)) * 15
                x2 = 20 + math.cos(math.radians(angle2)) * 7
                y2 = 20 + math.sin(math.radians(angle2)) * 7
                if i == 0:
                    points = [(x1, y1), (x2, y2)]
                else:
                    points.append((x1, y1))
                    points.append((x2, y2))
            pygame.draw.polygon(icon_surface, self.info['color'], points)
        elif self.type == 'double_points':
            # 2X text
            font = pygame.font.SysFont("Arial", 20, bold=True)
            text = font.render("2X", True, self.info['color'])
            icon_surface.blit(text, (text.get_rect(center=(20, 20))))
        
        # Rotate icon
        rotated = pygame.transform.rotate(icon_surface, self.rotation)
        rotated_rect = rotated.get_rect(center=(self.size // 2, self.size // 2))
        self.image.blit(rotated, rotated_rect)
    
    def draw_particles(self, screen):
        """Draw particle effects."""
        for particle in self.particles:
            alpha = int((particle['life'] / 30) * 200)
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.info['color'], alpha), 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (particle['x'] - particle['size'], 
                                          particle['y'] - particle['size']))


class PowerUpManager:
    """Manages power-up spawning and active effects."""
    
    def __init__(self):
        self.powerups_group = pygame.sprite.Group()
        self.active_effects = {}
        self.spawn_timer = 0
        self.spawn_interval = random.randint(8000, 15000)  # 8-15 seconds
        
    def update(self, delta_time, WIDTH, HEIGHT, bottom_margin):
        """Update power-ups and spawn new ones."""
        self.spawn_timer += delta_time
        
        # Spawn new power-up
        if self.spawn_timer >= self.spawn_interval:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - bottom_margin - 50)
            powerup = PowerUp(x, y)
            self.powerups_group.add(powerup)
            self.spawn_timer = 0
            self.spawn_interval = random.randint(8000, 15000)
        
        # Update all power-ups
        self.powerups_group.update()
        
        # Update active effects timers
        current_time = pygame.time.get_ticks()
        for effect_type in list(self.active_effects.keys()):
            if current_time >= self.active_effects[effect_type]['end_time']:
                del self.active_effects[effect_type]
    
    def check_collision(self, mosquito_rect):
        """Check if mosquito collected a power-up."""
        collected = []
        for powerup in self.powerups_group:
            if mosquito_rect.colliderect(powerup.rect):
                collected.append(powerup)
                self.activate_powerup(powerup.type)
                powerup.kill()
        return collected
    
    def activate_powerup(self, powerup_type):
        """Activate a power-up effect."""
        info = PowerUp.TYPES[powerup_type]
        end_time = pygame.time.get_ticks() + info['duration']
        self.active_effects[powerup_type] = {
            'end_time': end_time,
            'info': info
        }
    
    def is_active(self, effect_type):
        """Check if an effect is currently active."""
        return effect_type in self.active_effects
    
    def get_speed_multiplier(self):
        """Get current speed multiplier from active effects."""
        if self.is_active('speed'):
            return 1.5
        elif self.is_active('slow_motion'):
            return 0.6
        return 1.0
    
    def has_shield(self):
        """Check if shield is active."""
        return self.is_active('shield') or self.is_active('invincibility')
    
    def has_invincibility(self):
        """Check if invincibility is active."""
        return self.is_active('invincibility')
    
    def has_magnet(self):
        """Check if magnet is active."""
        return self.is_active('magnet')
    
    def get_points_multiplier(self):
        """Get current points multiplier."""
        return 2.0 if self.is_active('double_points') else 1.0
    
    def draw(self, screen):
        """Draw all power-ups and their particles."""
        for powerup in self.powerups_group:
            powerup.draw_particles(screen)
        self.powerups_group.draw(screen)
