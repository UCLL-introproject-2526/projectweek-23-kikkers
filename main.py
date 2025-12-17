import pygame
import os
import pygame
import sys
import random
from entities.fly import Mosquito
from entities.frog import Frog
#poopie
# Provides a simple alternating frame provider for human sprites.
# Call `get_current_human_frame()` to get a `pygame.Surface` that
# alternates between the two frames every 800 ms.
def get_current_human_frame():
    global _human_frames
    if '_human_frames' not in globals():
        _human_frames = []
        try:
            f1 = pygame.image.load(os.path.join('assets', 'images', 'crib_walk.png')).convert_alpha()
            f2 = pygame.image.load(os.path.join('assets', 'images', 'crib_walk_3.png')).convert_alpha()
        except Exception:
            f1 = pygame.Surface((72, 72), pygame.SRCALPHA)
            f1.fill((200, 50, 50))
            f2 = f1.copy()
        f1 = pygame.transform.scale(f1, (72, 72))
        f2 = pygame.transform.scale(f2, (72, 72))
        _human_frames = [f1, f2]

    # Alternate frames every 1000 ms
    idx = (pygame.time.get_ticks() // 800) % len(_human_frames)
    return _human_frames[idx]


if __name__ == '__main__':
    # Minimal test when running `python main.py` directly
    pygame.init()
    # create a tiny surface and blit current frame to verify
    s = pygame.display.set_mode((1, 1))
    print('Current human frame ready:', bool(get_current_human_frame()))


WIDTH, HEIGHT = 1024, 768
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogeato")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 64)

# Audio - commented out due to missing sound files
# background_music = "assets/sounds/background_music.mp3"
# musquito_sound = pygame.mixer.Sound("assets/sounds/musquito_sound.mp3")
# frog_sound = pygame.mixer.Sound("assets/sounds/frog_sound.mp3")
# tongue_attack = pygame.mixer.Sound("assets/sounds/tongue_stretching.mp3")
# game_over_sound = pygame.mixer.Sound("assets/sounds/fail_sound.mp3")
# level_up = pygame.mixer.Sound("assets/sounds/lvl_up_sound.mp3")
# victory = pygame.mixer.Sound("assets/sounds/victory_sound.mp3")
# death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")
# hit_sound = pygame.mixer.Sound("assets/sounds/hit_sound.mp3")
# suck_sound = pygame.mixer.Sound("assets/sounds/suck_sound.mp3")
# slap_sound = pygame.mixer.Sound("assets/sounds/slap_sound.mp3")
# countdown_sound = pygame.mixer.Sound("assets/sounds/countdown.mp3")

# pygame.mixer.music.load(background_music)
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)  # -1 = loop forever

# musquito_sound.set_volume(0.3)
# musquito_sound.play(-1)
# frog_sound.set_volume(0.3)
# frog_sound.play(-1)

import images


def start_screen():
    button_width = 200
    button_height = 50
    start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)

    while True:
        screen.blit(images.game_background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        start_color = (255, 255, 255) if start_button.collidepoint(mouse_pos) else (0, 0, 0)
        quit_color = (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0)

        if start_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        title_text = font.render("Frogeato", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 60))

        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = font.render("Start", True, start_color)
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))

        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        quit_text = font.render("Quit", True, quit_color)
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

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


def reset_game():
    mosquito = Mosquito(400, 100, size=70)
    mosquito.set_image(images.mosquito_image)
    frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=200)
    frog.set_image(images.frog_image)
    humans_group = pygame.sprite.Group()
    return mosquito, frog, humans_group, 0, 0, 0, False, False, False, 0


start_screen()

# Game state
mosquito, frog, humans_group, stun_timer, human_spawn_timer, score, game_won, game_over, paused, pause_countdown_start = reset_game()
countdown_start_time = pygame.time.get_ticks()
countdown_played = False
bottom_margin = 200
stun_duration = 500
human_spawn_interval = 5000
win_score = 10

