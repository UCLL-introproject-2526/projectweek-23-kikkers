import pygame
import sys
import random
import math


# Code werkt

WIDTH, HEIGHT = 1024, 768
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogeato")
import pygame
import sys
import random
import math
from entities.human import Human
import images


# Settings
WIDTH, HEIGHT = 1024, 768
FPS = 60
TARGET_SCORE = 10


def start_screen(screen, clock, font):
    button_width = 200
    button_height = 50
    start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)

    while True:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        start_color = (255, 255, 255) if start_button.collidepoint(mouse_pos) else (0, 0, 0)
        quit_color = (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0)

        if start_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        title_text = font.render("Frogeato", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2,
                                 HEIGHT // 2 - title_text.get_height() // 2 - 60))

        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = font.render("Start", True, start_color)
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                 start_button.centery - start_text.get_height() // 2))

        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        quit_text = font.render("Quit", True, quit_color)
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                quit_button.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def point_line_distance(px, py, x1, y1, x2, y2):
    line_mag = math.hypot(x2 - x1, y2 - y1)
    if line_mag == 0:
        return math.hypot(px - x1, py - y1)
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
    u = max(min(u, 1), 0)
    closest_x = x1 + u * (x2 - x1)
    closest_y = y1 + u * (y2 - y1)
    return math.hypot(px - closest_x, py - closest_y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frogeato")
    clock = pygame.time.Clock()
    ui_font = pygame.font.SysFont("Arial", 32)

    # Player (mosquito) and frog static area
    mosquito_size = 70
    mosquito = pygame.Rect(400, 400, mosquito_size, mosquito_size)
    speed = 5

    frog_size = 200
    top_margin = 200
    frog_space = pygame.Rect(0, 0, screen.get_width(), top_margin)
    frog = pygame.Rect(0, 0, frog_size, frog_size)
    frog.center = frog_space.center

    # Tongue
    tongue_color = (255, 100, 100)
    tongue_active = False
    tongue_length = 0
    max_tongue_length = 800
    tongue_speed = 14
    retracting_speed = 23
    tongue_width = 30
    tongue_dx, tongue_dy = 0, 0
    retracting = False
    attack_timer = random.randint(60, 120)

    # Humans, scoring
    humans = pygame.sprite.Group()
    score = 0
    game_won = False

    HUMAN_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(HUMAN_SPAWN_EVENT, 5000)

    # stun state
    STUN_MS = 500
    stunned = False
    stun_end_time = 0

    start_screen(screen, clock, ui_font)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == HUMAN_SPAWN_EVENT and not game_won:
                humans.add(Human(WIDTH, HEIGHT))

        # Update stun state
        if stunned and pygame.time.get_ticks() >= stun_end_time:
            stunned = False

        keys = pygame.key.get_pressed()
        # Movement disabled while stunned
        if not stunned:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                mosquito.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                mosquito.x += speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                mosquito.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                mosquito.y += speed

        play_area = pygame.Rect(0, top_margin, screen.get_width(), screen.get_height() - top_margin)
        mosquito.clamp_ip(play_area)

        # Tongue behavior (keeps original mechanics)
        if not tongue_active:
            attack_timer -= 1
            if attack_timer <= 0:
                tongue_active = True
                tongue_length = 0
                retracting = False
                dx = mosquito.centerx - frog.centerx
                dy = mosquito.centery - frog.centery
                dist = math.hypot(dx, dy)
                if dist == 0:
                    dist = 1
                tongue_dx = dx / dist
                tongue_dy = dy / dist
                attack_timer = random.randint(60, 180)

        if tongue_active:
            if not retracting:
                tongue_length += tongue_speed
                if tongue_length >= max_tongue_length:
                    retracting = True
            else:
                tongue_length -= retracting_speed
                if tongue_length <= 0:
                    tongue_active = False
                    tongue_length = 0

        end_x = frog.centerx + tongue_dx * tongue_length
        end_y = frog.centery + tongue_dy * tongue_length

        if tongue_active:
            if point_line_distance(mosquito.centerx, mosquito.centery,
                                   frog.centerx, frog.centery,
                                   end_x, end_y) < (tongue_width / 2 + mosquito_size / 2):
                print("Mosquito caught!")
                running = False

        # Update and draw
        screen.fill((40, 40, 40))
        screen.blit(images.mosquito_image, mosquito.topleft)
        screen.blit(images.frog_image, frog.topleft)

        if tongue_active:
            pygame.draw.line(screen, tongue_color, frog.center, (end_x, end_y), tongue_width)

        humans.update()
        humans.draw(screen)

        # Collision: mosquito rect with humans -> increment score
        collected = [h for h in humans if mosquito.colliderect(h.rect)]
        for h in collected:
            h.kill()
        if collected:
            score += len(collected)
            # apply stun for a short duration
            stunned = True
            stun_end_time = pygame.time.get_ticks() + STUN_MS
            if score >= TARGET_SCORE:
                game_won = True
                pygame.time.set_timer(HUMAN_SPAWN_EVENT, 0)

        # UI
        score_surf = ui_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        # Stun indicator
        if stunned:
            stun_surf = ui_font.render("Sucking Blood!", True, (255, 200, 0))
            screen.blit(stun_surf, (mosquito.centerx - stun_surf.get_width() // 2, mosquito.top - 30))
        if game_won:
            win_surf = ui_font.render("You win!", True, (0, 255, 0))
            screen.blit(win_surf, (WIDTH // 2 - win_surf.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()