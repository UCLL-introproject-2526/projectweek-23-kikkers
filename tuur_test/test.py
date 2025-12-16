import pygame
import sys
import random
import math

def create_main_surface():
    size = (1024, 768)
    surface = pygame.display.set_mode(size)
    pygame.display.set_caption("Mosquito vs Frog")
    return surface

def main():
    pygame.init()

    screen = create_main_surface()
    clock = pygame.time.Clock()

    # Mosquito setup
    mosquito_size = 30
    mosquito_color = (200, 50, 50)
    mosquito = pygame.Rect(400, 400, mosquito_size, mosquito_size)
    speed = 5

    # Frog setup
    frog_size = 150
    frog_color = (50, 200, 50)
    top_margin = 200
    frog_space = pygame.Rect(0, 0, screen.get_width(), top_margin)
    frog = pygame.Rect(0, 0, frog_size, frog_size)
    frog.center = frog_space.center

    # Tongue setup
    tongue_color = (255, 100, 100)
    tongue_active = False
    tongue_length = 0
    max_tongue_length = 400
    tongue_speed = 25
    tongue_width = 20
    tongue_dx, tongue_dy = 0, 0  # direction vector

    # Random attack timer
    attack_timer = random.randint(60, 180)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mosquito movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            mosquito.x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            mosquito.x += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            mosquito.y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            mosquito.y += speed

        # Keep mosquito inside play area
        play_area = pygame.Rect(0, top_margin, screen.get_width(), screen.get_height() - top_margin)
        mosquito.clamp_ip(play_area)

        # Tongue attack logic
        if not tongue_active:
            attack_timer -= 1
            if attack_timer <= 0:
                tongue_active = True
                tongue_length = 0
                # Calculate direction vector toward mosquito
                dx = mosquito.centerx - frog.centerx
                dy = mosquito.centery - frog.centery
                dist = math.hypot(dx, dy)
                if dist == 0: dist = 1
                tongue_dx = dx / dist
                tongue_dy = dy / dist
                attack_timer = random.randint(60, 180)

        if tongue_active:
            tongue_length += tongue_speed
            if tongue_length >= max_tongue_length:
                tongue_active = False

            # Tongue endpoint
            end_x = frog.centerx + tongue_dx * tongue_length
            end_y = frog.centery + tongue_dy * tongue_length

            # Draw tongue as a thick line (hitbox)
            tongue_rect = pygame.draw.line(
                screen, tongue_color,
                frog.center, (end_x, end_y),
                tongue_width
            )

            # Collision check (approximate with rect around line)
            if tongue_rect.colliderect(mosquito):
                print("Mosquito caught!")
                running = False

        # Draw everything
        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, mosquito_color, mosquito)  # mosquito
        pygame.draw.rect(screen, frog_color, frog)          # frog

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()