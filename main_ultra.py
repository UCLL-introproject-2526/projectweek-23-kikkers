"""
FROGEATO ULTRA - The Ultimate Swamp Survival Experience
========================================================
A fast-paced arcade game with power-ups, combos, and epic frog battles!

Features:
- Dynamic power-up system
- Combo multipliers
- Screen shake and particles
- Smooth movement mechanics
- Multiple difficulty levels
- Professional UI/HUD
"""

import pygame
import sys
import random
import math
from entities.fly import Mosquito
from entities.frog import Frog
from entities.human import Human
from entities.powerup import PowerUp, PowerUpManager
from entities.effects import ParticleSystem, ScreenShake, ComboSystem
import images

# Game constants
WIDTH, HEIGHT = 1024, 768
FPS = 60
BOTTOM_MARGIN = 200

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FROGEATO ULTRA")
clock = pygame.time.Clock()

# Load images after display is created
images.load_images()

# Fonts
font_small = pygame.font.SysFont("Arial", 18, bold=True)
font = pygame.font.SysFont("Arial", 32, bold=True)
font_large = pygame.font.SysFont("Arial", 48, bold=True)
font_huge = pygame.font.SysFont("Arial", 72, bold=True)

# Game settings
class Settings:
    difficulty = "NORMAL"  # EASY, NORMAL, HARD, INSANE
    sound_enabled = True
    music_enabled = True
    
    @classmethod
    def get_difficulty_multiplier(cls):
        multipliers = {"EASY": 0.7, "NORMAL": 1.0, "HARD": 1.4, "INSANE": 2.0}
        return multipliers.get(cls.difficulty, 1.0)


def draw_text_with_outline(surface, text, font, x, y, color, outline_color=(0, 0, 0)):
    """Draw text with outline for better visibility."""
    # Draw outline
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
        outline_surf = font.render(text, True, outline_color)
        surface.blit(outline_surf, (x + dx, y + dy))
    # Draw main text
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))


def create_button(text, x, y, width, height, color, hover_color, mouse_pos):
    """Create an interactive button and return if it's clicked."""
    rect = pygame.Rect(x, y, width, height)
    is_hover = rect.collidepoint(mouse_pos)
    
    # Draw button with glow effect when hovering
    if is_hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # Glow effect
        glow_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*hover_color, 100), glow_surf.get_rect(), border_radius=8)
        screen.blit(glow_surf, (x - 5, y - 5))
        pygame.draw.rect(screen, hover_color, rect, border_radius=5)
    else:
        pygame.draw.rect(screen, color, rect, border_radius=5)
    
    # Draw button border
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=5)
    
    # Draw text
    text_surf = font.render(text, True, (255, 255, 255) if is_hover else (200, 200, 200))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return rect, is_hover


