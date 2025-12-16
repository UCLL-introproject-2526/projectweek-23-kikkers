import pygame
import sys
import random
import math


WIDTH, HEIGHT = 1024, 768
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogeato")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

import images




class Human(pygame.sprite.Sprite):
    def __init__(self, width, height, image=None):
        super().__init__()
        # Load human head image
        try:
            self.image = pygame.image.load('assets/images/humanhead.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (72, 72))
        except:
            # Fallback to colored rectangle if image not found
            self.image = pygame.Surface((72, 72), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 200, 150), (36, 36), 36)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(1.5, 3.5)

    def update(self):
        self.rect.y += self.speed
        # remove when off bottom of screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

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

mosquito_size = 70
mosquito_color = (200, 50, 50)
mosquito = pygame.Rect(400, 100, mosquito_size, mosquito_size)
speed = 5

frog_size = 200
frog_color = (50, 200, 50)
bottom_margin = 200
frog_space = pygame.Rect(0, HEIGHT - bottom_margin, screen.get_width(), bottom_margin)
frog = pygame.Rect(0, 0, frog_size, frog_size)
frog.center = frog_space.center

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

# Humans entity group and stun timer
humans_group = pygame.sprite.Group()
stun_timer = 0  # Stun duration in milliseconds
stun_duration = 500  # 500ms stun when hitting a human
human_spawn_timer = 0  # Timer for spawning humans
human_spawn_interval = 5000  # Spawn a human every 5 seconds (in milliseconds)
# Score / win
score = 0
win_score = 10
game_won = False

def point_line_distance(px, py, x1, y1, x2, y2):
    line_mag = math.hypot(x2 - x1, y2 - y1)
    if line_mag == 0:
        return math.hypot(px - x1, py - y1)
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
    u = max(min(u, 1), 0)  
    closest_x = x1 + u * (x2 - x1)
    closest_y = y1 + u * (y2 - y1)
    return math.hypot(px - closest_x, py - closest_y)

running = True
while running:
    clock.tick(FPS)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elapsed = (pygame.time.get_ticks() - countdown_start_time) / 1000
    game_started = elapsed >= 3

    # Update stun timer
    if stun_timer > 0:
        stun_timer -= clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            mosquito = pygame.Rect(400, 100, mosquito_size, mosquito_size)
            tongue_active = False
            tongue_length = 0
            attack_timer = random.randint(60, 120)
            stun_timer = 0
            human_spawn_timer = 0
            score = 0
            game_won = False
            humans_group.empty()
            countdown_start_time = pygame.time.get_ticks()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                game_over = False
                mosquito = pygame.Rect(400, 100, mosquito_size, mosquito_size)
                tongue_active = False
                tongue_length = 0
                attack_timer = random.randint(60, 120)
                stun_timer = 0
                human_spawn_timer = 0
                score = 0
                game_won = False
                humans_group.empty()
                countdown_start_time = pygame.time.get_ticks()
            if quit_button.collidepoint(event.pos):
                running = False

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        # Only allow movement if not stunned
        if stun_timer <= 0:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                mosquito.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                mosquito.x += speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                mosquito.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                mosquito.y += speed

        play_area = pygame.Rect(0, 0, screen.get_width(), screen.get_height() - bottom_margin)
        mosquito.clamp_ip(play_area)

    # Update humans
    humans_group.update()
    
    # Spawn humans every 5 seconds
    if game_started and not game_over:
        human_spawn_timer += clock.get_time()
        if human_spawn_timer >= human_spawn_interval:
            new_human = Human(WIDTH, HEIGHT)
            humans_group.add(new_human)
            human_spawn_timer = 0
    
    # Check collision between mosquito and humans
    if game_started and not game_over:
        # Check collision with all humans in the group
        for human in humans_group:
            if mosquito.colliderect(human.rect):
                human.kill()  # Remove the human
                score += 1
                stun_timer = stun_duration  # Apply stun
                # Win check
                if score >= win_score:
                    game_over = True
                    game_won = True
                break  # Only process one collision per frame

    

    if game_started and not game_over and not tongue_active:
        attack_timer -= 1
        if attack_timer <= 0:
            tongue_active = True
            tongue_length = 0
            retracting = False
            dx = mosquito.centerx - frog.centerx
            dy = mosquito.centery - frog.centery
            dist = math.hypot(dx, dy)
            if dist == 0: dist = 1
            tongue_dx = dx / dist
            tongue_dy = dy / dist
            attack_timer = random.randint(60, 180)

    if game_started and tongue_active:
        if not retracting:
            if not game_over:
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

        if point_line_distance(mosquito.centerx, mosquito.centery,
                               frog.centerx, frog.centery,
                               end_x, end_y) < (tongue_width / 2 + mosquito_size / 2):
            game_over = True

    screen.blit(images.game_background, (0, 0))
    screen.blit(images.mosquito_image, mosquito.topleft)
    screen.blit(images.frog_image, frog.topleft)
    
    # Draw humans
    humans_group.draw(screen)

    # Draw score HUD
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # If stunned, show sucking message above the mosquito
    if stun_timer > 0 and game_started and not game_over:
        msg = font.render("sucking blood!", True, (255, 255, 255))
        msg_x = mosquito.centerx - msg.get_width() // 2
        msg_y = max(0, mosquito.top - msg.get_height() - 6)
        screen.blit(msg, (msg_x, msg_y))

    if tongue_active:
        pygame.draw.line(
            screen, tongue_color,
            frog.center, (end_x, end_y),
            tongue_width
        )

    if not game_started:
        countdown_num = max(1, 3 - int(elapsed))
        countdown_text = font.render(str(countdown_num), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if game_won:
            game_over_text = font.render("You Win!", True, (255, 255, 255))
        else:
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

