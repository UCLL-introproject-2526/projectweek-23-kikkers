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
        # touched state: when player touches the human show dying image briefly
        self.touched = False
        self.touched_start = None
        self._touched_image = None
        # whether this human can be hit by the player (becomes False after dying animation)
        self.can_be_hit = True

    def touch(self):
        """Mark this human as touched by player: show dying image briefly."""
        if not self.touched:
            # mark as touched and prevent further hits immediately
            self.touched = True
            self.can_be_hit = False
            self.touched_start = pygame.time.get_ticks()
            try:
                img = pygame.image.load('assets/images/dying_human.png').convert_alpha()
                img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
                self._touched_image = img
                topleft = self.rect.topleft
                self.image = self._touched_image
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft
            except Exception:
                # silently ignore image load errors
                self._touched_image = None

    def update(self):
        """Move human down the screen."""
        # If currently in touched state, switch back after 0.5s
        if self.touched:
            elapsed = pygame.time.get_ticks() - (self.touched_start or 0)
            if elapsed >= 500:
                # restore normal animation frame
                self.touched = False
                self.touched_start = None
                self._touched_image = None
                # after the dying animation is over, make the human un-hittable
                self.can_be_hit = False
                try:
                    topleft = self.rect.topleft
                    self.image = images.get_current_human_frame()
                    self.rect = self.image.get_rect()
                    self.rect.topleft = topleft
                except Exception:
                    pass

        # Update animation frame while preserving position if not touched
        if not self.touched:
            try:
                topleft = self.rect.topleft
                self.image = images.get_current_human_frame()
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft
            except Exception:
                pass

        # Always continue falling (touch doesn't stop movement)
        self.rect.y += self.speed

        # Remove when off bottom of screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
