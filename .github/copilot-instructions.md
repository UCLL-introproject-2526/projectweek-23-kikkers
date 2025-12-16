# Copilot Instructions - Kikkers Project

## Project Overview
This is a classroom assignment project ("projectweek-23-kikkers") featuring a pygame-based game implementation. The project uses a mixed-language setup with Python for the game logic and a simple Java "Hello World" application.

## Technology Stack
- **Python**: Main game implementation using pygame library
- **Java**: Simple standalone application (app.java)
- **Pygame**: Graphics and game loop framework

## Current State & Known Issues
- [game.py](game.py#L7): Contains a critical typo - `pygame.displaty.set_mode()` should be `pygame.display.set_mode()`
- [app.java](app.java#L7): Missing semicolon after `System.out.println("Hello world!")`
- The pygame implementation is incomplete - has an infinite loop with minimal functionality

## Development Setup
- **Python Environment**: macOS with Homebrew-managed Python (externally managed, PEP 668)
- **Virtual Environment Required**: MUST use venv - direct pip install will fail
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install pygame
  ```
- **Running the Game**: Always activate venv first: `source venv/bin/activate && python game.py`
- Project uses standard Python gitignore patterns from toptal.com
- **Note**: Do NOT use `--break-system-packages` - use proper venv isolation instead

## File Structure
```
/Users/moe/kikkers/
├── game.py          # Pygame application (incomplete)
├── app.java         # Java hello world
├── README.md        # GitHub classroom assignment metadata
├── .gitignore       # Python/VSCode ignore patterns
└── venv/            # Python virtual environment (git-ignored)
```

## Code Patterns & Conventions
- **Entry Points**: 
  - Python: `main()` function in game.py (not currently called)
  - Java: Standard `public static void main(String[] args)` pattern
  
- **Pygame Structure**: Uses nested function pattern - `create_main_surface()` defined inside `main()` but creates infinite loop

## Common Tasks
When fixing the game:
1. Fix the typo: `pygame.displaty` → `pygame.display`
2. Properly structure the game loop (current infinite while loop in initialization is incorrect)
3. Add missing `main()` call at module level
4. Consider extracting `create_main_surface()` outside of `main()` for better structure

When working with Java:
1. Add missing semicolon on line 7
2. Compile with standard javac: `javac app.java`
3. Run with: `java App`

## GitHub Context
- Repository: UCLL-introproject-2526/projectweek-23-kikkers
- Current branch: main (also default)
- This is a GitHub Classroom assignment