def start_screen():
    """Enhanced start screen with animated background."""
    firefly_particles = []
    title_wobble = 0
    
    # Create fireflies
    for _ in range(30):
        firefly_particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-0.5, 0.5),
            'glow': random.uniform(0, 2 * math.pi)
        })
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Draw background
        screen.blit(images.game_background, (0, 0))
        
        # Update and draw fireflies
        for firefly in firefly_particles:
            firefly['x'] += firefly['vx']
            firefly['y'] += firefly['vy']
            firefly['glow'] += 0.05
            
            # Wrap around screen
            if firefly['x'] < 0: firefly['x'] = WIDTH
            if firefly['x'] > WIDTH: firefly['x'] = 0
            if firefly['y'] < 0: firefly['y'] = HEIGHT
            if firefly['y'] > HEIGHT: firefly['y'] = 0
            
            # Draw glow
            glow_amount = abs(math.sin(firefly['glow']))
            glow_size = int(8 * glow_amount) + 2
            glow_surf = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 150, int(150 * glow_amount)), 
                             (glow_size * 2, glow_size * 2), glow_size * 2)
            screen.blit(glow_surf, (firefly['x'] - glow_size * 2, firefly['y'] - glow_size * 2))
        
        # Animated title
        title_wobble += 0.05
        title_offset = math.sin(title_wobble) * 10
        
        # Draw title with shadow
        title_y = HEIGHT // 3 + title_offset
        draw_text_with_outline(screen, "FROGEATO", font_huge, 
                              WIDTH // 2 - 200, title_y - 50, (100, 255, 100))
        draw_text_with_outline(screen, "ULTRA", font_large, 
                              WIDTH // 2 - 80, title_y + 20, (255, 255, 100))
        
        # Subtitle
        subtitle_text = "Survive the Swamp!"
        subtitle_surf = font.render(subtitle_text, True, (200, 200, 200))
        screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, title_y + 80))
        
        # Buttons
        button_y = HEIGHT // 2 + 80
        start_rect, start_hover = create_button("START GAME", WIDTH // 2 - 120, button_y, 
                                                240, 50, (50, 150, 50), (100, 255, 100), mouse_pos)
        
        options_rect, options_hover = create_button("OPTIONS", WIDTH // 2 - 120, button_y + 70, 
                                                    240, 50, (100, 100, 200), (150, 150, 255), mouse_pos)
        
        credits_rect, credits_hover = create_button("CREDITS", WIDTH // 2 - 120, button_y + 140, 
                                                    240, 50, (150, 100, 150), (200, 150, 200), mouse_pos)
        
        quit_rect, quit_hover = create_button("QUIT", WIDTH // 2 - 120, button_y + 210, 
                                              240, 50, (150, 50, 50), (255, 100, 100), mouse_pos)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return
                if options_rect.collidepoint(event.pos):
                    options_menu()
                if credits_rect.collidepoint(event.pos):
                    credits_screen()
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def options_menu():
    """Options menu for difficulty and settings."""
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        screen.blit(images.game_background, (0, 0))
        
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        draw_text_with_outline(screen, "OPTIONS", font_huge, WIDTH // 2 - 150, 80, (255, 255, 100))
        
        # Difficulty selection
        diff_y = 220
        draw_text_with_outline(screen, "DIFFICULTY:", font, WIDTH // 2 - 150, diff_y, (255, 255, 255))
        
        difficulties = ["EASY", "NORMAL", "HARD", "INSANE"]
        for i, diff in enumerate(difficulties):
            x = WIDTH // 2 - 300 + i * 160
            color = (100, 255, 100) if Settings.difficulty == diff else (100, 100, 100)
            hover_color = (150, 255, 150) if Settings.difficulty == diff else (150, 150, 150)
            
            diff_rect, diff_hover = create_button(diff, x, diff_y + 60, 140, 45, 
                                                   color, hover_color, mouse_pos)
            
            # Check if clicked
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and diff_rect.collidepoint(event.pos):
                    Settings.difficulty = diff
        
        # Back button
        back_rect, back_hover = create_button("BACK", WIDTH // 2 - 100, HEIGHT - 150, 
                                              200, 50, (100, 100, 100), (150, 150, 150), mouse_pos)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return


def credits_screen():
    """Credits screen."""
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        screen.blit(images.game_background, (0, 0))
        
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        draw_text_with_outline(screen, "CREDITS", font_huge, WIDTH // 2 - 150, 80, (255, 255, 100))
        
        # Credits text
        credits_lines = [
            "FROGEATO ULTRA",
            "",
            "Game Design & Development",
            "Your Amazing Team",
            "",
            "Special Thanks",
            "GitHub Copilot",
            "",
            "Made with Python & Pygame",
            "",
            "© 2025 All Rights Reserved"
        ]
        
        y = 200
        for line in credits_lines:
            if line:
                text_surf = font_small.render(line, True, (200, 200, 200))
                screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))
            y += 35
        
        # Back button
        back_rect, back_hover = create_button("BACK", WIDTH // 2 - 100, HEIGHT - 150, 
                                              200, 50, (100, 100, 100), (150, 150, 150), mouse_pos)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return


def reset_game():
    """Initialize/reset all game state."""
    mosquito = Mosquito(400, 100, size=70)
    mosquito.set_image(images.mosquito_image)
    
    frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=BOTTOM_MARGIN)
    frog.set_image(images.frog_image)
    
    humans_group = pygame.sprite.Group()
    powerup_manager = PowerUpManager()
    particle_system = ParticleSystem()
    screen_shake = ScreenShake()
    combo_system = ComboSystem()
    
    return (mosquito, frog, humans_group, powerup_manager, particle_system, 
            screen_shake, combo_system, 0, 0, 0, False, False, False, 0, 100)


