# 🐸 FROGEATO ULTRA - The Ultimate Swamp Survival Experience

An epic arcade-style survival game where you play as a mosquito trying to survive in a deadly swamp filled with hungry frogs!

## 🎮 Features

### 🌟 Core Gameplay
- **Smooth Physics-Based Movement** - Realistic acceleration, friction, and momentum
- **Smart Frog AI** - Predictive targeting, tactical decision-making, and varied attack patterns
- **Dynamic Difficulty** - Choose from Easy, Normal, Hard, or INSANE modes
- **Health System** - 100 HP with 3-hit death mechanic
- **Wave Progression** - Increasing challenge as you survive longer

### ⚡ Power-Up System
Collect 6 different power-ups with unique visual effects:
- **Speed Boost** ⚡ - Move 50% faster for 5 seconds
- **Shield** 🛡️ - Block one hit for 8 seconds
- **Slow Motion** ⏰ - Time slows down for 6 seconds
- **Magnet** 🧲 - Attract nearby humans for 7 seconds
- **Invincibility** ⭐ - Become untouchable for 4 seconds
- **Double Points** 💰 - 2x score for 10 seconds

### 🔥 Combo System
- Build massive combos by collecting humans without stopping
- Up to **10x multiplier**!
- Color-coded combo indicators:
  - Green (2x) → Orange (3x) → Red (5x) → Purple (8x+)
- Floating score popups show your points in real-time

### ✨ Visual Effects
- **Particle Systems** - Explosions, trails, sparkles, and collection effects
- **Screen Shake** - On hits and big moments
- **Animated UI** - Smooth health bars, power-up timers, and combo displays
- **Firefly Ambience** - Beautiful glowing particles on menu screens
- **Glowing Power-Ups** - Rotating, pulsing collectibles with particle trails

### 🎨 Professional UI/HUD
- **Health Bar** - Color-changing based on HP (Green → Yellow → Red)
- **Score Display** - Large, easy-to-read score counter
- **Combo Indicator** - Shows current multiplier and streak
- **Power-Up Timers** - Active effects with countdown
- **Wave Counter** - Track your progression

### 🎯 Enhanced Start Screen
- **Animated Background** - Firefly particles with swamp ambience
- **Wobbling Title** - Dynamic title animation
- **Multiple Menus**:
  - Start Game
  - Options (Difficulty selection)
  - Credits
  - Quit
- **Hover Effects** - Glowing buttons with smooth interactions

## 🕹️ Controls

### Movement
- **W/↑** - Move Up
- **A/←** - Move Left
- **S/↓** - Move Down
- **D/→** - Move Right

### Game Controls
- **SPACE** - Pause/Resume
- **R** - Restart (when dead)
- **ESC** - Quit to Menu

## 🎲 Difficulty Levels

| Difficulty | Speed Multiplier | Description |
|------------|------------------|-------------|
| **EASY** | 0.7x | Perfect for beginners - slower spawns, easier frogs |
| **NORMAL** | 1.0x | Balanced challenge for casual players |
| **HARD** | 1.4x | Fast-paced action for experienced players |
| **INSANE** | 2.0x | Brutal mode for true survivors |

## 🏆 Scoring System

- **Base Points**: 10 points per human
- **Difficulty Multiplier**: Points × difficulty setting
- **Combo Multiplier**: Up to 10x for streaks
- **Power-Up Bonus**: 2x with Double Points active
- **Maximum Combo**: Base × Difficulty × 10 × 2 = **massive scores!**

## 📊 Game Mechanics

### Frog AI Behavior
1. **Idle** - Waiting and watching
2. **Tracking** - Following your movement (eyes glow yellow)
3. **Preparing** - Tensing up for attack (intense glow)
4. **Attacking** - Tongue shoots with curved trajectory
5. **Retracting** - Pulling tongue (and you!) back

### Tongue Mechanics
- **Curved Trajectories** - 67% chance of curve for unpredictability
- **Predictive Targeting** - Aims where you'll be, not where you are
- **Grab & Pull** - If hit, you're dragged toward the frog's mouth
- **Shield Protection** - Active shields block tongue attacks

### Human Collection
- Humans spawn every 5 seconds (faster on higher difficulties)
- Collect to gain points and build combos
- Being "stunned" while collecting shows "Sucking Blood!" message
- Combo resets after 3 seconds without collection

### Power-Up Spawning
- Spawn every 8-15 seconds randomly
- Float and pulse with particle effects
- Rotating icon shows power-up type
- Automatically collected on contact

## 🎨 Visual Polish

### Particle Effects
- **Explosions** - On hits and deaths
- **Trails** - Behind fast-moving objects
- **Sparkles** - On power-up collection
- **Collect Effects** - When grabbing humans

### Screen Effects
- **Screen Shake** - Intensity-based camera shake
- **Color Grading** - Health-based color changes
- **Glow Effects** - On UI elements and power-ups
- **Smooth Animations** - 60 FPS gameplay

## 🛠️ Technical Features

- **60 FPS Gameplay** - Smooth, responsive action
- **Physics-Based Movement** - Realistic momentum and friction
- **Predictive AI** - Frogs lead their shots
- **Particle System** - Efficient particle management
- **Event-Driven UI** - Responsive button system
- **State Machine** - Clean game state management

## 📁 Project Structure

```
kikkers/
├── main_ultra.py          # Enhanced main game file
├── entities/
│   ├── fly.py            # Player mosquito class
│   ├── frog.py           # Enemy frog with AI
│   ├── tongue.py         # Curved tongue projectile
│   ├── human.py          # Collectible humans
│   ├── powerup.py        # Power-up system
│   └── effects.py        # Particles, combos, screen shake
├── images.py             # Image loader
└── assets/
    └── images/           # Game sprites
```

## 🚀 How to Run

### Requirements
- Python 3.7+
- Pygame

### Installation
```bash
# Install Pygame
pip install pygame

# Run the game
python3 main_ultra.py
```

## 🎯 Tips & Strategies

1. **Master Movement** - Use momentum to dodge tongue attacks
2. **Watch the Eyes** - Yellow glow warns of incoming attacks
3. **Build Combos** - Don't let 3 seconds pass without collecting
4. **Use Power-Ups Wisely** - Save invincibility for tough moments
5. **Stay Mobile** - Don't camp in corners
6. **Difficulty Scaling** - Start on Normal, master INSANE
7. **Shield Timing** - Collect shields before risky moves
8. **Double Points** - Maximize during high combos

## 🎨 Credits

**Game Design & Development**
- Your Amazing Team

**Special Thanks**
- GitHub Copilot for AI assistance
- Pygame community

**Assets**
- Custom pixel art swamp theme
- Frog, mosquito, and human sprites

## 📝 Version History

### v2.0 - ULTRA Edition (Current)
- ✨ Complete game overhaul
- ⚡ 6 Power-up types
- 🔥 Combo system with 10x multipliers
- 💫 Particle effects and screen shake
- 🎨 Professional UI/HUD
- 🎮 Enhanced start screen
- 🎯 4 Difficulty levels
- 💯 Health system

### v1.0 - Original Release
- Basic gameplay mechanics
- Simple scoring
- Basic frog AI

---

**Made with ❤️ using Python & Pygame**

*Survive the swamp. Collect the humans. Dodge the tongue. Become legendary.*

🐸 **FROGEATO ULTRA** - Are you ready for the ultimate challenge?
