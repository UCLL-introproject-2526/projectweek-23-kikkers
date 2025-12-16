import pygame
from settings import *
from entities.fly import Fly
from entities.frog import Frog
from entities.tongue import Tongue

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load images
fly_images = [pygame.image.load("assets/fly_sprite1.png"),
              pygame.image.load("assets/fly_sprite2.png")]

frog_image = pygame.image.load("assets/frog_idle.png")
tongue_image = pygame.image.load("assets/tongue.png")

fly = Fly(WIDTH//2, HEIGHT-50, fly_images)
frog = Frog(WIDTH//2, 50, frog_image, tongue_image)

score = 0

running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    fly.move(keys)
    fly.animate()
    frog.update()
    if random.randint(0,100) < 5:
        frog.attack()

    for tongue in frog.tongues:
        if fly.rect.colliderect(tongue.rect):
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()

    # Draw
    screen.fill((50,150,255))  # temporary sky
    fly.draw(screen)
    frog.draw(screen)

    score += 1
    score_text = pygame.font.SysFont("Arial",36).render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT-50))

    pygame.display.flip()
