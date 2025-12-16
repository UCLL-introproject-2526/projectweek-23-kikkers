import pygame
import random
from settings import *
from entities.tongue import Tongue

class Frog:
    def __init__(self, x, y, image, tongue_image):
        self.x = x
        self.y = y
        self.width = FROG_WIDTH
        self.height = FROG_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = image
        self.tongue_image = tongue_image
        self.speed = FROG_SPEED
        self.direction = 1
        self.attack_cooldown = 0
        self.tongues = []

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.direction = 1
        elif self.x + self.width >= WIDTH:
            self.direction = -1
        self.rect.topleft = (self.x, self.y)

    def attack(self):
        if self.attack_cooldown == 0:
            for _ in range(random.randint(2,4)):
                tongue_x = self.x + random.randint(0, self.width)
                tongue_y = self.y + self.height
                width = random.randint(20, 35)
                height = random.randint(150, 250)
                speed_y = random.randint(6,10)
                tongue = Tongue(tongue_x, tongue_y, width, height, speed_y, self.tongue_image)
                self.tongues.append(tongue)
            self.attack_cooldown = random.randint(60, 120)

    def update(self):
        self.move()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        new_tongues = []
        for tongue in self.tongues:
            if tongue.update():
                new_tongues.append(tongue)
        self.tongues = new_tongues

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for tongue in self.tongues:
            tongue.draw(screen)
