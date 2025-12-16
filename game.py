import pygame
import sys
import random
import math

#Code werkt maar problemen met tong 
WIDTH, HEIGHT = 900, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog vs Fly Pro Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

def main():
    pygame.init()

def start_screen():
    button_width = 200
    button_height = 50
    start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)
    quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)
    
    while True: #Startscherm
        screen.fill((0, 0, 0))  
        title_text = font.render("Frog vs Fly Pro Mode", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 60))
        
        # Startknop
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = font.render("Start", True, (0, 0, 0))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
        
        # Quitknop
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        quit_text = font.render("Quit", True, (0, 0, 0))
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

start_screen()

mosquito_size = 30
mosquito_color = (200, 50, 50)
mosquito = pygame.Rect(400, 400, mosquito_size, mosquito_size)
speed = 5

frog_size = 150
frog_color = (50, 200, 50)
top_margin = 200
frog_space = pygame.Rect(0, 0, screen.get_width(), top_margin)
frog = pygame.Rect(0, 0, frog_size, frog_size)
frog.center = frog_space.center

tongue_color = (255, 100, 100)
tongue_active = False
tongue_length = 0
max_tongue_length = 400
tongue_speed = 25
tongue_width = 20
tongue_dx, tongue_dy = 0, 0  

attack_timer = random.randint(60, 180)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
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

    # if not tongue_active:
    #     attack_timer -= 1
    #     if attack_timer <= 0:
    #         tongue_active = True
    #         tongue_length = 0
    #         dx = mosquito.centerx - frog.centerx
    #         dy = mosquito.centery - frog.centery
    #         dist = math.hypot(dx, dy)
    #         if dist == 0: dist = 1
    #         tongue_dx = dx / dist
    #         tongue_dy = dy / dist
    #         attack_timer = random.randint(60, 180)

    # if tongue_active:
    #     tongue_length += tongue_speed
    #     if tongue_length >= max_tongue_length:
    #         tongue_active = False

    #     end_x = frog.centerx + tongue_dx * tongue_length
    #     end_y = frog.centery + tongue_dy * tongue_length

    #     tongue_rect = pygame.draw.line(
    #         screen, tongue_color,
    #         frog.center, (end_x, end_y),
    #         tongue_width
    #     )

    #     if tongue_rect.colliderect(mosquito):
    #         print("Mosquito caught!")
    #         running = False

    screen.fill((40, 40, 40))
    pygame.draw.rect(screen, mosquito_color, mosquito)  
    pygame.draw.rect(screen, frog_color, frog)          

    pygame.display.flip()

pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()
