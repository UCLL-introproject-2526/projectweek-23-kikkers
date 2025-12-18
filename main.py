import pygame
import os
import pygame
import sys
import random
import audio
from entities.fly import Mosquito
from entities.frog import Frog
os.environ['SDL_VIDEO_CENTERED'] = '1'
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
# Silkscreen retro pixel font for authentic arcade feel
font = pygame.font.Font("Silkscreen-Regular.ttf", 20)
big_font = pygame.font.Font("Silkscreen-Regular.ttf", 40)
score_font = pygame.font.Font("Silkscreen-Regular.ttf", 28)
title_font = pygame.font.Font("Silkscreen-Regular.ttf", 72)  # HUGE title font

# Load images after display is initialized
import images
images.load_images()


def start_screen():
    button_width = 260
    button_height = 70
    start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 60, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height)

    while True:
        screen.blit(images.game_background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # HUGE pixelated title with swamp colors
        title_text = title_font.render("FROGEATO", False, (150, 255, 100))  # Bright swamp green
        title_bg = pygame.Surface((title_text.get_width() + 40, title_text.get_height() + 20))
        title_bg.fill((20, 50, 20))  # Dark swamp background
        title_bg.set_alpha(200)
        screen.blit(title_bg, (WIDTH // 2 - title_text.get_width() // 2 - 20, HEIGHT // 2 - 180))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 170))
        
        # Pixelated border around title
        title_border = pygame.Rect(WIDTH // 2 - title_text.get_width() // 2 - 20, HEIGHT // 2 - 180, 
                                    title_text.get_width() + 40, title_text.get_height() + 20)
        pygame.draw.rect(screen, (100, 200, 80), title_border, 4)  # Thick pixel border

        # START button - pixelated swamp style
        start_hover = start_button.collidepoint(mouse_pos)
        start_bg_color = (80, 180, 60) if start_hover else (50, 140, 40)  # Swamp green
        start_border_color = (150, 255, 100) if start_hover else (100, 200, 80)
        pygame.draw.rect(screen, start_bg_color, start_button)
        pygame.draw.rect(screen, start_border_color, start_button, 5)  # Thick pixelated border
        
        start_text = big_font.render("START", False, (255, 255, 255) if start_hover else (200, 255, 180))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, 
                                 start_button.centery - start_text.get_height() // 2))

        # QUIT button - pixelated swamp danger style  
        quit_hover = quit_button.collidepoint(mouse_pos)
        quit_bg_color = (180, 80, 60) if quit_hover else (140, 50, 40)  # Swamp red
        quit_border_color = (255, 150, 100) if quit_hover else (200, 100, 80)
        pygame.draw.rect(screen, quit_bg_color, quit_button)
        pygame.draw.rect(screen, quit_border_color, quit_button, 5)  # Thick pixelated border
        
        quit_text = big_font.render("QUIT", False, (255, 255, 255) if quit_hover else (255, 200, 180))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                quit_button.centery - quit_text.get_height() // 2))

        if start_hover or quit_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
    mosquito.set_wing_images(images.mosquito_wingup, images.mosquito_wingdown)
    frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=200)
    frog.set_image(images.frog_image)
    frog.set_open_image(images.frog_tong_image)
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
win_score = 100
# Points awarded per human hit. Default: 10% of win_score (so 10 when win_score=100)
points_per_human = max(1, win_score // 10)

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
    
    # Play frog sound every 5 seconds during gameplay
    current_time = pygame.time.get_ticks()
    
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
                # only process collision if human can currently be hit
                if mosquito.rect.colliderect(human.rect) and getattr(human, 'can_be_hit', True):
                    # show dying image when player touches human, but let it continue falling
                    try:
                        human.touch()
                    except Exception:
                        # fallback: remove if touch() not available
                        human.kill()
                    score += points_per_human
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
            audio.death_sound.play()
            mosquito.rect.centerx = int(caught_pos[0])
            mosquito.rect.centery = int(caught_pos[1])
        # Game over when mosquito is pulled into frog's mouth
        if game_started and frog.is_mosquito_eaten():
            game_over = True

    screen.blit(images.game_background, (0, 0))
    mosquito.draw(screen)
    frog.draw(screen)

    humans_group.draw(screen)
    
    # Pixelated swamp-style score display
    score_bg = pygame.Surface((200, 50))
    score_bg.fill((20, 40, 20))  # Dark swamp green background
    score_bg.set_alpha(180)
    screen.blit(score_bg, (5, 5))
    
    score_text = score_font.render(f"SCORE:{score}", False, (150, 255, 100))  # Bright swamp green
    screen.blit(score_text, (12, 12))

    if paused:
        # Dark swampy overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 25, 10))
        screen.blit(overlay, (0, 0))
        
        # PAUSED title with swamp style
        pause_text = big_font.render("PAUSED", False, (200, 255, 150))
        pause_bg = pygame.Surface((pause_text.get_width() + 40, pause_text.get_height() + 20))
        pause_bg.fill((30, 60, 30))
        pause_bg.set_alpha(220)
        screen.blit(pause_bg, (WIDTH // 2 - pause_text.get_width() // 2 - 20, HEIGHT // 2 - 110))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, (150, 255, 100), 
                        pygame.Rect(WIDTH // 2 - pause_text.get_width() // 2 - 20, HEIGHT // 2 - 110,
                                   pause_text.get_width() + 40, pause_text.get_height() + 20), 5)
        
        # Pixelated swamp-styled buttons
        restart_button = pygame.Rect(WIDTH//2 - 180, HEIGHT//2, 110, 50)
        resume_button = pygame.Rect(WIDTH//2 - 55, HEIGHT//2, 110, 50)
        quit_button = pygame.Rect(WIDTH//2 + 70, HEIGHT//2, 110, 50)
        mouse_pos = pygame.mouse.get_pos()
        
        # RESTART button
        restart_hover = restart_button.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (80, 180, 60) if restart_hover else (50, 140, 40), restart_button)
        pygame.draw.rect(screen, (150, 255, 100) if restart_hover else (100, 200, 80), restart_button, 4)
        restart_text = font.render("Restart", False, (255, 255, 255) if restart_hover else (200, 255, 180))
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                   restart_button.centery - restart_text.get_height() // 2))
        
        # RESUME button
        resume_hover = resume_button.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (80, 180, 60) if resume_hover else (50, 140, 40), resume_button)
        pygame.draw.rect(screen, (150, 255, 100) if resume_hover else (100, 200, 80), resume_button, 4)
        resume_text = font.render("Resume", False, (255, 255, 255) if resume_hover else (200, 255, 180))
        screen.blit(resume_text, (resume_button.centerx - resume_text.get_width() // 2,
                                  resume_button.centery - resume_text.get_height() // 2))
        
        # QUIT button
        quit_hover = quit_button.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (180, 80, 60) if quit_hover else (140, 50, 40), quit_button)
        pygame.draw.rect(screen, (255, 150, 100) if quit_hover else (200, 100, 80), quit_button, 4)
        quit_text = font.render("Quit", False, (255, 255, 255) if quit_hover else (255, 200, 180))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                quit_button.centery - quit_text.get_height() // 2))
        
        if restart_hover or resume_hover or quit_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    if stun_timer > 0 and game_started and not game_over:
        msg = font.render("sucking blood!", False, (255, 100, 100))
        screen.blit(msg, (mosquito.centerx - msg.get_width() // 2, max(0, mosquito.rect.top - msg.get_height() - 6)))

    if not game_started:
        countdown_text = font.render(str(max(1, 3 - int(elapsed))), False, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    if pause_countdown_start > 0:
        countdown_text = big_font.render(str(max(1, 3 - int(pause_countdown_elapsed))), False, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - 150))

    if game_over:
        # Dark swampy overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 25, 10))  # Dark swamp green
        screen.blit(overlay, (0, 0))
        
        # HUGE game over title with pixelated swamp style
        game_over_message = "YOU WIN!" if game_won else "GAME OVER"
        game_over_text = title_font.render(game_over_message, False, (255, 255, 100) if game_won else (255, 100, 100))
        
        # Background panel for game over text
        game_over_bg = pygame.Surface((game_over_text.get_width() + 60, game_over_text.get_height() + 30))
        game_over_bg.fill((30, 60, 30) if game_won else (60, 30, 30))  # Swamp colored
        game_over_bg.set_alpha(220)
        screen.blit(game_over_bg, (WIDTH // 2 - game_over_text.get_width() // 2 - 30, HEIGHT // 2 - 150))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 135))
        
        # Thick pixelated border around game over text
        game_over_border = pygame.Rect(WIDTH // 2 - game_over_text.get_width() // 2 - 30, HEIGHT // 2 - 150,
                                        game_over_text.get_width() + 60, game_over_text.get_height() + 30)
        border_color = (200, 255, 150) if game_won else (255, 150, 150)
        pygame.draw.rect(screen, border_color, game_over_border, 6)
        
        # Pixelated swamp-styled buttons
        restart_button = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 20, 130, 60)
        quit_button = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 20, 130, 60)
        mouse_pos = pygame.mouse.get_pos()
        
        # RESTART button
        restart_hover = restart_button.collidepoint(mouse_pos)
        restart_bg_color = (80, 180, 60) if restart_hover else (50, 140, 40)
        restart_border_color = (150, 255, 100) if restart_hover else (100, 200, 80)
        pygame.draw.rect(screen, restart_bg_color, restart_button)
        pygame.draw.rect(screen, restart_border_color, restart_button, 5)
        
        restart_text = font.render("RESTART", False, (255, 255, 255) if restart_hover else (200, 255, 180))
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                   restart_button.centery - restart_text.get_height() // 2))
        
        # QUIT button
        quit_hover = quit_button.collidepoint(mouse_pos)
        quit_bg_color = (180, 80, 60) if quit_hover else (140, 50, 40)
        quit_border_color = (255, 150, 100) if quit_hover else (200, 100, 80)
        pygame.draw.rect(screen, quit_bg_color, quit_button)
        pygame.draw.rect(screen, quit_border_color, quit_button, 5)
        
        quit_text = font.render("QUIT", False, (255, 255, 255) if quit_hover else (255, 200, 180))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                quit_button.centery - quit_text.get_height() // 2))
        
        if restart_hover or quit_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    pygame.display.flip()

pygame.quit()
sys.exit()

