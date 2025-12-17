import pygame

# Load and scale images
frog_image = pygame.image.load('assets/images/kikker_zonder_tong.png').convert_alpha()
frog_image = pygame.transform.scale(frog_image, (170, 170))

frog_tong_image = pygame.image.load('assets/images/kikker_met_tong.png').convert_alpha()
frog_tong_image = pygame.transform.scale(frog_tong_image, (170,170))

mosquito_image = pygame.image.load('assets/images/fly_sprite.png').convert_alpha()
mosquito_image = pygame.transform.scale(mosquito_image, (70, 70))

game_background = pygame.image.load('assets/images/game background 2.png').convert()

# Human image (optional). Filename contains space: 'human head.png'
try:
    human_head = pygame.image.load('images/human head.png')
    human_head = pygame.transform.scale(human_head, (48, 48))
except Exception:
    human_head = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.rect(human_head, (200, 50, 50), human_head.get_rect())