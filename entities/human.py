import pygame
import random
import images


class Human(pygame.sprite.Sprite):
    """Falling human that stuns the mosquito when caught."""
    
    def __init__(self, width, height, image=None):
        super().__init__()
        # Use animated frames from images module if available
        try:
            self.image = images.get_current_human_frame()
        except Exception:
            # Fallback to static human head image or colored circle
            try:
                self.image = pygame.image.load('assets/images/humanhead.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (72, 72))
            except Exception:
                self.image = pygame.Surface((72, 72), pygame.SRCALPHA)
                pygame.draw.circle(self.image, (255, 200, 150), (36, 36), 36)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(1.5, 3.5)
        # dying state: when True, show dying image until `dying_until` timestamp
        self.dying = False
        self.dying_until = 0

    def update(self):
        """Move human down the screen."""
        # If dying, show dying image and wait until timer expires, do not move
        if getattr(self, 'dying', False):
            try:
                topleft = self.rect.topleft
                self.image = images.dying_human
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft
            except Exception:
                pass
            # remove when dying period has passed
            if pygame.time.get_ticks() >= getattr(self, 'dying_until', 0):
                self.kill()
            return

        # Normal animation: update frame and move down
        try:
            topleft = self.rect.topleft
            self.image = images.get_current_human_frame()
            self.rect = self.image.get_rect()
            self.rect.topleft = topleft
        except Exception:
            pass

        self.rect.y += self.speed
        # Remove when off bottom of screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
