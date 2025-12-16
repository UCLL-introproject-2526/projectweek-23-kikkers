import pygame, random, images



class Human(pygame.sprite.Sprite):
    def __init__(self, width, height, image=None):
        super().__init__()
        if image:
            self.image = image
        else:
            # try to use images.human_head if available
            try:
                import images
                self.image = images.human_head
            except Exception:
                self.image = pygame.Surface((24, 24))
                self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(1.5, 3.5)
        self.image = pygame.transform.scale(images.human_head, (72, 72))

    def update(self):
        self.rect.y += self.speed
        # remove when off bottom of screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()


    