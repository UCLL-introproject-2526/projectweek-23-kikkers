import pygame

# Load and scale images
frog_image = pygame.image.load('assets/images/frog1.png').convert_alpha()
frog_image = pygame.transform.scale(frog_image, (230, 170))

mosquito_image = pygame.image.load('assets/images/fly_sprite.png').convert_alpha()
mosquito_image = pygame.transform.scale(mosquito_image, (70, 70))

game_background = pygame.image.load('assets/images/game background 2.png').convert()
