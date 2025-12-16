import pygame

# Load and scale images
frog_image = pygame.image.load('images/frog1.png').convert_alpha()
frog_image = pygame.transform.scale(frog_image, (230, 170))

mosquito_image = pygame.image.load('images/musqi1.png').convert_alpha()
mosquito_image = pygame.transform.scale(mosquito_image, (70, 70))
