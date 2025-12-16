import pygame
import random


class Human(pygame.sprite.Sprite):
    """Falling human that stuns the mosquito when caught."""
    
    def __init__(self, width, height, image=None):
        super().__init__()
        # Load human head image
        try:
            self.image = pygame.image.load('assets/images/humanhead.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (72, 72))
        except:
            # Fallback to colored circle if image not found
            self.image = pygame.Surface((72, 72), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 200, 150), (36, 36), 36)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(1.5, 3.5)

    def update(self):
        """Move human down the screen."""
        self.rect.y += self.speed
        # Remove when off bottom of screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
