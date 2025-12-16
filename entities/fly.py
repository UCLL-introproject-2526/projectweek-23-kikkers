import pygame


class Mosquito:
    """Player-controlled mosquito that must avoid the frog's tongue."""
    
    def __init__(self, x, y, size=70):
        self.size = size
        self.color = (200, 50, 50)
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 5
        self.image = None
        
    def set_image(self, image):
        """Set sprite image for mosquito."""
        self.image = image
        
    def handle_input(self, keys):
        """Handle WASD movement."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
    
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
