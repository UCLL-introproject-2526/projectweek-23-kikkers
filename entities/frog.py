import pygame
import random
import math
from entities.tongue import Tongue


class Frog:
    """Enemy frog that shoots tongue at mosquito with realistic hunting behavior."""
    
    def __init__(self, screen_width, screen_height, size=200, bottom_margin=200):
        self.size = size
        self.color = (50, 200, 50)
        self.bottom_margin = bottom_margin
        
        # Position frog at bottom center
        frog_space = pygame.Rect(0, screen_height - bottom_margin, screen_width, bottom_margin)
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = frog_space.center
        
        # Tongue
        self.tongue = Tongue()
        
        # Hunting behavior states
        self.state = "idle"  # idle, tracking, preparing, attacking
        self.attack_timer = random.randint(40, 70)  # Shoots more frequently
        self.preparation_timer = 0
        self.tracking_duration = 0
        
        # Targeting system
        self.target_history = []  # Track mosquito positions for prediction
        self.last_mosquito_pos = None
        self.attack_range = 700  # Wider attack range for difficulty
        self.optimal_range = 400  # Preferred attack distance
        
        # Visual feedback
        self.eye_glow = 0  # Intensity of eye glow when preparing to attack
        self.body_tension = 0  # Visual indicator of attack preparation
        
        # Image
        self.image = None
        
    def set_image(self, image):
        """Set sprite image for frog."""
        self.image = image
        
    def update(self, mosquito_center, game_started, game_over):
        """Update frog AI with realistic hunting behavior."""
        # Update tongue
        self.tongue.update()
        
        if not game_started or game_over:
            self.state = "idle"
            self.eye_glow = max(0, self.eye_glow - 5)
            self.body_tension = max(0, self.body_tension - 0.05)
            return
        
        # Calculate distance to mosquito
        dist_to_mosquito = math.hypot(
            mosquito_center[0] - self.rect.centerx,
            mosquito_center[1] - self.rect.centery
        )
        
        # Track mosquito movement for prediction
        if self.last_mosquito_pos:
            self.target_history.append(mosquito_center)
            if len(self.target_history) > 10:  # Keep last 10 positions
                self.target_history.pop(0)
        self.last_mosquito_pos = mosquito_center
        
        # State machine for realistic frog behavior
        if self.tongue.active:
            self.state = "attacking"
            self.eye_glow = max(0, self.eye_glow - 8)
            self.body_tension = max(0, self.body_tension - 0.1)
            
        elif self.state == "attacking":
            # Tongue finished, return to idle and prepare for next attack
            self.state = "idle"
            self.attack_timer = random.randint(20, 40)  # Quick cooldown for constant attacks
            
        elif self.state == "idle":
            self.eye_glow = max(0, self.eye_glow - 3)
            self.body_tension = max(0, self.body_tension - 0.05)
            self.attack_timer -= 1
            
            # Start tracking if mosquito is in range and timer expired
            if self.attack_timer <= 0 and dist_to_mosquito < self.attack_range:
                self.state = "tracking"
                self.tracking_duration = random.randint(25, 50)  # Balanced tracking
                
        elif self.state == "tracking":
            # Frog watches the mosquito, eyes following
            self.tracking_duration -= 1
            self.eye_glow = min(100, self.eye_glow + 4)
            
            # Decide whether to attack based on position and movement
            if self.tracking_duration <= 0:
                # Check if mosquito is in good position
                in_optimal_range = dist_to_mosquito < self.optimal_range
                mosquito_moving_slowly = self._is_mosquito_slow()
                
                if in_optimal_range or mosquito_moving_slowly or random.random() < 0.4:
                    # Enter preparation phase
                    self.state = "preparing"
                    self.preparation_timer = random.randint(15, 28)  # Slightly slower windup for fairness
                else:
                    # Reset and wait
                    self.state = "idle"
                    self.attack_timer = random.randint(25, 50)  # Shorter cooldown
                    
        elif self.state == "preparing":
            # Frog tenses up before strike (visual windup)
            self.preparation_timer -= 1
            self.eye_glow = min(255, self.eye_glow + 15)
            self.body_tension = min(1.0, self.body_tension + 0.08)
            
            if self.preparation_timer <= 0:
                # STRIKE! Predict where mosquito will be
                predicted_target = self._predict_mosquito_position(mosquito_center)
                self.tongue.shoot(self.rect.center, predicted_target)
                self.state = "attacking"
                self.attack_timer = random.randint(30, 60)  # Quick cooldown for multiple shots
    
    def _is_mosquito_slow(self):
        """Check if mosquito is moving slowly (easier target)."""
        if len(self.target_history) < 3:
            return False
        
        # Calculate recent movement
        recent_movement = 0
        for i in range(len(self.target_history) - 3, len(self.target_history) - 1):
            dx = self.target_history[i+1][0] - self.target_history[i][0]
            dy = self.target_history[i+1][1] - self.target_history[i][1]
            recent_movement += math.hypot(dx, dy)
        
        return recent_movement < 10  # Moving less than 10 pixels over 3 frames
    
    def _predict_mosquito_position(self, current_pos):
        """Predict where mosquito will be based on movement history."""
        if len(self.target_history) < 3:
            return current_pos
        
        # Calculate velocity from recent positions
        vx = (self.target_history[-1][0] - self.target_history[-3][0]) / 2
        vy = (self.target_history[-1][1] - self.target_history[-3][1]) / 2
        
        # Predict position 12-18 frames ahead for better accuracy
        lead_frames = random.randint(12, 18)
        predicted_x = current_pos[0] + vx * lead_frames
        predicted_y = current_pos[1] + vy * lead_frames
        
        return (predicted_x, predicted_y)
    
    def check_hit(self, mosquito_center, mosquito_radius):
        """Check if tongue hit mosquito."""
        return self.tongue.check_collision(mosquito_center, mosquito_radius)
    
    def get_caught_mosquito_position(self):
        """Get position of mosquito if caught by tongue."""
        return self.tongue.get_caught_mosquito_position()
    
    def is_mosquito_eaten(self):
        """Check if caught mosquito has been pulled into mouth."""
        return self.tongue.is_mosquito_eaten()
    
    def draw(self, screen):
        """Draw frog and tongue with visual feedback."""
        # Draw frog image with tension effect
        if self.image:
            # Apply slight scaling when preparing to attack
            if self.body_tension > 0:
                scale_factor = 1.0 + (self.body_tension * 0.08)
                scaled_size = (int(self.image.get_width() * scale_factor), 
                             int(self.image.get_height() * scale_factor))
                scaled_image = pygame.transform.scale(self.image, scaled_size)
                offset_x = (scaled_image.get_width() - self.image.get_width()) // 2
                offset_y = (scaled_image.get_height() - self.image.get_height()) // 2
                screen.blit(scaled_image, (self.rect.left - offset_x, self.rect.top - offset_y))
            else:
                screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw eye glow when tracking/preparing (warning to player)
        if self.eye_glow > 50:
            glow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            glow_alpha = int(min(150, self.eye_glow))
            
            # Draw glowing eyes
            eye_color = (255, 200, 0, glow_alpha)  # Yellow glow
            left_eye_pos = (int(self.rect.width * 0.35), int(self.rect.height * 0.3))
            right_eye_pos = (int(self.rect.width * 0.65), int(self.rect.height * 0.3))
            pygame.draw.circle(glow_surface, eye_color, left_eye_pos, 12)
            pygame.draw.circle(glow_surface, eye_color, right_eye_pos, 12)
            
            screen.blit(glow_surface, self.rect.topleft)
        
        # Update tongue center before drawing
        self.tongue.frog_center = self.rect.center
        self.tongue.draw(screen)
    
    def reset(self):
        """Reset frog state."""
        self.tongue.active = False
        self.tongue.length = 0
        self.attack_timer = random.randint(40, 70)
        self.state = "idle"
        self.preparation_timer = 0
        self.tracking_duration = 0
        self.target_history = []
        self.last_mosquito_pos = None
        self.eye_glow = 0
        self.body_tension = 0
