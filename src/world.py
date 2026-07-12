"""
World Class - Manages level, terrain, and environmental objects
"""

import pygame
from config import *
import random

class World:
    def __init__(self, seed=42):
        self.seed = seed
        random.seed(seed)
        self.tiles = []
        self.objects = []
        self.prey_objects = []
        self.time_of_day = 0  # 0-24 hours
        self.weather = "sunny"
        self.temperature = 20
        self.humidity = 50
        self.day_count = 0
        self.generate_world()
    
    def generate_world(self):
        """Generate the game world"""
        # Generate background terrain with different zones
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                # Create zones
                noise = random.random()
                
                # Forest zone (north)
                if y < SCREEN_HEIGHT * 0.4:
                    if noise > 0.85:
                        self.objects.append(Tree(x, y))
                    elif noise > 0.80:
                        self.objects.append(Rock(x, y))
                    elif noise > 0.75:
                        self.prey_objects.append(Deer(x, y))
                
                # Grassland zone (middle)
                elif y < SCREEN_HEIGHT * 0.7:
                    if noise > 0.90:
                        self.objects.append(Rock(x, y))
                    elif noise > 0.85:
                        self.prey_objects.append(Deer(x, y))
                
                # Desert zone (south)
                else:
                    if noise > 0.92:
                        self.objects.append(Rock(x, y))
    
    def update(self, delta_time=1):
        """Update world state"""
        self.time_of_day += 0.004  # Simulate day/night cycle
        if self.time_of_day >= 24:
            self.time_of_day = 0
            self.day_count += 1
            self._update_weather()
        
        # Update objects
        for obj in self.objects:
            obj.update()
        
        for prey in self.prey_objects:
            prey.update()
    
    def _update_weather(self):
        """Update weather conditions"""
        weather_roll = random.random()
        if weather_roll > 0.7:
            self.weather = "rainy"
            self.temperature -= 5
        elif weather_roll > 0.5:
            self.weather = "cloudy"
        else:
            self.weather = "sunny"
            self.temperature += 2
        
        self.temperature = max(-10, min(35, self.temperature))
    
    def draw(self, surface):
        """Draw the world"""
        # Draw background based on time of day
        ambient = self.get_ambient_light()
        bg_color = (
            int(LIGHT_GREEN[0] * ambient),
            int(LIGHT_GREEN[1] * ambient),
            int(LIGHT_GREEN[2] * ambient)
        )
        surface.fill(bg_color)
        
        # Draw weather effects
        if self.weather == "rainy":
            self._draw_rain(surface)
        elif self.weather == "cloudy":
            self._draw_clouds(surface)
        
        # Draw grid (optional)
        self._draw_grid(surface)
        
        # Draw objects
        for obj in self.objects:
            obj.draw(surface)
        
        # Draw prey
        for prey in self.prey_objects:
            prey.draw(surface)
    
    def _draw_grid(self, surface):
        """Draw grid overlay"""
        grid_color = (200, 200, 200)
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(surface, grid_color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(surface, grid_color, (0, y), (SCREEN_WIDTH, y))
    
    def _draw_rain(self, surface):
        """Draw rain particles"""
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(surface, CYAN, (x, y), (x - 2, y + 10), 1)
    
    def _draw_clouds(self, surface):
        """Draw clouds"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(50)
        overlay.fill(GRAY)
        surface.blit(overlay, (0, 0))
    
    def get_ambient_light(self):
        """Calculate ambient light based on time of day"""
        if 6 <= self.time_of_day < 18:  # Day
            return 1.0
        elif 18 <= self.time_of_day < 20:  # Sunset
            return 0.7
        elif 20 <= self.time_of_day or self.time_of_day < 4:  # Night
            return 0.3
        else:  # Sunrise
            return 0.5


class TreeObject:
    """Tree terrain object"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw tree"""
        pygame.draw.rect(surface, BROWN, (self.x + 8, self.y + 16, 16, 16))  # Trunk
        pygame.draw.polygon(surface, DARK_GREEN, [  # Canopy
            (self.x + 16, self.y + 4),
            (self.x + 4, self.y + 16),
            (self.x + 28, self.y + 16)
        ])
    
    def update(self):
        pass


class Rock:
    """Rock terrain object"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.health = 200
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw rock"""
        pygame.draw.ellipse(surface, GRAY, (self.x + 4, self.y + 4, 24, 24))
        pygame.draw.ellipse(surface, (200, 200, 200), (self.x + 8, self.y + 8, 8, 8))
    
    def update(self):
        pass


class Deer:
    """Prey animal"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.health = 30
        self.max_health = 30
        self.speed = 4
        self.direction = random.randint(0, 360)
        self.movement_timer = random.randint(30, 180)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw deer"""
        pygame.draw.ellipse(surface, (200, 150, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, (150, 100, 50), (self.x + 18, self.y + 6), 4)  # Head
        # Draw antlers
        pygame.draw.line(surface, (139, 69, 19), (self.x + 16, self.y + 2), (self.x + 14, self.y - 4), 2)
        pygame.draw.line(surface, (139, 69, 19), (self.x + 20, self.y + 2), (self.x + 22, self.y - 4), 2)
    
    def update(self):
        """Update deer behavior"""
        self.movement_timer -= 1
        if self.movement_timer <= 0:
            self.direction = random.randint(0, 360)
            self.movement_timer = random.randint(30, 180)
        
        # Move in current direction
        import math
        rad = math.radians(self.direction)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        
        # Bounce off walls
        if self.x < 0 or self.x + self.width > SCREEN_WIDTH:
            self.direction = (180 - self.direction) % 360
        if self.y < 0 or self.y + self.height > SCREEN_HEIGHT:
            self.direction = (360 - self.direction) % 360
        
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        self.rect.topleft = (self.x, self.y)


# Alias for the tree class
Tree = TreeObject
