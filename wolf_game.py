import pygame
import sys
import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

# Initialize Pygame
pygame.init()

# ============= CONSTANTS =============
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
BACKGROUND_COLOR = (34, 139, 34)  # Forest green

# Game settings
WOLF_SPEED = 3
WOLF_SIZE = 15
PACK_MAX_SIZE = 15
PREY_SIZE = 8
GRASS_PATCH_COUNT = 50
ENERGY_DEPLETION_RATE = 0.3
HUNTING_SUCCESS_RATE = 0.3
MATURITY_AGE = 300
BREEDING_AGE_MAX = 2000
STARVATION_THRESHOLD = 10

# ============= ENUMS =============
class WolfState(Enum):
    HUNTING = 1
    ROAMING = 2
    RESTING = 3
    FOLLOWING = 4

class Gender(Enum):
    MALE = 1
    FEMALE = 2

# ============= DATA STRUCTURES =============
@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def normalize(self):
        dist = math.sqrt(self.x**2 + self.y**2)
        if dist == 0:
            return Vector2(0, 0)
        return Vector2(self.x / dist, self.y / dist)
    
    def clamp(self, width, height):
        return Vector2(
            max(0, min(width, self.x)),
            max(0, min(height, self.y))
        )

# ============= PREY =============
class Prey:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.vel = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.energy = 100
        self.age = 0
        
    def update(self):
        # Random wandering with some persistence
        if random.random() < 0.02:
            self.vel = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        
        self.pos = self.pos + self.vel
        self.pos = self.pos.clamp(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.energy -= 0.1
        self.age += 1
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 200, 0), (int(self.pos.x), int(self.pos.y)), PREY_SIZE)

