import pygame

# Initialize mixer
pygame.mixer.init()

# Load sounds
background_music = "assets/sounds/background_music.mp3"
musquito_sound = pygame.mixer.Sound("assets/sounds/musquito_sound.mp3")
frog_sound = pygame.mixer.Sound("assets/sounds/frog_sound.mp3")
tongue_attack = pygame.mixer.Sound("assets/sounds/tongue_stretching.mp3")
game_over_sound = pygame.mixer.Sound("assets/sounds/fail_sound.mp3")
level_up = pygame.mixer.Sound("assets/sounds/lvl_up_sound.mp3")
victory = pygame.mixer.Sound("assets/sounds/victory_sound.mp3")
death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")
hit_sound = pygame.mixer.Sound("assets/sounds/hit_sound.mp3")
suck_sound = pygame.mixer.Sound("assets/sounds/suck_sound.mp3")
slap_sound = pygame.mixer.Sound("assets/sounds/slap_sound.mp3")
countdown_sound = pygame.mixer.Sound("assets/sounds/countdown.mp3")

# Set volumes
musquito_sound.set_volume(0.3)
frog_sound.set_volume(0.3)

# Start background sounds
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
musquito_sound.play(-1)
frog_sound.play(-1)