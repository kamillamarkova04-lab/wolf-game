# Wolf Game 🐺

2D survival game where you play as a wolf, hunting for food, avoiding dangers, and managing your pack.

## Features

- **Open World Exploration**: Roam freely across diverse landscapes
- **Hunting Mechanics**: Hunt prey to survive and grow stronger
- **Pack Management**: Recruit and manage other wolves
- **Dynamic Environment**: Day/night cycle, weather, seasons
- **Combat System**: Fight predators and rival packs
- **Stats System**: Hunger, health, energy, reputation
- **Multiple Levels**: Forest, mountains, plains, tundra
- **Save/Load System**: Persistent game saves

## Requirements

- Python 3.9+
- Pygame 2.1+

## Installation

```bash
git clone https://github.com/kamillamarkova04-lab/wolf-game.git
cd wolf-game
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **W/A/S/D** - Move
- **Space** - Attack/Interact
- **E** - Use ability
- **Tab** - Inventory
- **Esc** - Menu
- **Ctrl+S** - Save Game

## Project Structure

```
wolf-game/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config.py              # Game configuration
├── src/
│   ├── game.py            # Main game loop
│   ├── player.py          # Wolf player character
│   ├── enemy.py           # Enemy entities
│   ├── world.py           # World/level management
│   ├── save_system.py     # Save/load functionality
│   ├── ui.py              # User interface
│   ├── weather.py         # Weather system
│   └── utils.py           # Utility functions
├── assets/
│   ├── sprites/           # Character and object sprites
│   ├── maps/              # Level maps
│   └── sounds/            # Audio files
└── docs/                  # Documentation
```

## Development

Created: July 2026

## License

MIT
