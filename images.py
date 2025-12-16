import pygame

# Load and scale images (avoid convert/convert_alpha here because
# this module may be imported before a display is initialized)
frog_image = pygame.image.load('images/frog1.png')
frog_image = pygame.transform.scale(frog_image, (230, 170))

mosquito_image = pygame.image.load('images/musqi1.png')
mosquito_image = pygame.transform.scale(mosquito_image, (70, 70))

# Human image (optional). Filename contains space: 'human head.png'
try:
    human_head = pygame.image.load('images/human head.png')
    human_head = pygame.transform.scale(human_head, (48, 48))
except Exception:
    human_head = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.rect(human_head, (200, 50, 50), human_head.get_rect())
