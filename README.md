# Wolf Game - Realistic Survival Simulator

A Python-based ecological simulation game featuring realistic wolf pack behavior, hunting dynamics, and survival mechanics.

## Features

### 🐺 Realistic Wolf Behavior
- **Pack Dynamics**: Wolves organize into packs with natural hierarchies
- **State Machine**: Wolves switch between Hunting, Roaming, Following, and Resting states
- **Energy System**: Complex energy management with starvation mechanics
- **Health Tracking**: Visual health indicators showing wolf vitality
- **Gender System**: Male and female wolves for natural reproduction

### 🦌 Prey & Ecological Balance
- **Dynamic Prey Population**: Herbivores wander naturally with energy depletion
- **Hunting Success**: Pack size affects hunting effectiveness
- **Population Control**: Prey respawns maintain ecological balance

### 👥 Breeding & Evolution
- **Natural Reproduction**: Wolves breed when conditions are favorable
- **Pack Growth**: Packs grow based on hunting success and resources
- **Pack Limits**: Maximum pack size prevents overpopulation
- **Generational Change**: Wolves age and eventually die

### 🎮 Interactive Controls
- **SPACE**: Pause/Resume simulation
- **R**: Reset the game
- **P**: Add more prey to the ecosystem

### 📊 Real-time Statistics
- Time elapsed
- Number of active packs
- Total wolf population
- Available prey count

## Game Mechanics

### Energy System
- Wolves lose energy through movement and metabolism
- Hunting replenishes energy when successful
- Starvation leads to health decline and death
- Resting restores energy and health

### Pack Hunting
- Single wolves have base hunting success rate of 30%
- Pack bonus: +10% success rate per additional pack member
- Coordinated hunting increases survival chances
- Larger packs have better hunting success

### Territory & Breeding
- Wolves must mature (age 300) before breeding
- Breeding only occurs when wolves are close together
- Maximum breeding age prevents overly old wolves from reproducing
- New pups inherit pack membership and gender

## Requirements

```
pygame>=2.0.0
numpy
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python wolf_game.py
```

## Game Settings

Edit the constants at the top of `wolf_game.py` to customize:
- `WINDOW_WIDTH` / `WINDOW_HEIGHT`: Display resolution
- `WOLF_SPEED`: Movement speed of wolves
- `PACK_MAX_SIZE`: Maximum wolves per pack
- `ENERGY_DEPLETION_RATE`: How fast energy depletes
- `HUNTING_SUCCESS_RATE`: Base hunting effectiveness
- `MATURITY_AGE`: Age when wolves can breed

## Simulation Parameters

- **Frame Rate**: 60 FPS
- **Initial Setup**: 3 packs (4-8 wolves each), 150 prey
- **Prey Respawn**: Maintains minimum 50 prey
- **Pack Creation**: New packs spawn if population < 2

## Visual Indicators

- **Wolves**: Blue circles with yellow eyes
- **Health Color**: Brighter = healthier
- **Energy Bar**: Red bar above each wolf shows energy level
- **Prey**: Yellow/gold circles

## Strategy Tips

1. **Monitor Prey Population**: Insufficient prey leads to wolf starvation
2. **Observe Pack Behavior**: Larger packs hunt more effectively
3. **Watch Breeding Cycles**: Successful packs grow over time
4. **Balance Ecosystem**: Use 'P' key to stabilize prey if needed

## Future Enhancements

- Territorial warfare between packs
- Seasonal changes affecting prey availability
- Wolf vocalizations and communication
- Predator-prey visual feedback
- Advanced AI pathfinding
- Save/load simulation states
- Statistical graphs and analysis tools

## License

MIT License

## Author

Created as a realistic ecosystem simulation using Python and Pygame.
