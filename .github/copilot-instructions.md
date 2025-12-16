# Copilot Instructions - Kikkers Project

## Project Overview
**Kikkers** (Frogs) is a pygame-based arcade game where you play as a fly trying to eat humans while avoiding a frog's tongue. Eat 30 humans to grow large enough to defeat the frog and win!

## Game Mechanics
- **Player**: Fly controlled with W-A-S-D keys
- **Objective**: Eat 30 humans to grow large enough, then eat the frog
- **Enemy**: Frog shoots tongues from the top of screen
- **Growth System**: Fly grows at 10, 20, and 30 humans eaten (small → medium → large → mega)
- **Win Condition**: Reach 30 humans and eat the frog
- **Lose Condition**: Get hit by frog's tongue
- **Difficulty Scaling**: Humans fall faster and frog shoots more frequently as fly grows

## Technology Stack
- **Python 3.x**: Main language
- **Pygame**: Graphics, input, game loop
- **Virtual Environment**: REQUIRED for macOS/Homebrew Python (PEP 668)

## Development Setup
**CRITICAL - macOS/Homebrew Python Environment:**
```bash
# Create virtual environment (required)
python3 -m venv venv
source venv/bin/activate

# Install pygame
pip install pygame

# Run the game
python main.py
```

**Note**: Direct `pip install` without venv will fail with "externally-managed-environment" error.

## File Structure
```
kikkers/
├── main.py              # Game loop, entity manager, state transitions
├── game_states.py       # MenuState, PlayingState, WinState, LoseState
├── config.py            # All constants (speeds, colors, thresholds, paths)
├── background.py        # Parallax scrolling background system
├── entities/
│   ├── fly.py           # Player (WASD controls, growth, physics)
│   ├── frog.py          # Boss enemy (tongue shooting, aiming)
│   ├── tongue.py        # Frog's projectile (extend/retract animation)
│   └── human.py         # Food items (falling, collision)
└── assets/images/
    ├── fly_sprite.png
    ├── frog_idle.png
    ├── frog_tongue.png
    └── human.png
```

## Architecture Patterns

### Game Loop (main.py)
- **State Machine**: Menu → Playing → Won/Lost
- **Delta Time**: Frame-independent movement (`dt` normalized to 60 FPS)
- **Entity Management**: Centralized lists for humans, tongues
- **State Transitions**: States set `next_state` to trigger transitions

### Entity System
All entities follow this pattern:
- `__init__()`: Load sprites, initialize physics
- `update(dt)`: Update position, animation, state
- `draw(surface)`: Render to screen
- Collision uses circular hitboxes with radius

### State Classes (game_states.py)
Each state has:
- `handle_event(event)`: Process input
- `update(dt)`: Game logic
- `render(screen)`: Drawing
- `next_state`: Trigger state change

### Configuration (config.py)
**ALL constants centralized here** - no magic numbers in code:
- Screen dimensions, FPS
- Entity spawn positions and speeds
- Growth thresholds (10, 20, 30 humans)
- Asset paths
- Color definitions

## Critical Gameplay Systems

### Growth System
Thresholds in [config.py](config.py#L24-L29):
```python
FLY_GROWTH_THRESHOLDS = {
    'small': 0,    # 0-9 humans
    'medium': 10,  # 10-19 humans  
    'large': 20,   # 20-29 humans
    'mega': 30     # 30+ humans (can eat frog)
}
```

Fly tracks `humans_eaten` counter, scales sprite, adjusts hitbox radius.

### Frog Tongue Shooting
1. **Idle**: Frog waits random cooldown (gets shorter as fly grows)
2. **Aiming**: 500ms warning with visual indicator (line + target circle)
3. **Shooting**: Creates Tongue entity with predictive aim
4. **Retracting**: Tongue returns, frog returns to idle

Frog uses predictive targeting - aims ahead of fly's velocity.

### Collision Detection
- **Fly ↔ Human**: Circle-circle (distance < radius1 + radius2)
- **Fly ↔ Tongue**: Line-circle (checks 20 segments along tongue)
- **Fly ↔ Frog**: Circle-circle (only when fly is mega size)

### Scrolling Background
Parallax system with multiple layers scrolling at different speeds to simulate upward flight. Tiles seamlessly. Fallback to solid color if images missing.

## Common Tasks

### Adding New Features
1. Add constants to [config.py](config.py)
2. Implement in relevant entity class
3. Update game loop in [game_states.py](game_states.py) PlayingState
4. Test across different fly growth levels

### Debugging
- Each entity has `draw_debug()` method for collision circles
- Check terminal for pygame errors
- Verify asset paths in config.py match actual file locations

### Balancing Difficulty
Edit in [config.py](config.py):
- `HUMAN_SPAWN_INTERVAL_MS`: Time between spawns
- `FROG_SHOOT_COOLDOWN_MIN/MAX`: Tongue shooting frequency
- `*_SPEED_MULTIPLIERS`: Entity speeds by level
- `HUMANS_TO_WIN`: Victory threshold

## Known Issues & Todos
- Background images may not exist (uses black fallback)
- No sound effects or music yet
- No particle effects for eating humans
- Win screen doesn't check if fly actually collides with frog (auto-win at 30 humans)

## GitHub Context
- **Repository**: UCLL-introproject-2526/projectweek-23-kikkers
- **Branch**: main (default)
- **Type**: GitHub Classroom assignment