def draw_hud(screen, score, health, combo_system, powerup_manager, wave):
    """Draw professional HUD."""
    # Health bar
    health_bar_width = 200
    health_bar_height = 25
    health_x = 20
    health_y = 20
    
    # Health background
    pygame.draw.rect(screen, (100, 0, 0), (health_x, health_y, health_bar_width, health_bar_height), border_radius=5)
    # Health fill
    health_fill = int((health / 100) * health_bar_width)
    health_color = (0, 255, 0) if health > 50 else (255, 200, 0) if health > 25 else (255, 0, 0)
    pygame.draw.rect(screen, health_color, (health_x, health_y, health_fill, health_bar_height), border_radius=5)
    # Health border
    pygame.draw.rect(screen, (255, 255, 255), (health_x, health_y, health_bar_width, health_bar_height), 3, border_radius=5)
    # Health text
    health_text = font_small.render(f"HP: {health}/100", True, (255, 255, 255))
    screen.blit(health_text, (health_x + 5, health_y + 3))
    
    # Score
    score_text = font.render(f"SCORE: {score}", True, (255, 255, 100))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    
    # Wave
    wave_text = font_small.render(f"WAVE: {wave}", True, (150, 200, 255))
    screen.blit(wave_text, (WIDTH - wave_text.get_width() - 20, 70))
    
    # Combo
    if combo_system.combo_count > 1:
        combo_text = combo_system.get_combo_text()
        combo_color = (255, 100, 255) if combo_system.multiplier >= 5 else (255, 200, 0)
        draw_text_with_outline(screen, combo_text, font, WIDTH // 2 - 150, 20, combo_color)
    
    # Active power-ups
    powerup_y = 100
    for effect_type, data in powerup_manager.active_effects.items():
        remaining = (data['end_time'] - pygame.time.get_ticks()) / 1000
        text = f"{data['info']['name']}: {remaining:.1f}s"
        powerup_text = font_small.render(text, True, data['info']['color'])
        screen.blit(powerup_text, (20, powerup_y))
        powerup_y += 25


# Show start screen
start_screen()

# Initialize game
(mosquito, frog, humans_group, powerup_manager, particle_system, screen_shake, 
 combo_system, stun_timer, human_spawn_timer, score, game_won, game_over, 
 paused, pause_countdown_start, health) = reset_game()

countdown_start_time = pygame.time.get_ticks()
countdown_played = False
stun_duration = 500
human_spawn_interval = 5000
win_score = 50  # Higher win score
wave = 1
health = 100

running = True
while running:
    delta_time = clock.tick(FPS)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elapsed = (pygame.time.get_ticks() - countdown_start_time) / 1000
    game_started = elapsed >= 3

    if stun_timer > 0:
        stun_timer -= delta_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                (mosquito, frog, humans_group, powerup_manager, particle_system, screen_shake, 
                 combo_system, stun_timer, human_spawn_timer, score, game_won, game_over, 
                 paused, pause_countdown_start, health) = reset_game()
                countdown_start_time = pygame.time.get_ticks()
                countdown_played = False
                wave = 1
            if event.key == pygame.K_SPACE and game_started and not game_over:
                paused = not paused
            if event.key == pygame.K_ESCAPE:
                running = False

    # Game logic (when not paused)
    if game_started and not paused and not game_over:
        # Movement
        if stun_timer <= 0:
            mosquito.handle_input(pygame.key.get_pressed())
        mosquito.clamp_to_area(pygame.Rect(0, 0, WIDTH, HEIGHT - BOTTOM_MARGIN))
        
        # Update systems
        powerup_manager.update(delta_time, WIDTH, HEIGHT, BOTTOM_MARGIN)
        combo_system.update(delta_time)
        particle_system.update()
        screen_shake.update()
        humans_group.update()
        frog.update((mosquito.centerx, mosquito.centery), game_started, game_over)
        
        # Spawn humans with wave difficulty
        human_spawn_timer += delta_time
        spawn_interval = human_spawn_interval / Settings.get_difficulty_multiplier()
        if human_spawn_timer >= spawn_interval:
            humans_group.add(Human(WIDTH, HEIGHT))
            human_spawn_timer = 0
        
        # Check power-up collection
        collected = powerup_manager.check_collision(mosquito.rect)
        for powerup in collected:
            particle_system.add_sparkle(powerup.rect.centerx, powerup.rect.centery, powerup.info['color'])
        
        # Check human collection
        for human in humans_group:
            if getattr(human, 'dying', False):
                continue
            if mosquito.rect.colliderect(human.rect):
                human.dying = True
                human.dying_until = pygame.time.get_ticks() + stun_duration
                
                # Add score with combo
                base_points = int(10 * Settings.get_difficulty_multiplier())
                points = combo_system.add_catch(human.rect.centerx, human.rect.centery, base_points)
                score += int(points * powerup_manager.get_points_multiplier())
                
                particle_system.add_collect_effect(human.rect.centerx, human.rect.centery)
                stun_timer = stun_duration
                
                # Check win
                if score >= win_score:
                    game_over = True
                    game_won = True
                    particle_system.add_explosion(mosquito.centerx, mosquito.centery, (255, 255, 0), 50)
                break
        
        # Check tongue collision
        if frog.check_hit((mosquito.centerx, mosquito.centery), mosquito.size / 2):
            if not powerup_manager.has_shield():
                health -= 34  # 3 hits = death
                screen_shake.start(15, 20)
                particle_system.add_explosion(mosquito.centerx, mosquito.centery, (255, 0, 0), 30)
                if health <= 0:
                    game_over = True
                    combo_system.combo_count = 0
        
        # Check if tongue caught mosquito
        caught_pos = frog.get_caught_mosquito_position()
        if caught_pos and not game_over:
            if not powerup_manager.has_invincibility():
                mosquito.rect.centerx = int(caught_pos[0])
                mosquito.rect.centery = int(caught_pos[1])
        
        # Death by eating
        if game_started and frog.is_mosquito_eaten() and not powerup_manager.has_shield():
            health = 0
            game_over = True
    
    # Draw everything with screen shake
    shake_offset = screen_shake.get_offset()
    
    # Background
    screen.blit(images.game_background, shake_offset)
    
    # Particles (background layer)
    particle_system.draw(screen)
    
    # Game objects
    mosquito.draw(screen)
    frog.draw(screen)
    humans_group.draw(screen)
    powerup_manager.draw(screen)
    
    # Effects (foreground layer)
    combo_system.draw(screen)
    
    # HUD
    draw_hud(screen, score, health, combo_system, powerup_manager, wave)
    
    # Stun message
    if stun_timer > 0 and game_started and not game_over:
        msg = font.render("Sucking Blood!", True, (255, 100, 100))
        screen.blit(msg, (mosquito.centerx - msg.get_width() // 2, 
                         max(0, mosquito.rect.top - msg.get_height() - 6)))
    
    # Countdown
    if not game_started:
        countdown_num = max(1, 3 - int(elapsed))
        draw_text_with_outline(screen, str(countdown_num), font_huge, 
                              WIDTH // 2 - 40, HEIGHT // 2 - 50, (255, 255, 100))
    
    # Game Over
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        if game_won:
            draw_text_with_outline(screen, "VICTORY!", font_huge, WIDTH // 2 - 180, HEIGHT // 2 - 150, (255, 255, 0))
        else:
            draw_text_with_outline(screen, "GAME OVER", font_huge, WIDTH // 2 - 220, HEIGHT // 2 - 150, (255, 100, 100))
        
        final_score = font_large.render(f"FINAL SCORE: {score}", True, (255, 255, 255))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 50))
        
        mouse_pos = pygame.mouse.get_pos()
        restart_rect, _ = create_button("RESTART", WIDTH // 2 - 120, HEIGHT // 2 + 50, 240, 50, 
                                       (50, 150, 50), (100, 255, 100), mouse_pos)
        menu_rect, _ = create_button("MAIN MENU", WIDTH // 2 - 120, HEIGHT // 2 + 120, 240, 50, 
                                     (100, 100, 200), (150, 150, 255), mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    (mosquito, frog, humans_group, powerup_manager, particle_system, screen_shake, 
                     combo_system, stun_timer, human_spawn_timer, score, game_won, game_over, 
                     paused, pause_countdown_start, health) = reset_game()
                    countdown_start_time = pygame.time.get_ticks()
                    wave = 1
                if menu_rect.collidepoint(event.pos):
                    start_screen()
                    (mosquito, frog, humans_group, powerup_manager, particle_system, screen_shake, 
                     combo_system, stun_timer, human_spawn_timer, score, game_won, game_over, 
                     paused, pause_countdown_start, health) = reset_game()
                    countdown_start_time = pygame.time.get_ticks()
                    wave = 1
    
    pygame.display.flip()

pygame.quit()
sys.exit()
