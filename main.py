import pygame
import sys
from entities.fly import Mosquito
from entities.frog import Frog


WIDTH, HEIGHT = 1024, 768
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogeato")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

import images


def main():
    pygame.init()

def start_screen(): #Startscherm
    button_width = 200
    button_height = 50
    start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)

    while True:
        screen.blit(images.game_background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Hover
        start_color = (255, 255, 255) if start_button.collidepoint(mouse_pos) else (0, 0, 0)
        quit_color = (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0)

        if start_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        title_text = font.render("Frogeato", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2,
                                 HEIGHT // 2 - title_text.get_height() // 2 - 60))

        # Startknop
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = font.render("Start", True, start_color)
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                 start_button.centery - start_text.get_height() // 2))

        # Quitknop
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

start_screen() 

countdown_start_time = pygame.time.get_ticks()
game_over = False
restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 80, 40)
quit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2, 80, 40)

# Create mosquito using Mosquito class
mosquito = Mosquito(400, 100, size=70)
mosquito.set_image(images.mosquito_image)

# Create frog using Frog class
bottom_margin = 200
frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=bottom_margin)
frog.set_image(images.frog_image)

running = True
while running:
    clock.tick(FPS)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elapsed = (pygame.time.get_ticks() - countdown_start_time) / 1000
    game_started = elapsed >= 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                game_over = False
                mosquito = Mosquito(400, 100, size=70)
                mosquito.set_image(images.mosquito_image)
                frog.reset()
                countdown_start_time = pygame.time.get_ticks()
            if quit_button.collidepoint(event.pos):
                running = False

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        mosquito.handle_input(keys)
        play_area = pygame.Rect(0, 0, screen.get_width(), screen.get_height() - bottom_margin)
        mosquito.clamp_to_area(play_area)

    # Update frog (handles tongue shooting and AI)
    frog.update((mosquito.centerx, mosquito.centery), game_started, game_over)
    
    # Check collision
    if game_started and frog.check_hit((mosquito.centerx, mosquito.centery), mosquito.size / 2):
        game_over = True

    screen.blit(images.game_background, (0, 0))
    mosquito.draw(screen)
    frog.draw(screen)

    if not game_started:
        countdown_num = max(1, 3 - int(elapsed))
        countdown_text = font.render(str(countdown_num), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        restart_color = (255, 255, 255) if restart_button.collidepoint(mouse_pos) else (0, 0, 0)
        quit_color = (255, 255, 255) if quit_button.collidepoint(mouse_pos) else (0, 0, 0)
        if restart_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        restart_text = font.render("Restart", True, restart_color)
        quit_text = font.render("Quit", True, quit_color)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()