running = True
while running:
    clock.tick(FPS)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elapsed = (pygame.time.get_ticks() - countdown_start_time) / 1000
    game_started = elapsed >= 3

    if not game_started and not countdown_played:
        # countdown_sound.play()
        countdown_played = True

    if stun_timer > 0:
        stun_timer -= clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mosquito, frog, humans_group, stun_timer, human_spawn_timer, score, game_won, game_over, paused, pause_countdown_start = reset_game()
            countdown_start_time = pygame.time.get_ticks()
            countdown_played = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_started and not game_over:
            if paused:
                paused = False
            else:
                paused = True
        if paused and event.type == pygame.MOUSEBUTTONDOWN:
            restart_button = pygame.Rect(WIDTH//2 - 180, HEIGHT//2, 80, 40)
            resume_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2, 80, 40)
            quit_button = pygame.Rect(WIDTH//2 + 60, HEIGHT//2, 80, 40)
            if restart_button.collidepoint(event.pos):
                mosquito, frog, humans_group, stun_timer, human_spawn_timer, score, game_won, game_over, paused, pause_countdown_start = reset_game()
                countdown_start_time = pygame.time.get_ticks()
                countdown_played = False
            if resume_button.collidepoint(event.pos):
                pause_countdown_start = pygame.time.get_ticks()
            if quit_button.collidepoint(event.pos):
                running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 80, 40)
            quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2, 80, 40)
            if restart_button.collidepoint(event.pos):
                mosquito, frog, humans_group, stun_timer, human_spawn_timer, score, game_won, game_over, paused, pause_countdown_start = reset_game()
                countdown_start_time = pygame.time.get_ticks()
                countdown_played = False
            if quit_button.collidepoint(event.pos):
                running = False

    pause_countdown_elapsed = 0
    if pause_countdown_start > 0:
        pause_countdown_elapsed = (pygame.time.get_ticks() - pause_countdown_start) / 1000
        if pause_countdown_elapsed >= 3:
            paused = False
            pause_countdown_start = 0

    if not paused and pause_countdown_start == 0:
        if game_started and not game_over:
            if stun_timer <= 0:
                mosquito.handle_input(pygame.key.get_pressed())
            mosquito.clamp_to_area(pygame.Rect(0, 0, WIDTH, HEIGHT - bottom_margin))

        humans_group.update()
        
        if game_started and not game_over:
            human_spawn_timer += clock.get_time()
            if human_spawn_timer >= human_spawn_interval:
                # import here to avoid circular import at module load time
                from entities.human import Human
                humans_group.add(Human(WIDTH, HEIGHT))
                human_spawn_timer = 0
        
        if game_started and not game_over:
            for human in humans_group:
                if mosquito.rect.colliderect(human.rect):
                    human.kill()
                    score += 1
                    # suck_sound.play()
                    stun_timer = stun_duration
                    if score >= win_score:
                        game_over = True
                        game_won = True
                        # victory.play()
                    break
        frog.update((mosquito.centerx, mosquito.centery), game_started, game_over)

        # Check if tongue hit mosquito
        if game_started and not game_over:
            frog.check_hit((mosquito.centerx, mosquito.centery), mosquito.size / 2)
        # Check if tongue caught mosquito and update position
        caught_pos = frog.get_caught_mosquito_position()
        if caught_pos and not game_over:
            # Move mosquito to tongue tip position
            mosquito.rect.centerx = int(caught_pos[0])
            mosquito.rect.centery = int(caught_pos[1])
        # Game over when mosquito is pulled into frog's mouth
        if game_started and frog.is_mosquito_eaten():
            game_over = True
            # death_sound.play()
            # tongue_attack.play()

    screen.blit(images.game_background, (0, 0))
    mosquito.draw(screen)
    frog.draw(screen)

    humans_group.draw(screen)
    score_text = font.render(f"Score: {score}", True, (255, 100, 100))
    screen.blit(score_text, (10, 10))

    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pause_text = font.render("Paused", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))
        
        restart_button = pygame.Rect(WIDTH//2 - 180, HEIGHT//2, 80, 40)
        resume_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2, 80, 40)
        quit_button = pygame.Rect(WIDTH//2 + 60, HEIGHT//2, 80, 40)
        mouse_pos = pygame.mouse.get_pos()
        
        if restart_button.collidepoint(mouse_pos) or resume_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        pygame.draw.rect(screen, (0, 255, 0), resume_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        
        restart_text = font.render("Restart", True, (255, 255, 255) if restart_button.collidepoint(mouse_pos) else (0, 0, 0))
        resume_text = font.render("Resume", True, (255, 255, 255) if resume_button.collidepoint(mouse_pos) else (0, 0, 0))
        quit_text = font.render("Quit", True, (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0))
        
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))
        screen.blit(resume_text, (resume_button.centerx - resume_text.get_width() // 2, resume_button.centery - resume_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    if stun_timer > 0 and game_started and not game_over:
        msg = font.render("sucking blood!", True, (255, 100, 100))
        screen.blit(msg, (mosquito.centerx - msg.get_width() // 2, max(0, mosquito.rect.top - msg.get_height() - 6)))

    if not game_started:
        countdown_text = font.render(str(max(1, 3 - int(elapsed))), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    if pause_countdown_start > 0:
        countdown_text = big_font.render(str(max(1, 3 - int(pause_countdown_elapsed))), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - 150))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render("You Win!" if game_won else "Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        
        restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 80, 40)
        quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2, 80, 40)
        mouse_pos = pygame.mouse.get_pos()
        
        if restart_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        
        restart_text = font.render("Restart", True, (255, 255, 255) if restart_button.collidepoint(mouse_pos) else (0, 0, 0))
        quit_text = font.render("Quit", True, (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0))
        
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()