# ============= WOLF =============
class Wolf:
    def __init__(self, x, y, pack_id):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.energy = 100
        self.age = 0
        self.pack_id = pack_id
        self.state = WolfState.ROAMING
        self.gender = random.choice([Gender.MALE, Gender.FEMALE])
        self.target_prey = None
        self.wander_direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.wander_timer = 0
        self.territory_memory = []  # Remember good hunting spots
        self.health = 100
        
    def update(self, prey_list: List[Prey], wolf_pack: List['Wolf']):
        self.age += 1
        self.energy -= ENERGY_DEPLETION_RATE
        self.health = max(0, self.health - 0.1)
        
        # State machine
        if self.energy < STARVATION_THRESHOLD:
            self.state = WolfState.HUNTING
        elif self.energy > 80 and self.age > 500:
            self.state = WolfState.RESTING
        elif len(wolf_pack) > 1 and self.age > 100:
            self.state = WolfState.FOLLOWING
        
        # Behavior based on state
        if self.state == WolfState.HUNTING:
            self._hunt(prey_list, wolf_pack)
        elif self.state == WolfState.FOLLOWING:
            self._follow_pack(wolf_pack)
        elif self.state == WolfState.RESTING:
            self._rest()
        else:
            self._roam()
        
        # Apply velocity
        self.pos = self.pos + self.vel
        self.pos = self.pos.clamp(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Starvation check
        if self.energy < 0:
            self.health -= 5
    
    def _hunt(self, prey_list: List[Prey], wolf_pack: List['Wolf']):
        """Realistic hunting behavior - wolves hunt together in packs"""
        closest_prey = None
        closest_dist = float('inf')
        
        for prey in prey_list:
            dist = self.pos.distance_to(prey.pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_prey = prey
        
        if closest_prey:
            self.target_prey = closest_prey
            direction = (closest_prey.pos + Vector2(-self.pos.x, -self.pos.y)).normalize()
            self.vel = direction * WOLF_SPEED
            
            # Pack hunting bonus - more wolves = higher success
            pack_size = len([w for w in wolf_pack if w.pack_id == self.pack_id])
            success_rate = HUNTING_SUCCESS_RATE * (1 + pack_size * 0.1)
            
            if closest_dist < WOLF_SIZE + PREY_SIZE:
                if random.random() < success_rate:
                    self.energy += 50
                    self.health += 10
                    return closest_prey
        else:
            self._roam()
        
        return None
    
    def _follow_pack(self, wolf_pack: List['Wolf']):
        """Stay close to pack members and follow the alpha"""
        pack_members = [w for w in wolf_pack if w.pack_id == self.pack_id and w != self]
        
        if pack_members:
            # Find nearest pack member
            closest = min(pack_members, key=lambda w: self.pos.distance_to(w.pos))
            dist = self.pos.distance_to(closest.pos)
            
            if dist > 50:
                direction = (closest.pos + Vector2(-self.pos.x, -self.pos.y)).normalize()
                self.vel = direction * WOLF_SPEED
            else:
                self.vel = self.vel * 0.9  # Slow down
    
    def _roam(self):
        """Natural roaming behavior with territory memory"""
        self.wander_timer += 1
        
        if self.wander_timer > 100 or self.wander_direction.distance_to(Vector2(0, 0)) == 0:
            self.wander_direction = Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ).normalize()
            self.wander_timer = 0
        
        self.vel = self.wander_direction * (WOLF_SPEED * 0.7)
    
    def _rest(self):
        """Resting recovers energy"""
        self.energy = min(100, self.energy + 0.5)
        self.health = min(100, self.health + 0.3)
        self.vel = self.vel * 0.95
    
    def can_breed(self):
        """Breeding conditions"""
        return (
            self.age > MATURITY_AGE and
            self.age < BREEDING_AGE_MAX and
            self.energy > 70 and
            self.health > 60
        )
    
    def draw(self, screen):
        # Wolf body color based on health
        health_ratio = self.health / 100
        color = (
            int(100 + 155 * health_ratio),
            int(100 + 155 * health_ratio),
            150
        )
        
        # Draw wolf
        pygame.draw.circle(screen, color, (int(self.pos.x), int(self.pos.y)), WOLF_SIZE)
        
        # Draw eyes
        eye_offset = 5
        pygame.draw.circle(screen, (255, 255, 0), 
                          (int(self.pos.x - eye_offset), int(self.pos.y - eye_offset)), 2)
        pygame.draw.circle(screen, (255, 255, 0),
                          (int(self.pos.x + eye_offset), int(self.pos.y - eye_offset)), 2)
        
        # Draw energy bar
        bar_width = 20
        bar_height = 3
        pygame.draw.rect(screen, (50, 50, 50),
                        (int(self.pos.x - bar_width/2), int(self.pos.y - WOLF_SIZE - 5), bar_width, bar_height))
        pygame.draw.rect(screen, (255, 100, 100),
                        (int(self.pos.x - bar_width/2), int(self.pos.y - WOLF_SIZE - 5),
                         bar_width * (self.energy / 100), bar_height))

# ============= WOLF PACK =============
class WolfPack:
    _pack_counter = 0
    
    def __init__(self, initial_wolves=5):
        self.pack_id = WolfPack._pack_counter
        WolfPack._pack_counter += 1
        self.wolves = [
            Wolf(
                random.randint(100, WINDOW_WIDTH - 100),
                random.randint(100, WINDOW_HEIGHT - 100),
                self.pack_id
            )
            for _ in range(initial_wolves)
        ]
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
    
    def update(self, prey_list: List[Prey]):
        """Update all wolves in pack"""
        # Remove dead wolves
        self.wolves = [w for w in self.wolves if w.health > 0 and w.energy > -50]
        
        # Update each wolf
        for wolf in self.wolves:
            wolf.update(prey_list, self.wolves)
        
        # Breeding - create new wolves
        breeding_pairs = []
        for i, wolf1 in enumerate(self.wolves):
            for wolf2 in self.wolves[i+1:]:
                if (wolf1.can_breed() and wolf2.can_breed() and 
                    wolf1.gender != wolf2.gender and
                    wolf1.pos.distance_to(wolf2.pos) < 30):
                    breeding_pairs.append((wolf1, wolf2))
        
        for wolf1, wolf2 in breeding_pairs:
            if len(self.wolves) < PACK_MAX_SIZE and random.random() < 0.3:
                new_wolf = Wolf(
                    (wolf1.pos.x + wolf2.pos.x) / 2,
                    (wolf1.pos.y + wolf2.pos.y) / 2,
                    self.pack_id
                )
                new_wolf.age = 0
                new_wolf.energy = 80
                self.wolves.append(new_wolf)
                wolf1.energy -= 20
                wolf2.energy -= 20

# ============= GAME =============
class WolfGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Wolf Game - Realistic Survival Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        
        self.prey_list = []
        self.packs = []
        self.time_step = 0
        self.paused = False
        
        self._init_game()
    
    def _init_game(self):
        """Initialize game world"""
        # Create prey
        for _ in range(150):
            self.prey_list.append(
                Prey(
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT)
                )
            )
        
        # Create wolf packs
        for _ in range(3):
            self.packs.append(WolfPack(initial_wolves=random.randint(4, 8)))
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self._init_game()
                    self.time_step = 0
                elif event.key == pygame.K_p:
                    # Spawn new prey
                    for _ in range(20):
                        self.prey_list.append(
                            Prey(
                                random.randint(0, WINDOW_WIDTH),
                                random.randint(0, WINDOW_HEIGHT)
                            )
                        )
    
    def update(self):
        """Update game state"""
        if self.paused:
            return
        
        self.time_step += 1
        
        # Update prey
        self.prey_list = [p for p in self.prey_list if p.energy > 0]
        for prey in self.prey_list:
            prey.update()
        
        # Respawn prey if too few
        if len(self.prey_list) < 50:
            for _ in range(30):
                self.prey_list.append(
                    Prey(
                        random.randint(0, WINDOW_WIDTH),
                        random.randint(0, WINDOW_HEIGHT)
                    )
                )
        
        # Update packs
        for pack in self.packs:
            pack.update(self.prey_list)
        
        # Remove extinct packs
        self.packs = [p for p in self.packs if len(p.wolves) > 0]
        
        # Occasionally create new packs
        if len(self.packs) < 2 and self.time_step % 500 == 0:
            self.packs.append(WolfPack(initial_wolves=random.randint(3, 5)))
    
    def draw(self):
        """Render game state"""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw prey
        for prey in self.prey_list:
            prey.draw(self.screen)
        
        # Draw wolves
        for pack in self.packs:
            for wolf in pack.wolves:
                wolf.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw HUD"""
        total_wolves = sum(len(pack.wolves) for pack in self.packs)
        
        stats = [
            f"Time: {self.time_step}",
            f"Packs: {len(self.packs)}",
            f"Wolves: {total_wolves}",
            f"Prey: {len(self.prey_list)}",
            "",
            "CONTROLS:",
            "SPACE - Pause/Resume",
            "R - Reset",
            "P - Add Prey"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (255, 255, 255))
            self.screen.blit(text, (10, 10 + i * 25))
        
        # Status message
        if self.paused:
            pause_text = self.font.render("PAUSED", True, (255, 0, 0))
            self.screen.blit(pause_text, (WINDOW_WIDTH - 150, 10))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# ============= MAIN =============
if __name__ == "__main__":
    game = WolfGame()
    game.run()
