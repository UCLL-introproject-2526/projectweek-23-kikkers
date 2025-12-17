import pygame

# Load and scale images
frog_image = pygame.image.load('assets/images/kikker_zonder_tong.png').convert_alpha()
frog_image = pygame.transform.scale(frog_image, (170, 170))

frog_tong_image = pygame.image.load('assets/images/kikker_met_tong.png').convert_alpha()
frog_tong_image = pygame.transform.scale(frog_tong_image, (170,170))

mosquito_image = pygame.image.load('assets/images/fly_sprite.png').convert_alpha()
mosquito_image = pygame.transform.scale(mosquito_image, (70, 70))

game_background = pygame.image.load('assets/images/background_moving.gif').convert()

# Human image (optional). Filename contains space: 'human head.png'
try:
    human_head = pygame.image.load('images/human head.png')
    human_head = pygame.transform.scale(human_head, (48, 48))
except Exception:
    human_head = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.rect(human_head, (200, 50, 50), human_head.get_rect())

# Load alternate walking frames for humans (used for simple animation)
_human_walk_frames = []
try:
    _f1 = pygame.image.load('assets/images/crib_walk.png').convert_alpha()
    _f2 = pygame.image.load('assets/images/crib_walk_3.png').convert_alpha()
    _f1 = pygame.transform.scale(_f1, (96, 96))
    _f2 = pygame.transform.scale(_f2, (96, 96))
    _human_walk_frames = [_f1, _f2]
except Exception:
    # Fallback: create two colored placeholders
    s = pygame.Surface((96, 96), pygame.SRCALPHA)
    s.fill((200, 50, 50))
    _human_walk_frames = [s, s.copy()]

def get_current_human_frame():
    # Alternate frames every 1000 ms
    idx = (pygame.time.get_ticks() // 1000) % len(_human_walk_frames)
    return _human_walk_frames[idx]

# Dying human image (displayed while mosquito is sucking blood)
try:
    dying_human = pygame.image.load('assets/images/dying_human.png').convert_alpha()
    dying_human = pygame.transform.scale(dying_human, (_human_walk_frames[0].get_width(), _human_walk_frames[0].get_height()))
except Exception:
    dying_human = pygame.Surface((_human_walk_frames[0].get_width(), _human_walk_frames[0].get_height()), pygame.SRCALPHA)
    pygame.draw.rect(dying_human, (150, 30, 30), dying_human.get_rect())