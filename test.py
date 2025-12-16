import pygame
import sys
import random
import math

# --------------------------- Settings ---------------------------
WIDTH, HEIGHT = 900, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE_SKY = (50, 150, 255)
RED = (200,50,50)
YELLOW = (255,255,0)
GREEN = (50,180,50)
DARK_GREEN = (20,120,20)
GRAY = (200,200,200)

# Fly settings
FLY_SPEED = 6
FLY_WING_FLAP_RATE = 5

# Tongue settings
TONGUE_SPEED_MIN = 15
TONGUE_SPEED_MAX = 25
TONGUE_MAX_LENGTH = 600
TONGUE_WIDTH = 8
TONGUE_COOLDOWN = 40  # frames before next tongue

# Particle settings
PARTICLE_LIFETIME = 20
PARTICLE_COUNT = 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog vs Fly Pro Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# --------------------------- Pixel Frog & Fly ---------------------------
def create_pixel_frog():
    frog = pygame.Surface((40,30), pygame.SRCALPHA)
    frog.fill((0,0,0,0))
    pygame.draw.rect(frog, GREEN, (0,10,40,20))
    pygame.draw.rect(frog, DARK_GREEN, (10,0,20,15))
    pygame.draw.rect(frog, BLACK, (10,5,5,5))
    pygame.draw.rect(frog, BLACK, (25,5,5,5))
    return frog

def create_pixel_fly():
    fly1 = pygame.Surface((20,20), pygame.SRCALPHA)
    fly1.fill((0,0,0,0))
    pygame.draw.circle(fly1, YELLOW, (10,10),10)
    pygame.draw.circle(fly1, BLACK, (7,7),3)
    pygame.draw.circle(fly1, BLACK, (13,7),3)
    fly2 = pygame.Surface((20,20), pygame.SRCALPHA)
    fly2.fill((0,0,0,0))
    pygame.draw.circle(fly2, YELLOW, (10,10),10)
    pygame.draw.circle(fly2, BLACK, (6,8),3)
    pygame.draw.circle(fly2, BLACK, (14,8),3)
    return [fly1, fly2]  # for flapping animation

# --------------------------- Particle Class ---------------------------
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2,4)
        self.color = WHITE
        self.lifetime = PARTICLE_LIFETIME
        self.vx = random.uniform(-2,2)
        self.vy = random.uniform(-2,0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -=1

    def draw(self, screen, camera_y):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y - camera_y)), self.radius)

# --------------------------- Fly Class ---------------------------
class Fly:
    def __init__(self, x, y, images):
        self.rect = images[0].get_rect(center=(x,y))
        self.images = images
        self.current_frame = 0
        self.frame_timer = 0
        self.speed = FLY_SPEED

    def move(self, keys):
        if keys[pygame.K_w] and self.rect.top - self.speed > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom + self.speed < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left - self.speed > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right + self.speed < WIDTH:
            self.rect.x += self.speed

    def animate(self):
        self.frame_timer +=1
        if self.frame_timer % FLY_WING_FLAP_RATE ==0:
            self.current_frame = (self.current_frame +1) % len(self.images)

    def draw(self, screen, camera_y):
        screen.blit(self.images[self.current_frame], (self.rect.x, self.rect.y - camera_y))

# --------------------------- Tongue Class ---------------------------
class Tongue:
    def __init__(self, frog, fly, particles):
        self.frog = frog
        self.fly = fly
        self.width = TONGUE_WIDTH
        self.length = 0
        self.max_length = TONGUE_MAX_LENGTH
        self.speed = random.randint(TONGUE_SPEED_MIN, TONGUE_SPEED_MAX)
        self.extending = True
        self.particles = particles

    def update(self):
        # Horizontal follow
        self.frog.rect.centerx += (self.fly.rect.centerx - self.frog.rect.centerx) * 0.05

        if self.extending:
            self.length += self.speed
            if self.length >= self.max_length:
                self.extending = False
        else:
            self.length -= self.speed
            # Generate particles when retracting
            for _ in range(PARTICLE_COUNT):
                self.particles.append(Particle(self.frog.rect.centerx, self.frog.rect.bottom + self.length))
            if self.length <=0:
                return False
        return True

    def get_rect(self):
        return pygame.Rect(self.frog.rect.centerx - self.width//2, self.frog.rect.bottom, self.width, self.length)

    def draw(self, screen, camera_y):
        rect = self.get_rect()
        pygame.draw.rect(screen, RED, (rect.x, rect.y - camera_y, rect.width, rect.height))

# --------------------------- Frog Class ---------------------------
class Frog:
    def __init__(self, x, y, image):
        self.rect = image.get_rect(center=(x,y))
        self.image = image

    def draw(self, screen, camera_y):
        screen.blit(self.image, (self.rect.x, self.rect.y - camera_y))

# --------------------------- Menu ---------------------------
def draw_menu():
    screen.fill(BLUE_SKY)
    title = font.render("Frog vs Fly Pro", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    button_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2, 200, 60)
    pygame.draw.rect(screen, GREEN, button_rect)
    button_text = font.render("NEW GAME", True, BLACK)
    screen.blit(button_text, (WIDTH//2 - button_text.get_width()//2, HEIGHT//2+5))
    pygame.display.flip()
    return button_rect

def menu_loop():
    while True:
        button_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

# --------------------------- Main Game ---------------------------
def main():
    menu_loop()

    fly_images = create_pixel_fly()
    fly = Fly(WIDTH//2, HEIGHT-50, fly_images)
    frog_img = create_pixel_frog()
    frogs = [
        Frog(WIDTH//4, 50, frog_img),
        Frog(WIDTH//2, 50, frog_img),
        Frog(WIDTH*3//4, 50, frog_img)
    ]

    tongue = None
    tongue_cooldown = 0
    score = 0
    particles = []
    camera_y = 0

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update fly
        fly.move(keys)
        fly.animate()
        camera_y = fly.rect.y - HEIGHT//2

        # Tongue
        if tongue is None and tongue_cooldown <=0:
            shooter = random.choice(frogs)
            tongue = Tongue(shooter, fly, particles)
            tongue_cooldown = TONGUE_COOLDOWN
        elif tongue_cooldown >0:
            tongue_cooldown -=1

        if tongue:
            if not tongue.update():
                tongue = None

        # Update particles
        particles = [p for p in particles if p.lifetime>0]
        for p in particles:
            p.update()

        # Collision check
        if tongue and fly.rect.colliderect(tongue.get_rect()):
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()

        # Draw background (vertical scrolling)
        screen.fill(BLUE_SKY)
        for i in range(-1, HEIGHT//100 +2):
            pygame.draw.rect(screen, GRAY, (0, i*100 - camera_y%100, WIDTH, 50))

        # Draw frogs
        for f in frogs:
            f.draw(screen, camera_y)

        # Draw tongue
        if tongue:
            tongue.draw(screen, camera_y)

        # Draw particles
        for p in particles:
            p.draw(screen, camera_y)

        # Draw fly
        fly.draw(screen, camera_y)

        # Score
        score +=1
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT-50))

        pygame.display.flip()

if __name__ == "__main__":
    main()
