"""
FROGEATO ULTRA EXTREME - Professional Edition
==============================================
A visually stunning, professionally designed arcade survival game
"""

import pygame
import sys
import random
import math
from entities.fly import Mosquito
from entities.frog import Frog
from entities.human import Human
from entities.powerup import PowerUp, PowerUpManager
from entities.effects import ParticleSystem, ComboSystem
import images

WIDTH, HEIGHT = 1024, 768
FPS = 60
BOTTOM_MARGIN = 200

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FROGEATO ULTRA EXTREME - Professional Edition")
clock = pygame.time.Clock()
images.load_images()

# Professional font hierarchy
font_tiny = pygame.font.SysFont("Arial", 12, bold=True)
font_small = pygame.font.SysFont("Arial", 16, bold=True)
font_medium = pygame.font.SysFont("Arial", 24, bold=True)
font = pygame.font.SysFont("Arial", 32, bold=True)
font_large = pygame.font.SysFont("Arial", 48, bold=True)
font_huge = pygame.font.SysFont("Arial", 72, bold=True)
font_mega = pygame.font.SysFont("Arial", 96, bold=True)

# Professional color palette
COLORS = {
    'primary': (100, 255, 200),
    'secondary': (255, 200, 100),
    'accent': (255, 100, 150),
    'gold': (255, 215, 0),
    'success': (100, 255, 100),
    'danger': (255, 80, 80),
    'warning': (255, 200, 50),
    'info': (100, 200, 255),
    'dark': (20, 20, 30),
    'light': (240, 240, 250),
    'glass': (255, 255, 255, 30),
}

class FrogType:
    NORMAL = "normal"
    FAST = "fast"
    TANK = "tank"
    SNIPER = "sniper"
    BOSS = "boss"

class GameSettings:
    difficulty_mult = 1.0
    wave_number = 1
    kills_this_wave = 0
    coins = 0
    dash_unlocked = False
    shield_duration_upgrade = 0
    max_health = 100
    mosquito_base_size = 70
    size_growth_rate = 0.5
    
    total_kills = 0
    highest_combo = 0
    total_coins_earned = 0
    bosses_defeated = 0
    golden_humans_caught = 0

class StarField:
    def __init__(self):
        self.stars = []
        for _ in range(150):
            self.stars.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'size': random.randint(1, 3),
                'brightness': random.randint(100, 255)
            })
    
    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, WIDTH)
    
    def draw(self, surf):
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(surf, color, (int(star['x']), int(star['y'])), star['size'])

starfield = StarField()

