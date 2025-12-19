import pygame
import os
import pygame
import sys
import random
import audio
from entities.fly import Mosquito
from entities.frog import Frog
import asyncio
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


async def main():
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
    
    # Load the legendary Silkscreen font
    try:
        font_small = pygame.font.Font("Silkscreen-Regular.ttf", 20)
        font = pygame.font.Font("Silkscreen-Regular.ttf", 32)
        big_font = pygame.font.Font("Silkscreen-Regular.ttf", 64)
        title_font = pygame.font.Font("Silkscreen-Regular.ttf", 100)
        huge_font = pygame.font.Font("Silkscreen-Regular.ttf", 120)
    except:
        # Fallback just in case
        font_small = pygame.font.SysFont("Arial", 20, bold=True)
        font = pygame.font.SysFont("Arial", 32, bold=True)
        big_font = pygame.font.SysFont("Arial", 64, bold=True)
        title_font = pygame.font.SysFont("Arial", 100, bold=True)
        huge_font = pygame.font.SysFont("Arial", 120, bold=True)

    # Load images after display is initialized
    import images
    images.load_images()


    async def start_screen():
        import math
        
        # Swamp aesthetic particles
        fireflies = []
        water_ripples = []
        lily_pads = []
        mist_particles = []
        
        # Initialize fireflies (glowing swamp lights)
        for _ in range(25):
            fireflies.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT - 200),
                'size': random.randint(2, 5),
                'speed': random.uniform(0.3, 1.0),
                'glow': random.randint(0, 360),
                'brightness': random.uniform(0.5, 1.0),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.8, 0.2)
            })
        
        # Initialize lily pads
        for _ in range(8):
            lily_pads.append({
                'x': random.randint(50, WIDTH - 50),
                'y': random.randint(HEIGHT - 250, HEIGHT - 100),
                'size': random.randint(40, 70),
                'rotation': random.uniform(0, 360),
                'bob': random.uniform(0, math.pi * 2)
            })
        
        # Initialize mist
        for _ in range(15):
            mist_particles.append({
                'x': random.randint(-100, WIDTH),
                'y': random.randint(HEIGHT // 2, HEIGHT),
                'size': random.randint(60, 150),
                'speed': random.uniform(0.1, 0.4),
                'alpha': random.randint(10, 40)
            })
        
        button_width = 350
        button_height = 70
        button_spacing = 20
        start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)
        quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80 + button_height + button_spacing, button_width, button_height)
        
        time_offset = 0
        ripple_timer = 0

        while True:
            time_offset += 0.02
            ripple_timer += 1
            
            # Draw base background
            screen.blit(images.game_background, (0, 0))
            
            # Draw atmospheric gradient overlay (swamp fog)
            gradient_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(HEIGHT):
                alpha = int(30 * (i / HEIGHT))
                color = (15, 35, 25, alpha)  # Dark greenish overlay
                pygame.draw.line(gradient_surf, color, (0, i), (WIDTH, i))
            screen.blit(gradient_surf, (0, 0))
            
            # Draw mist particles
            for mist in mist_particles:
                mist['x'] += mist['speed']
                if mist['x'] > WIDTH + 100:
                    mist['x'] = -100
                    mist['y'] = random.randint(HEIGHT // 2, HEIGHT)
                
                mist_surf = pygame.Surface((mist['size'], mist['size']), pygame.SRCALPHA)
                pygame.draw.circle(mist_surf, (200, 220, 200, mist['alpha']), 
                                 (mist['size'] // 2, mist['size'] // 2), mist['size'] // 2)
                screen.blit(mist_surf, (int(mist['x']), int(mist['y'])))
            
            # Draw lily pads with bobbing animation
            for pad in lily_pads:
                pad['bob'] += 0.02
                bob_offset = math.sin(pad['bob']) * 3
                
                lily_surf = pygame.Surface((pad['size'], pad['size']), pygame.SRCALPHA)
                # Outer darker green
                pygame.draw.ellipse(lily_surf, (40, 80, 40), lily_surf.get_rect())
                # Inner lighter green
                inner_rect = pygame.Rect(5, 5, pad['size'] - 10, pad['size'] - 10)
                pygame.draw.ellipse(lily_surf, (60, 120, 60), inner_rect)
                # Add a notch (lily pad characteristic)
                pygame.draw.line(lily_surf, (40, 80, 40), 
                               (pad['size'] // 2, 0), 
                               (pad['size'] // 2, pad['size'] // 4), 4)
                
                screen.blit(lily_surf, (int(pad['x']), int(pad['y'] + bob_offset)))
            
            # Spawn water ripples occasionally
            if ripple_timer > 60 and random.random() < 0.05:
                water_ripples.append({
                    'x': random.randint(100, WIDTH - 100),
                    'y': random.randint(HEIGHT - 250, HEIGHT - 100),
                    'radius': 0,
                    'max_radius': random.randint(40, 80),
                    'alpha': 255
                })
                ripple_timer = 0
            
            # Draw water ripples
            for ripple in water_ripples[:]:
                ripple['radius'] += 1.5
                ripple['alpha'] = max(0, ripple['alpha'] - 5)
                
                if ripple['alpha'] <= 0 or ripple['radius'] > ripple['max_radius']:
                    water_ripples.remove(ripple)
                else:
                    ripple_surf = pygame.Surface((int(ripple['radius'] * 2 + 10), int(ripple['radius'] * 2 + 10)), pygame.SRCALPHA)
                    pygame.draw.circle(ripple_surf, (100, 180, 150, ripple['alpha']), 
                                     (int(ripple['radius'] + 5), int(ripple['radius'] + 5)), 
                                     int(ripple['radius']), 2)
                    screen.blit(ripple_surf, (int(ripple['x'] - ripple['radius']), int(ripple['y'] - ripple['radius'])))
            
            # Draw fireflies with glow effect
            for fly in fireflies:
                fly['x'] += fly['dx']
                fly['y'] += fly['dy']
                fly['glow'] = (fly['glow'] + 3) % 360
                
                # Wrap around screen
                if fly['x'] < 0: fly['x'] = WIDTH
                if fly['x'] > WIDTH: fly['x'] = 0
                if fly['y'] < 0: fly['y'] = HEIGHT - 200
                if fly['y'] > HEIGHT - 200: fly['y'] = 0
                
                # Pulsing glow effect
                pulse = abs(math.sin(math.radians(fly['glow']))) * fly['brightness']
                glow_size = int(fly['size'] * 3 * pulse)
                
                if glow_size > 0:
                    glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                    for i in range(glow_size, 0, -2):
                        alpha = int(100 * (i / glow_size) * pulse)
                        pygame.draw.circle(glow_surf, (255, 255, 150, alpha), 
                                         (glow_size, glow_size), i)
                    screen.blit(glow_surf, (int(fly['x'] - glow_size), int(fly['y'] - glow_size)))
                
                # Core light
                core_brightness = int(200 + 55 * pulse)
                pygame.draw.circle(screen, (core_brightness, core_brightness, 100), 
                                 (int(fly['x']), int(fly['y'])), fly['size'])
            
            mouse_pos = pygame.mouse.get_pos()

            # Animated title with swamp glow
            title_y = HEIGHT // 2 - 180
            title_float = math.sin(time_offset * 2) * 8
            
            # Title glow layers
            for offset in [8, 6, 4, 2]:
                glow_alpha = int(40 * (offset / 8))
                glow_color = (50, 200, 100, glow_alpha)
                glow_surf = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
                glow_title = title_font.render("Frogeato", True, glow_color)
                glow_surf.blit(glow_title, (WIDTH // 2 - glow_title.get_width() // 2 + offset, 
                                           title_y + offset + title_float - 50))
                screen.blit(glow_surf, (0, 50))
            
            # Main title with shadow
            title_shadow = title_font.render("Frogeato", True, (10, 30, 20))
            screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 4, 
                                      title_y + title_float + 4))
            title_text = title_font.render("Frogeato", True, (100, 255, 150))
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 
                                    title_y + title_float))
            
            # Subtitle
            subtitle = font.render("The Swamp Chronicles", True, (150, 200, 160))
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_y + 110))
            
            # Draw stylish swamp-themed buttons
            for button, text, color_base in [(start_button, "Start Adventure", (60, 150, 80)), 
                                              (quit_button, "Leave Swamp", (150, 80, 60))]:
                is_hover = button.collidepoint(mouse_pos)
                
                if is_hover:
                    # Hover glow effect
                    glow_rect = button.inflate(20, 20)
                    glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    pulse_glow = abs(math.sin(time_offset * 3)) * 30
                    for i in range(10, 0, -1):
                        alpha = int(pulse_glow * (i / 10))
                        rect = pygame.Rect(10 - i, 10 - i, glow_rect.width - 2 * (10 - i), 
                                         glow_rect.height - 2 * (10 - i))
                        pygame.draw.rect(glow_surf, (*color_base, alpha), rect, border_radius=15)
                    screen.blit(glow_surf, (glow_rect.x, glow_rect.y))
                
                # Button base (darker)
                pygame.draw.rect(screen, (20, 35, 25), button, border_radius=12)
                
                # Button fill with gradient effect
                button_inner = button.inflate(-6, -6)
                if is_hover:
                    brightness_mult = 1.3
                else:
                    brightness_mult = 1.0
                
                inner_color = tuple(int(c * brightness_mult) for c in color_base)
                pygame.draw.rect(screen, inner_color, button_inner, border_radius=10)
                
                # Button border
                border_color = (150, 200, 150) if is_hover else (80, 120, 90)
                pygame.draw.rect(screen, border_color, button, 3, border_radius=12)
                
                # Button text with glow
                if is_hover:
                    text_glow = font.render(text, True, (200, 255, 200))
                    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                        screen.blit(text_glow, (button.centerx - text_glow.get_width() // 2 + dx, 
                                               button.centery - text_glow.get_height() // 2 + dy))
                
                button_text = font.render(text, True, (255, 255, 255))
                screen.blit(button_text, (button.centerx - button_text.get_width() // 2, 
                                         button.centery - button_text.get_height() // 2))
            
            # Set cursor
            if start_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()
            await asyncio.sleep(1/FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        # Ripple effect on click
                        for _ in range(5):
                            water_ripples.append({
                                'x': event.pos[0] + random.randint(-20, 20),
                                'y': event.pos[1] + random.randint(-20, 20),
                                'radius': 0,
                                'max_radius': random.randint(60, 100),
                                'alpha': 255
                            })
                        await asyncio.sleep(0.3)
                        return
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            await asyncio.sleep(0)


    def reset_game():
        mosquito = Mosquito(400, 100, size=70)
        mosquito.set_image(images.mosquito_image)
        mosquito.set_wing_images(images.mosquito_wingup, images.mosquito_wingdown)
        frog = Frog(WIDTH, HEIGHT, size=200, bottom_margin=200)
        frog.set_image(images.frog_image)
        frog.set_open_image(images.frog_tong_image)
        humans_group = pygame.sprite.Group()
        return mosquito, frog, humans_group, 0, 0, 0, False, False, False, 0


    await start_screen()

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
                restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
                resume_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
                quit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
                if restart_button.collidepoint(event.pos):
                    mosquito, frog, humans_group, stun_timer, human_spawn_timer, score, game_won, game_over, paused, pause_countdown_start = reset_game()
                    countdown_start_time = pygame.time.get_ticks()
                    countdown_played = False
                if resume_button.collidepoint(event.pos):
                    paused = False
                if quit_button.collidepoint(event.pos):
                    running = False
            if (game_over or game_won) and event.type == pygame.MOUSEBUTTONDOWN:
                restart_button = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 80, 150, 50)
                quit_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 80, 150, 50)
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
        
        # Clean, simple score display with dark swamp feel
        import math
        
        # Dark panel background
        panel = pygame.Surface((320, 110), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 25, 20, 220), (0, 0, 320, 110), border_radius=12)
        pygame.draw.rect(panel, (50, 80, 60, 255), (0, 0, 320, 110), 3, border_radius=12)
        screen.blit(panel, (15, 15))
        
        # Score text - clean and readable
        score_label = font_small.render("SCORE", True, (140, 180, 150))
        screen.blit(score_label, (30, 30))
        
        score_str = str(score)
        score_text = big_font.render(score_str, True, (180, 220, 180))
        screen.blit(score_text, (30, 55))
        
        # Goal indicator
        goal_text = font_small.render(f"Goal: {win_score}", True, (120, 160, 130))
        screen.blit(goal_text, (200, 95))

        if paused:
            # Simple dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 20, 15, 180))
            screen.blit(overlay, (0, 0))
            
            # Clean pause title
            pause_text = huge_font.render("PAUSED", True, (140, 200, 160))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 180))
            
            # Simple, clean buttons
            restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
            resume_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
            quit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
            mouse_pos = pygame.mouse.get_pos()
            
            if restart_button.collidepoint(mouse_pos) or resume_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
            # Draw clean buttons
            for button, text, base_color in [(restart_button, "RESTART", (60, 120, 80)),
                                               (resume_button, "RESUME", (70, 140, 90)),
                                               (quit_button, "QUIT", (120, 60, 50))]:
                is_hover = button.collidepoint(mouse_pos)
                
                # Simple button style
                bg_color = base_color if not is_hover else tuple(min(255, int(c * 1.3)) for c in base_color)
                pygame.draw.rect(screen, (15, 25, 20), button, border_radius=8)
                pygame.draw.rect(screen, bg_color, button.inflate(-4, -4), border_radius=6)
                pygame.draw.rect(screen, (100, 150, 120) if is_hover else (60, 100, 80), button, 2, border_radius=8)
                
                # Text
                button_text = font.render(text, True, (240, 250, 240))
                screen.blit(button_text, (button.centerx - button_text.get_width() // 2,
                                         button.centery - button_text.get_height() // 2))

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
            # LEGENDARY SWAMP GAME OVER SCREEN
            import math
            time_val = pygame.time.get_ticks() * 0.001
            
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Dark murky water overlay with ripples
            for i in range(0, HEIGHT, 3):
                ripple = math.sin(i * 0.03 + time_val * 1.5) * 8
                alpha = 160 + int(ripple)
                pygame.draw.rect(overlay, (10, 25, 20, alpha), (0, i, WIDTH, 3))
            screen.blit(overlay, (0, 0))
            
            # Falling swamp leaves/debris
            for i in range(30):
                leaf_x = (pygame.time.get_ticks() * 0.03 + i * 33) % WIDTH
                leaf_y = (pygame.time.get_ticks() * 0.02 + i * 27) % HEIGHT
                leaf_rot = (time_val + i) * 50
                leaf_size = 12 + int(math.sin(time_val + i) * 4)
                
                leaf_surf = pygame.Surface((leaf_size * 2, leaf_size * 2), pygame.SRCALPHA)
                pygame.draw.ellipse(leaf_surf, (60, 100, 50, 180), (0, 0, leaf_size * 2, leaf_size))
                screen.blit(leaf_surf, (int(leaf_x), int(leaf_y)))
            
            # Main result panel
            panel_width = 700
            panel_height = 450
            panel_x = WIDTH // 2 - panel_width // 2
            panel_y = HEIGHT // 2 - panel_height // 2
            
            panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            
            # Lily pads around the panel
            for i in range(8):
                angle = (i / 8) * 3.14159 * 2 + time_val * 0.5
                pad_x = int(panel_width // 2 + math.cos(angle) * (panel_width // 2 + 40))
                pad_y = int(panel_height // 2 + math.sin(angle) * (panel_height // 2 + 40))
                pad_size = 50 + int(math.sin(time_val * 2 + i) * 8)
                
                # Shadow
                pygame.draw.ellipse(panel_surf, (10, 20, 15, 150),
                                  (pad_x - pad_size//2 + 3, pad_y - pad_size//2 + 3, pad_size, pad_size))
                # Lily pad
                pygame.draw.ellipse(panel_surf, (50, 110, 60, 230),
                                  (pad_x - pad_size//2, pad_y - pad_size//2, pad_size, pad_size))
                # Highlight
                pygame.draw.ellipse(panel_surf, (80, 150, 90, 180),
                                  (pad_x - pad_size//2 + 5, pad_y - pad_size//2 + 5, pad_size - 15, pad_size - 15))
            
            # Dark swamp panel background
            pygame.draw.rect(panel_surf, (15, 30, 25, 240), (50, 50, panel_width - 100, panel_height - 100), border_radius=30)
            
            # Glowing border animation
            border_pulse = abs(math.sin(time_val * 3)) * 30
            border_color = (80 + int(border_pulse), 180 + int(border_pulse), 100 + int(border_pulse))
            
            # Multiple border layers for depth
            for thickness in [8, 5, 2]:
                alpha = int(255 * (thickness / 8))
                pygame.draw.rect(panel_surf, (*border_color, alpha), 
                               (50, 50, panel_width - 100, panel_height - 100), thickness, border_radius=30)
            
            # Simple dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 20, 15, 200))
            screen.blit(overlay, (0, 0))
            
            # Title
            title_text = "VICTORY!" if game_won else "GAME OVER"
            title_color = (160, 220, 140) if game_won else (220, 140, 140)
            title = huge_font.render(title_text, True, title_color)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 180))
            
            # Score
            score_label = font.render("Final Score", True, (140, 180, 150))
            screen.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, HEIGHT // 2 - 40))
            
            score_text = big_font.render(str(score), True, (180, 220, 180))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            
            # Simple buttons
            restart_button = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 80, 150, 50)
            quit_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 80, 150, 50)
            mouse_pos = pygame.mouse.get_pos()
            
            if restart_button.collidepoint(mouse_pos) or quit_button.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
            for button, text, base_color in [(restart_button, "RESTART", (60, 120, 80)),
                                              (quit_button, "QUIT", (120, 60, 50))]:
                is_hover = button.collidepoint(mouse_pos)
                
                bg_color = base_color if not is_hover else tuple(min(255, int(c * 1.3)) for c in base_color)
                pygame.draw.rect(screen, (15, 25, 20), button, border_radius=8)
                pygame.draw.rect(screen, bg_color, button.inflate(-4, -4), border_radius=6)
                pygame.draw.rect(screen, (100, 150, 120) if is_hover else (60, 100, 80), button, 2, border_radius=8)
                
                button_text = font.render(text, True, (240, 250, 240))
                screen.blit(button_text, (button.centerx - button_text.get_width() // 2,
                                         button.centery - button_text.get_height() // 2))

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    asyncio.run(main())

