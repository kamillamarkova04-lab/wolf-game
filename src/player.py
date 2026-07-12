"""
Player Class - Represents the player-controlled wolf
"""

import pygame
from config import *
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        
        # Stats
        self.health = PLAYER_HEALTH
        self.hunger = PLAYER_HUNGER
        self.energy = PLAYER_ENERGY
        self.stamina = PLAYER_STAMINA
        self.max_health = PLAYER_HEALTH
        self.max_hunger = PLAYER_HUNGER
        self.max_energy = PLAYER_ENERGY
        self.max_stamina = PLAYER_STAMINA
        
        # Progression
        self.level = 1
        self.experience = 0
        self.kills = 0
        self.exp_to_next_level = 100
        
        # Skills
        self.hunting_skill = 1.0
        self.defense_skill = 1.0
        self.speed_skill = 1.0
        
        # Status
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_range = 40
        self.attack_damage = 15
        self.direction = 0  # Angle in radians
        self.is_sprinting = False
        self.sprint_drain = 0.5
        
        # Inventory
        self.inventory = {
            'meat': 0,
            'herbs': 0,
            'bones': 0,
        }
        
        # Create a simple wolf sprite
        self.image = self._create_wolf_sprite()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def _create_wolf_sprite(self):
        """Create a simple wolf sprite"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw wolf body
        pygame.draw.ellipse(surface, (100, 100, 100), (8, 12, 16, 8))  # Body
        pygame.draw.circle(surface, (100, 100, 100), (24, 10), 8)     # Head
        
        # Draw ears
        pygame.draw.polygon(surface, (100, 100, 100), [(20, 2), (24, 2), (22, 8)])
        pygame.draw.polygon(surface, (100, 100, 100), [(24, 2), (28, 2), (26, 8)])
        
        # Draw eyes
        pygame.draw.circle(surface, WHITE, (22, 8), 2)
        pygame.draw.circle(surface, BLACK, (23, 8), 1)
        pygame.draw.circle(surface, WHITE, (26, 8), 2)
        pygame.draw.circle(surface, BLACK, (27, 8), 1)
        
        # Draw nose
        pygame.draw.circle(surface, BLACK, (24, 10), 1)
        
        # Draw legs
        pygame.draw.line(surface, (100, 100, 100), (12, 20), (12, 28), 2)
        pygame.draw.line(surface, (100, 100, 100), (18, 20), (18, 28), 2)
        pygame.draw.line(surface, (100, 100, 100), (20, 20), (20, 28), 2)
        pygame.draw.line(surface, (100, 100, 100), (26, 20), (26, 28), 2)
        
        # Draw tail
        pygame.draw.line(surface, (100, 100, 100), (8, 15), (2, 10), 2)
        
        return surface
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        self.vel_x = 0
        self.vel_y = 0
        
        is_moving = False
        if keys[pygame.K_w]:
            self.vel_y -= PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_s]:
            self.vel_y += PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_a]:
            self.vel_x -= PLAYER_SPEED
            is_moving = True
        if keys[pygame.K_d]:
            self.vel_x += PLAYER_SPEED
            is_moving = True
        
        # Sprint
        self.is_sprinting = keys[pygame.K_LSHIFT] and is_moving and self.stamina > 10
        if self.is_sprinting:
            speed_multiplier = 1.5 * self.speed_skill
            self.vel_x *= speed_multiplier
            self.vel_y *= speed_multiplier
            self.stamina -= self.sprint_drain
        
        # Attack
        if keys[pygame.K_SPACE]:
            if self.attack_cooldown <= 0:
                self.attack()
    
    def attack(self):
        """Perform attack action"""
        self.is_attacking = True
        self.attack_cooldown = 15
    
    def gain_experience(self, amount):
        """Gain experience points"""
        self.experience += amount
        if self.experience >= self.exp_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the wolf"""
        self.level += 1
        self.experience = 0
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        
        # Improve stats
        self.max_health += 20
        self.health = self.max_health
        self.max_stamina += 15
        self.stamina = self.max_stamina
        self.attack_damage += 5
        self.hunting_skill += 0.1
        self.defense_skill += 0.1
    
    def eat(self, food_type):
        """Eat food to restore hunger and possibly get buffs"""
        if food_type == 'meat':
            self.hunger = min(self.max_hunger, self.hunger + 40)
            self.health = min(self.max_health, self.health + 10)
            self.inventory['meat'] -= 1
        elif food_type == 'herbs':
            self.hunger = min(self.max_hunger, self.hunger + 15)
            self.health = min(self.max_health, self.health + 20)
            self.inventory['herbs'] -= 1
    
    def update(self):
        """Update player state"""
        # Move player
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player on screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        # Update rect
        self.rect.topleft = (self.x, self.y)
        
        # Update stats
        self.hunger = max(0, self.hunger - 0.15)  # Hunger decreases over time
        if self.is_sprinting:
            self.hunger -= 0.1  # Extra hunger from sprinting
        
        # Energy and stamina recovery
        if not self.is_sprinting:
            self.energy = min(self.max_energy, self.energy + 0.08)
            self.stamina = min(self.max_stamina, self.stamina + 0.05)
        
        # Health affected by hunger
        if self.hunger < 20:
            self.health -= 0.15
        elif self.hunger > 50:
            self.health = min(self.max_health, self.health + 0.05)  # Heal when well-fed
        
        self.health = max(0, min(self.max_health, self.health))
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.is_attacking = False
    
    def draw(self, surface):
        """Draw the player"""
        # Draw wolf sprite
        surface.blit(self.image, (self.x, self.y))
        
        # Draw health bar
        bar_width = self.width
        bar_height = 4
        health_ratio = max(0, self.health / self.max_health)
        
        pygame.draw.rect(surface, RED, (self.x, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y - 10, bar_width, bar_height), 1)
        
        # Draw hunger indicator
        hunger_ratio = max(0, self.hunger / self.max_hunger)
        pygame.draw.rect(surface, (255, 100, 0), (self.x, self.y - 16, bar_width * hunger_ratio, 3))
        
        # Draw attack effect
        if self.is_attacking:
            pygame.draw.circle(surface, (255, 100, 100), 
                              (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                              self.attack_range, 2)
    
    def take_damage(self, amount):
        """Take damage"""
        damage = amount / (1 + self.defense_skill * 0.1)
        self.health -= damage
    
    def feed(self, amount):
        """Feed the wolf"""
        self.hunger = min(self.max_hunger, self.hunger + amount)