def draw_glass_panel(surf, rect, color=None, border_color=None, border_width=2):
    if color is None:
        color = COLORS['glass']
    
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*COLORS['dark'], 180), panel.get_rect(), border_radius=15)
    
    glass_overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(glass_overlay, color, glass_overlay.get_rect(), border_radius=15)
    panel.blit(glass_overlay, (0, 0))
    
    shine = pygame.Surface((rect.width, rect.height // 3), pygame.SRCALPHA)
    for i in range(rect.height // 3):
        alpha = int(30 * (1 - i / (rect.height // 3)))
        pygame.draw.rect(shine, (255, 255, 255, alpha), (0, i, rect.width, 1))
    panel.blit(shine, (0, 0))
    
    surf.blit(panel, rect.topleft)
    
    if border_color:
        pygame.draw.rect(surf, border_color, rect, border_width, border_radius=15)

def draw_text_outline(surf, text, font, x, y, color, outline=(0, 0, 0), outline_width=3):
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                t = font.render(text, True, outline)
                surf.blit(t, (x + dx, y + dy))
    surf.blit(font.render(text, True, color), (x, y))

def draw_gradient_text(surf, text, font, x, y, color1, color2):
    text_surf = font.render(text, True, color1)
    w, h = text_surf.get_size()
    
    gradient = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(gradient, (r, g, b), (0, i), (w, i))
    
    gradient.blit(text_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(gradient, (x, y))

def create_modern_button(text, x, y, w, h, color, hover_color, mouse_pos, font_obj=font, icon=None):
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(mouse_pos)
    
    time_val = pygame.time.get_ticks() * 0.003
    pulse = abs(math.sin(time_val)) * 10
    
    if hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
        glow_surf = pygame.Surface((w + 40, h + 40), pygame.SRCALPHA)
        for i in range(20):
            alpha = int(50 * (1 - i / 20))
            glow_rect = pygame.Rect(20 - i, 20 - i, w + i * 2, h + i * 2)
            pygame.draw.rect(glow_surf, (*hover_color, alpha), glow_rect, border_radius=15 + i)
        screen.blit(glow_surf, (x - 20, y - 20))
        
        shadow_rect = rect.copy()
        shadow_rect.y += 2
        draw_glass_panel(screen, shadow_rect, (*COLORS['dark'], 100))
        draw_glass_panel(screen, rect, (*hover_color, 200), hover_color, 3)
    else:
        draw_glass_panel(screen, rect, (*color, 150), color, 2)
    
    text_color = COLORS['light'] if hover else (200, 200, 200)
    if hover:
        glow_text = font_obj.render(text, True, (*hover_color, 150))
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            screen.blit(glow_text, (rect.centerx - font_obj.size(text)[0] // 2 + offset[0],
                                   rect.centery - font_obj.size(text)[1] // 2 + offset[1]))
    
    text_surf = font_obj.render(text, True, text_color)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))
    
    return rect, hover

def start_screen():
    particles = []
    title_time = 0
    menu_alpha = 0
    
    while True:
        screen.fill(COLORS['dark'])
        starfield.update()
        starfield.draw(screen)
        
        for i in range(HEIGHT):
            alpha = int(100 * (i / HEIGHT))
            pygame.draw.line(screen, (*COLORS['primary'], alpha), (0, i), (WIDTH, i))
        
        screen.blit(images.game_background, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if random.random() < 0.3:
            particles.append({
                'x': random.randint(0, WIDTH),
                'y': HEIGHT,
                'speed': random.uniform(1, 3),
                'size': random.randint(3, 8),
                'color': random.choice([COLORS['primary'], COLORS['secondary'], COLORS['gold']]),
                'alpha': 255
            })
        
        for p in particles[:]:
            p['y'] -= p['speed']
            p['alpha'] -= 2
            if p['y'] < 0 or p['alpha'] <= 0:
                particles.remove(p)
            else:
                s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
                color_with_alpha = (*p['color'], int(p['alpha']))
                pygame.draw.circle(s, color_with_alpha, (p['size'], p['size']), p['size'])
                screen.blit(s, (p['x'], p['y']))
        
        title_time += 0.03
        title_y_offset = math.sin(title_time) * 15
        title_y = HEIGHT // 2 - 200 + title_y_offset
        
        draw_text_outline(screen, "FROGEATO", font_mega, WIDTH // 2 - 350, title_y + 5,
                         (0, 0, 0, 150), (0, 0, 0), 0)
        
        draw_gradient_text(screen, "FROGEATO", font_mega, WIDTH // 2 - 350, title_y,
                          COLORS['primary'], COLORS['secondary'])
        
        subtitle_pulse = abs(math.sin(title_time * 2)) * 20
        draw_text_outline(screen, "ULTRA EXTREME", font_large, WIDTH // 2 - 220, title_y + 100,
                         (*COLORS['accent'], int(200 + subtitle_pulse)), COLORS['dark'], 2)
        
        badge_rect = pygame.Rect(WIDTH // 2 - 150, title_y + 160, 300, 40)
        draw_glass_panel(screen, badge_rect, (*COLORS['gold'], 50), COLORS['gold'], 2)
        draw_text_outline(screen, "PROFESSIONAL EDITION", font_small, WIDTH // 2 - 130, title_y + 170,
                         COLORS['gold'], COLORS['dark'], 1)
        
        menu_alpha = min(255, menu_alpha + 5)
        
        stats_rect = pygame.Rect(20, 20, 300, 180)
        draw_glass_panel(screen, stats_rect, COLORS['glass'], COLORS['primary'], 2)
        
        stats_title = font_medium.render("PLAYER STATS", True, COLORS['primary'])
        screen.blit(stats_title, (35, 30))
        
        stats_data = [
            (f"Total Kills: {GameSettings.total_kills}", COLORS['light']),
            (f"Coins: {GameSettings.coins}", COLORS['gold']),
            (f"Best Combo: {GameSettings.highest_combo}x", COLORS['accent']),
            (f"Bosses: {GameSettings.bosses_defeated}", COLORS['danger']),
            (f"Golden Humans: {GameSettings.golden_humans_caught}", COLORS['gold'])
        ]
        
        for i, (text, color) in enumerate(stats_data):
            stat_surf = font_small.render(text, True, color)
            screen.blit(stat_surf, (35, 65 + i * 22))
        
        button_y_start = HEIGHT // 2 + 50
        
        start_btn, start_hover = create_modern_button(
            "START GAME", WIDTH // 2 - 200, button_y_start, 400, 70,
            COLORS['success'], COLORS['primary'], mouse_pos, font_large
        )
        
        shop_btn, shop_hover = create_modern_button(
            "UPGRADE SHOP", WIDTH // 2 - 200, button_y_start + 90, 400, 70,
            COLORS['warning'], COLORS['gold'], mouse_pos, font_large
        )
        
        quit_btn, quit_hover = create_modern_button(
            "QUIT", WIDTH // 2 - 200, button_y_start + 180, 400, 70,
            COLORS['danger'], (255, 100, 100), mouse_pos, font_large
        )
        
        footer_text = font_tiny.render("Made with ♥ for Professional Game Development", True, (150, 150, 150))
        screen.blit(footer_text, (WIDTH // 2 - footer_text.get_width() // 2, HEIGHT - 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return "game"
                if shop_btn.collidepoint(event.pos):
                    return "shop"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        clock.tick(FPS)

def upgrade_shop():
    shop_particles = []
    
    while True:
        screen.fill(COLORS['dark'])
        starfield.update()
        starfield.draw(screen)
        screen.blit(images.game_background, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if random.random() < 0.2:
            shop_particles.append({
                'x': random.randint(0, WIDTH),
                'y': 0,
                'speed': random.uniform(0.5, 2),
                'size': random.randint(2, 5),
                'color': COLORS['gold']
            })
        
        for p in shop_particles[:]:
            p['y'] += p['speed']
            if p['y'] > HEIGHT:
                shop_particles.remove(p)
            else:
                pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
        
        draw_gradient_text(screen, "UPGRADE SHOP", font_huge, WIDTH // 2 - 280, 40,
                          COLORS['gold'], COLORS['secondary'])
        
        coins_rect = pygame.Rect(WIDTH // 2 - 150, 130, 300, 60)
        draw_glass_panel(screen, coins_rect, (*COLORS['gold'], 50), COLORS['gold'], 3)
        
        coin_icon_size = 40
        pygame.draw.circle(screen, COLORS['gold'], (WIDTH // 2 - 100, 160), coin_icon_size // 2)
        draw_text_outline(screen, "$", font_large, WIDTH // 2 - 110, 140, COLORS['dark'], COLORS['gold'], 1)
        
        coins_text = font_large.render(f"{GameSettings.coins}", True, COLORS['gold'])
        screen.blit(coins_text, (WIDTH // 2 - 50, 140))
        
        upgrades = [
            {"name": "Max Health +20", "cost": 50, "id": "health", "desc": "Increase survivability", "color": COLORS['success']},
            {"name": "Unlock DASH", "cost": 100, "id": "dash", "desc": "Press SPACE to dash", "color": COLORS['info']},
            {"name": "Shield Duration +50%", "cost": 75, "id": "shield", "desc": "Longer invincibility", "color": COLORS['warning']},
            {"name": "Start with Power-up", "cost": 150, "id": "start_powerup", "desc": "Begin with advantage", "color": COLORS['accent']},
            {"name": "Golden Human Magnet", "cost": 200, "id": "magnet", "desc": "Attract golden humans", "color": COLORS['gold']},
        ]
        
        buttons = []
        for i, upgrade in enumerate(upgrades):
            y = 220 + i * 90
            can_afford = GameSettings.coins >= upgrade["cost"]
            
            already_owned = False
            if upgrade["id"] == "dash" and GameSettings.dash_unlocked:
                already_owned = True
            
            card_rect = pygame.Rect(WIDTH // 2 - 350, y, 700, 75)
            
            if already_owned:
                draw_glass_panel(screen, card_rect, (*COLORS['success'], 30), COLORS['success'], 2)
                status_text = "OWNED"
                status_color = COLORS['success']
            elif can_afford:
                draw_glass_panel(screen, card_rect, (*upgrade['color'], 50), upgrade['color'], 2)
                status_text = f"${upgrade['cost']}"
                status_color = COLORS['gold']
            else:
                draw_glass_panel(screen, card_rect, (*COLORS['dark'], 100), (80, 80, 80), 2)
                status_text = f"${upgrade['cost']}"
                status_color = (120, 120, 120)
            
            name_surf = font_medium.render(upgrade["name"], True, COLORS['light'] if (can_afford or already_owned) else (120, 120, 120))
            screen.blit(name_surf, (WIDTH // 2 - 330, y + 12))
            
            desc_surf = font_small.render(upgrade["desc"], True, (180, 180, 180) if (can_afford or already_owned) else (100, 100, 100))
            screen.blit(desc_surf, (WIDTH // 2 - 330, y + 42))
            
            status_surf = font_large.render(status_text, True, status_color)
            screen.blit(status_surf, (WIDTH // 2 + 200, y + 20))
            
            buttons.append((card_rect, upgrade, can_afford, already_owned))
        
        back_btn, back_hover = create_modern_button(
            "BACK TO MENU", WIDTH // 2 - 150, HEIGHT - 100, 300, 60,
            COLORS['danger'], (255, 100, 100), mouse_pos, font_medium
        )
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
                
                for btn, upgrade, can_afford, already_owned in buttons:
                    if btn.collidepoint(event.pos) and can_afford and not already_owned:
                        GameSettings.coins -= upgrade["cost"]
                        
                        if upgrade["id"] == "health":
                            GameSettings.max_health += 20
                        elif upgrade["id"] == "dash":
                            GameSettings.dash_unlocked = True
                        elif upgrade["id"] == "shield":
                            GameSettings.shield_duration_upgrade += 1
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        clock.tick(FPS)

def create_wave_frogs(wave_num):
    frogs = []
    
    # Always just one frog
    frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=BOTTOM_MARGIN)
    frog.set_image(images.frog_image)
    frog.frog_type = FrogType.NORMAL
    frog.rect.centerx = WIDTH // 2
    frogs.append(frog)
    
    return frogs

def reset_game():
    mosquito = Mosquito(400, 100, size=GameSettings.mosquito_base_size)
    mosquito.set_image(images.mosquito_image)
    mosquito.dash_cooldown = 0
    mosquito.dash_duration = 0
    mosquito.dash_speed = 15
    mosquito.velocity_x = 0
    mosquito.velocity_y = 0
    mosquito.acceleration = 0.8
    mosquito.max_speed = 7
    mosquito.friction = 0.85
    
    frogs = create_wave_frogs(GameSettings.wave_number)
    humans_group = pygame.sprite.Group()
    
    powerup_manager = PowerUpManager()
    particle_system = ParticleSystem()
    combo_system = ComboSystem()
    
    return (mosquito, frogs, humans_group, 0, 0, GameSettings.max_health,
            powerup_manager, particle_system, combo_system, 0, False, False)

def draw_professional_hud(score, health, wave_num, coins, combo_count, frogs_remaining, dash_cooldown):
    hud_panel = pygame.Rect(15, 15, 350, 150)
    draw_glass_panel(screen, hud_panel, COLORS['glass'], COLORS['primary'], 2)
    
    health_pct = max(0, health / GameSettings.max_health)
    health_color = COLORS['success'] if health_pct > 0.6 else COLORS['warning'] if health_pct > 0.3 else COLORS['danger']
    
    pygame.draw.rect(screen, (40, 40, 40), (30, 30, 320, 25), border_radius=12)
    pygame.draw.rect(screen, health_color, (30, 30, int(320 * health_pct), 25), border_radius=12)
    pygame.draw.rect(screen, COLORS['light'], (30, 30, 320, 25), 2, border_radius=12)
    
    hp_text = font_small.render(f"HP: {health}/{GameSettings.max_health}", True, COLORS['light'])
    screen.blit(hp_text, (35, 32))
    
    wave_surf = font_medium.render(f"WAVE {wave_num}", True, COLORS['primary'])
    screen.blit(wave_surf, (30, 65))
    
    score_surf = font_medium.render(f"SCORE: {score}", True, COLORS['light'])
    screen.blit(score_surf, (30, 95))
    
    coin_surf = font_medium.render(f"${coins}", True, COLORS['gold'])
    screen.blit(coin_surf, (30, 125))
    
    info_panel = pygame.Rect(WIDTH - 365, 15, 350, 100)
    draw_glass_panel(screen, info_panel, COLORS['glass'], COLORS['secondary'], 2)
    
    frogs_text = font_medium.render(f"FROGS: {frogs_remaining}", True, COLORS['danger'])
    screen.blit(frogs_text, (WIDTH - 350, 30))
    
    if combo_count > 1:
        combo_scale = 1 + min(combo_count / 30, 1.5)
        combo_font = pygame.font.SysFont("Arial", int(32 * combo_scale), bold=True)
        combo_text = f"{combo_count}x COMBO!"
        combo_color = COLORS['gold'] if combo_count > 10 else COLORS['accent']
        draw_text_outline(screen, combo_text, combo_font, WIDTH - 340, 65, combo_color, COLORS['dark'], 2)
    
    if GameSettings.dash_unlocked:
        dash_panel = pygame.Rect(WIDTH // 2 - 100, 15, 200, 40)
        draw_glass_panel(screen, dash_panel, COLORS['glass'], COLORS['info'], 2)
        
        if dash_cooldown > 0:
            progress = dash_cooldown / 120
            pygame.draw.rect(screen, (60, 60, 60), (WIDTH // 2 - 85, 25, 170, 20), border_radius=10)
            pygame.draw.rect(screen, COLORS['info'], (WIDTH // 2 - 85, 25, int(170 * (1 - progress)), 20), border_radius=10)
            cd_text = font_tiny.render("DASH COOLDOWN", True, COLORS['light'])
        else:
            cd_text = font_small.render("DASH READY!", True, COLORS['success'])
        
        screen.blit(cd_text, (WIDTH // 2 - cd_text.get_width() // 2, 27))

def draw_professional_hud_with_powerups(score, health, wave_num, coins, combo_count, frogs_remaining, dash_cooldown, powerup_manager):
    draw_professional_hud(score, health, wave_num, coins, combo_count, frogs_remaining, dash_cooldown)
    
    # Active power-up indicators
    active_count = 0
    current_time = pygame.time.get_ticks()
    for effect_type, data in powerup_manager.active_effects.items():
        remaining_ms = data['end_time'] - current_time
        remaining_sec = remaining_ms / 1000.0
        
        if remaining_sec > 0:
            indicator_rect = pygame.Rect(WIDTH - 240, 130 + active_count * 35, 220, 30)
            draw_glass_panel(screen, indicator_rect, (*data['info']['color'], 40), data['info']['color'], 2)
            
            powerup_text = font_small.render(f"{effect_type.upper()}: {remaining_sec:.1f}s", True, COLORS['light'])
            screen.blit(powerup_text, (WIDTH - 230, 135 + active_count * 35))
            
            active_count += 1

# MAIN
menu_result = start_screen()
if menu_result == "shop":
    upgrade_shop()
    menu_result = start_screen()

(mosquito, frogs, humans_group, score, human_spawn_timer, health,
 powerup_manager, particle_system, combo_system,
 wave_timer, game_over, game_won) = reset_game()

countdown_start = pygame.time.get_ticks()
human_spawn_interval = 3000
golden_human_spawn_interval = 10000
golden_human_timer = 0
invincibility_timer = 0
flash_timer = 0
stun_timer = 0
stun_duration = 500

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
    game_started = elapsed >= 3
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                GameSettings.wave_number = 1
                GameSettings.kills_this_wave = 0
                (mosquito, frogs, humans_group, score, human_spawn_timer, health,
                 powerup_manager, particle_system, combo_system,
                 wave_timer, game_over, game_won) = reset_game()
                countdown_start = pygame.time.get_ticks()
            
            if event.key == pygame.K_SPACE and GameSettings.dash_unlocked:
                if mosquito.dash_cooldown <= 0 and game_started and not game_over:
                    mosquito.dash_duration = 10
                    mosquito.dash_cooldown = 120
                    particle_system.add_explosion(mosquito.rect.centerx, mosquito.rect.centery, COLORS['info'], 30)
    
    if not game_over and game_started:
        keys = pygame.key.get_pressed()
        
        # Update stun timer
        if stun_timer > 0:
            stun_timer -= clock.get_time()
        
        if mosquito.dash_duration > 0:
            mosquito.dash_duration -= 1
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
            if dx != 0 or dy != 0:
                length = math.hypot(dx, dy)
                mosquito.rect.x += int((dx / length) * mosquito.dash_speed)
                mosquito.rect.y += int((dy / length) * mosquito.dash_speed)
                particle_system.add_trail(mosquito.rect.centerx, mosquito.rect.centery, COLORS['info'], 3)
        else:
            # Smooth acceleration-based movement (only if not stunned)
            if stun_timer <= 0:
                dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
                dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
                
                # Apply acceleration
                mosquito.velocity_x += dx * mosquito.acceleration
                mosquito.velocity_y += dy * mosquito.acceleration
                
                # Apply friction
                mosquito.velocity_x *= mosquito.friction
                mosquito.velocity_y *= mosquito.friction
                
                # Limit max speed
                speed = math.hypot(mosquito.velocity_x, mosquito.velocity_y)
                if speed > mosquito.max_speed:
                    mosquito.velocity_x = (mosquito.velocity_x / speed) * mosquito.max_speed
                    mosquito.velocity_y = (mosquito.velocity_y / speed) * mosquito.max_speed
                
                # Update position
                mosquito.rect.x += int(mosquito.velocity_x)
                mosquito.rect.y += int(mosquito.velocity_y)
        
        if mosquito.dash_cooldown > 0:
            mosquito.dash_cooldown -= 1
        
        new_size = int(GameSettings.mosquito_base_size + score * GameSettings.size_growth_rate)
        new_size = min(new_size, 150)
        if mosquito.size != new_size:
            old_center = mosquito.rect.center
            mosquito.size = new_size
            mosquito.rect = pygame.Rect(0, 0, new_size, new_size)
            mosquito.rect.center = old_center
        
        mosquito.clamp_to_area(pygame.Rect(0, 0, WIDTH, HEIGHT - BOTTOM_MARGIN))
        
        human_spawn_timer += clock.get_time()
        if human_spawn_timer >= human_spawn_interval:
            humans_group.add(Human(WIDTH, HEIGHT))
            human_spawn_timer = 0
        
        golden_human_timer += clock.get_time()
        if golden_human_timer >= golden_human_spawn_interval:
            golden_human = Human(WIDTH, HEIGHT)
            golden_human.is_golden = True
            golden_human.worth = 5
            humans_group.add(golden_human)
            golden_human_timer = 0
            particle_system.add_explosion(golden_human.rect.centerx, golden_human.rect.centery, COLORS['gold'], 50)
        
        humans_group.update()
        
        for human in humans_group:
            if getattr(human, 'dying', False):
                continue
            if mosquito.rect.colliderect(human.rect):
                human.dying = True
                human.dying_until = pygame.time.get_ticks() + 500
                
                is_golden = getattr(human, 'is_golden', False)
                worth = getattr(human, 'worth', 1)
                
                points = int(combo_system.multiplier * 10 * worth)
                coins_earned = int(combo_system.multiplier * worth * (10 if is_golden else 1))
                
                score += points
                GameSettings.coins += coins_earned
                combo_system.add_catch(human.rect.centerx, human.rect.centery, points)
                
                if is_golden:
                    GameSettings.golden_humans_caught += 1
                    particle_system.add_explosion(human.rect.centerx, human.rect.centery, COLORS['gold'], 100)
                else:
                    particle_system.add_collect_effect(human.rect.centerx, human.rect.centery)
                break
        
        powerup_manager.update(dt, WIDTH, HEIGHT, BOTTOM_MARGIN)
        collected_powerup = powerup_manager.check_collision(mosquito.rect)
        if collected_powerup:
            particle_system.add_sparkle(mosquito.rect.centerx, mosquito.rect.centery)
        
        active_frogs = []
        for frog in frogs:
            if not hasattr(frog, 'dead'):
                frog.dead = False
            if not frog.dead:
                frog.update((mosquito.centerx, mosquito.centery), game_started, game_over)
                active_frogs.append(frog)
                
                if invincibility_timer <= 0 and not powerup_manager.has_shield() and not powerup_manager.has_invincibility():
                    if frog.check_hit((mosquito.centerx, mosquito.centery), mosquito.size / 2):
                        health -= 25
                        invincibility_timer = 60
                        flash_timer = 30
                        particle_system.add_explosion(mosquito.rect.centerx, mosquito.rect.centery, COLORS['danger'], 40)
                        combo_system.combo_count = 0
                        combo_system.multiplier = 1.0
                        
                        if health <= 0:
                            game_over = True
                            GameSettings.total_kills += score // 10
        
        frogs = active_frogs

    
    if invincibility_timer > 0:
        invincibility_timer -= 1
    if flash_timer > 0:
        flash_timer -= 1
    
    combo_system.update(dt)
    particle_system.update()
    starfield.update()
    
    screen.fill(COLORS['dark'])
    starfield.draw(screen)
    
    screen.blit(images.game_background, (0, 0))
    
    for human in humans_group:
        human.image = images.get_current_human_frame()
        
        if getattr(human, 'is_golden', False):
            glow_size = human.rect.width + 20
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 30
            pygame.draw.circle(glow_surf, (*COLORS['gold'], int(100 + pulse)),
                             (glow_size // 2, glow_size // 2), glow_size // 2)
            screen.blit(glow_surf, (human.rect.x - 10, human.rect.y - 10))
        
        screen.blit(human.image, (human.rect.x, human.rect.y))
    
    powerup_manager.draw(screen)
    particle_system.draw(screen)
    
    for frog in frogs:
        frog.draw(screen)
        if hasattr(frog, 'health') and frog.health > 1:
            bar_w = 100
            bar_h = 10
            bar_x = frog.rect.centerx - bar_w // 2
            bar_y = frog.rect.top - 20
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
            health_w = int(bar_w * (frog.health / (5 + GameSettings.wave_number // 5)))
            pygame.draw.rect(screen, COLORS['success'], (bar_x, bar_y, health_w, bar_h), border_radius=5)
    
    if invincibility_timer > 0 and flash_timer % 10 < 5:
        pass
    else:
        mosquito.draw(screen)
    
    # Show "SUCKING BLOOD!" message when stunned
    if stun_timer > 0 and game_started and not game_over:
        stun_text = font.render("SUCKING BLOOD!", True, COLORS['danger'])
        text_x = mosquito.rect.centerx - stun_text.get_width() // 2
        text_y = max(0, mosquito.rect.top - stun_text.get_height() - 10)
        
        # Pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 10
        glow_surf = pygame.Surface((stun_text.get_width() + 20, stun_text.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLORS['danger'], int(100 + pulse)), glow_surf.get_rect(), border_radius=10)
        screen.blit(glow_surf, (text_x - 10, text_y - 5))
        screen.blit(stun_text, (text_x, text_y))
    
    draw_professional_hud(score, health, GameSettings.wave_number, GameSettings.coins,
                         combo_system.combo_count, len(frogs), mosquito.dash_cooldown)
    
    if not game_started:
        countdown_val = max(1, 3 - int(elapsed))
        countdown_surf = font_mega.render(str(countdown_val), True, COLORS['gold'])
        pos = (WIDTH // 2 - countdown_surf.get_width() // 2, HEIGHT // 2 - 100)
        
        for offset in [(5, 5), (-5, -5), (5, -5), (-5, 5)]:
            glow = font_mega.render(str(countdown_val), True, (*COLORS['primary'], 100))
            screen.blit(glow, (pos[0] + offset[0], pos[1] + offset[1]))
        
        screen.blit(countdown_surf, pos)
    
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLORS['dark'], 230))
        screen.blit(overlay, (0, 0))
        
        # Animated panel with pulse effect
        pulse_scale = 1 + abs(math.sin(pygame.time.get_ticks() * 0.002)) * 0.02
        panel_w = int(600 * pulse_scale)
        panel_h = int(450 * pulse_scale)
        panel_rect = pygame.Rect(WIDTH // 2 - panel_w // 2, HEIGHT // 2 - panel_h // 2, panel_w, panel_h)
        draw_glass_panel(screen, panel_rect, (*COLORS['danger'], 50), COLORS['danger'], 3)
        
        # Animated title
        title_offset = math.sin(pygame.time.get_ticks() * 0.003) * 5
        draw_gradient_text(screen, "GAME OVER", font_huge, WIDTH // 2 - 240, HEIGHT // 2 - 170 + title_offset,
                          COLORS['danger'], COLORS['accent'])
        
        stats = [
            f"Final Score: {score}",
            f"Coins Earned: {GameSettings.coins}",
            f"Best Combo: {GameSettings.highest_combo}x",
            f"Golden Humans: {GameSettings.golden_humans_caught}"
        ]
        
        for i, stat in enumerate(stats):
            stat_surf = font_medium.render(stat, True, COLORS['light'])
            screen.blit(stat_surf, (WIDTH // 2 - stat_surf.get_width() // 2, HEIGHT // 2 - 80 + i * 40))
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        restart_btn, restart_hover = create_modern_button(
            "RESTART", WIDTH // 2 - 220, HEIGHT // 2 + 120, 200, 50,
            COLORS['success'], COLORS['primary'], mouse_pos, font_medium
        )
        
        menu_btn, menu_hover = create_modern_button(
            "MENU", WIDTH // 2 + 20, HEIGHT // 2 + 120, 200, 50,
            COLORS['warning'], COLORS['gold'], mouse_pos, font_medium
        )
        
        # Handle button clicks in game over state
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    GameSettings.wave_number = 1
                    GameSettings.kills_this_wave = 0
                    (mosquito, frogs, humans_group, score, human_spawn_timer, health,
                     powerup_manager, particle_system, combo_system,
                     wave_timer, game_over, game_won) = reset_game()
                    countdown_start = pygame.time.get_ticks()
                    stun_timer = 0
                elif menu_btn.collidepoint(event.pos):
                    game_over = False
                    menu_result = start_screen()
                    if menu_result == "shop":
                        upgrade_shop()
                        menu_result = start_screen()
                    GameSettings.wave_number = 1
                    (mosquito, frogs, humans_group, score, human_spawn_timer, health,
                     powerup_manager, particle_system, combo_system,
                     wave_timer, game_over, game_won) = reset_game()
                    countdown_start = pygame.time.get_ticks()
                    stun_timer = 0
    
    pygame.display.flip()

pygame.quit()
sys.exit()
