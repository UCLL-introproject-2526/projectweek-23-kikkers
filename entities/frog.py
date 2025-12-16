import pygame
import random
from entities.tongue import Tongue


class Frog:
    """Enemy frog that shoots tongue at mosquito."""
    
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
        
        # Attack timing
        self.attack_timer = random.randint(60, 120)
        
        # Image
        self.image = None
        
    def set_image(self, image):
        """Set sprite image for frog."""
        self.image = image
        
    def update(self, mosquito_center, game_started, game_over):
        """Update frog AI and tongue."""
        # Update tongue
        self.tongue.update()
        
        # Attack logic
        if game_started and not game_over and not self.tongue.active:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.tongue.shoot(self.rect.center, mosquito_center)
                self.attack_timer = random.randint(60, 180)
    
    def check_hit(self, mosquito_center, mosquito_radius):
        """Check if tongue hit mosquito."""
        return self.tongue.check_collision(mosquito_center, mosquito_radius)
    
    def draw(self, screen):
        """Draw frog and tongue."""
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Update tongue center before drawing
        self.tongue.frog_center = self.rect.center
        self.tongue.draw(screen)
    
    def reset(self):
        """Reset frog state."""
        self.tongue.active = False
        self.tongue.length = 0
        self.attack_timer = random.randint(60, 120)
