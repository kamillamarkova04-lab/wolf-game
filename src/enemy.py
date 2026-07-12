"""
Enemy Class - Manages enemy wolves and creatures
"""

import pygame
from config import *
import random
import math

class Enemy:
    """Base enemy class"""
    def __init__(self, x, y, enemy_type="wolf"):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.vel_x = 0
        self.vel_y = 0
        self.type = enemy_type
        
        # Stats based on type
        if enemy_type == "wolf":
            self.health = 45
            self.max_health = 45
            self.speed = 3.5
            self.attack_damage = 12
            self.exp_reward = 50
        elif enemy_type == "bear":
            self.health = 80
            self.max_health = 80
            self.speed = 2.5
            self.attack_damage = 25
            self.exp_reward = 150
        else:  # lynx
            self.health = 35
            self.max_health = 35
            self.speed = 4.5
            self.attack_damage = 10
            self.exp_reward = 40
        
        self.detection_range = 150
        self.attack_range = 50
        self.attack_cooldown = 0
        self.state = "patrol"  # patrol, chase, attack, dead
        self.direction = random.randint(0, 360)
        self.movement_timer = random.randint(60, 300)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(dx*dx + dy*dy)
    
    def update(self, player):
        """Update enemy behavior"""
        distance_to_player = self.distance_to(player.x, player.y)
        
        # State machine
        if distance_to_player < self.detection_range and self.state != "dead":
            if distance_to_player < self.attack_range:
                self.state = "attack"
            else:
                self.state = "chase"
        else:
            self.state = "patrol"
        
        # Behavior
        if self.state == "patrol":
            self._patrol()
        elif self.state == "chase":
            self._chase_player(player)
        elif self.state == "attack":
            self._attack_player(player)
        
        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Bounds
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        self.rect.topleft = (self.x, self.y)
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def _patrol(self):
        """Patrol behavior"""
        self.movement_timer -= 1
        if self.movement_timer <= 0:
            self.direction = random.randint(0, 360)
            self.movement_timer = random.randint(60, 300)
        
        rad = math.radians(self.direction)
        self.vel_x = math.cos(rad) * self.speed
        self.vel_y = math.sin(rad) * self.speed
        
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.direction = (180 - self.direction) % 360
        if self.y <= 0 or self.y + self.height >= SCREEN_HEIGHT:
            self.direction = (360 - self.direction) % 360
    
    def _chase_player(self, player):
        """Chase the player"""
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            self.vel_x = (dx / dist) * self.speed
            self.vel_y = (dy / dist) * self.speed
    
    def _attack_player(self, player):
        """Attack the player"""
        if self.attack_cooldown <= 0:
            player.take_damage(self.attack_damage)
            self.attack_cooldown = 30
    
    def draw(self, surface):
        """Draw enemy"""
        color = {"wolf": (60, 60, 60), "bear": (100, 80, 60), "lynx": (200, 100, 50)}
        pygame.draw.ellipse(surface, color.get(self.type, GRAY), (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        health_ratio = max(0, self.health / self.max_health)
        pygame.draw.rect(surface, RED, (self.x, self.y - 6, self.width, 3))
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 6, self.width * health_ratio, 3))
    
    def take_damage(self, amount):
        """Take damage"""
        self.health -= amount
        if self.health <= 0:
            self.state = "dead"


class EnemyManager:
    """Manages all enemies in the game"""
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 300
    
    def update(self, player, world):
        """Update all enemies"""
        # Spawn new enemies
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval and len(self.enemies) < 5:
            self._spawn_enemy()
            self.spawn_timer = 0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(player)
            
            # Check if player attacks enemy
            if player.is_attacking:
                dist = player.distance_to(enemy.x, enemy.y) if hasattr(player, 'distance_to') else \
                       math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2)
                if dist < player.attack_range:
                    enemy.take_damage(player.attack_damage * player.hunting_skill)
                    if enemy.health <= 0:
                        player.gain_experience(enemy.exp_reward)
                        player.kills += 1
                        if 'meat' in player.inventory:
                            player.inventory['meat'] += 2
            
            # Remove dead enemies
            if enemy.health <= 0:
                self.enemies.remove(enemy)
    
    def _spawn_enemy(self):
        """Spawn a new enemy"""
        enemy_types = ["wolf", "lynx"]
        if random.random() > 0.8:
            enemy_types.append("bear")
        
        enemy_type = random.choice(enemy_types)
        x = random.randint(0, SCREEN_WIDTH - 28)
        y = random.randint(0, SCREEN_HEIGHT - 28)
        
        self.enemies.append(Enemy(x, y, enemy_type))
    
    def draw(self, surface):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(surface)
