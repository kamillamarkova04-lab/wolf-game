"""
UI Class - Manages user interface and HUD elements
"""

import pygame
from config import *

class UI:
    def __init__(self):
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 48)
        self.show_debug = False
    
    def update(self, player):
        """Update UI state"""
        self.player = player
    
    def draw(self, surface):
        """Draw UI elements"""
        if hasattr(self, 'player'):
            self._draw_stats_panel(surface)
            self._draw_minimap(surface)
            self._draw_info(surface)
            self._draw_inventory(surface)
            if self.show_debug:
                self._draw_debug_info(surface)
    
    def _draw_stats_panel(self, surface):
        """Draw stats panel in top-left"""
        panel_width = 280
        panel_height = 160
        padding = 10
        
        # Background
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill(BLACK)
        panel.set_alpha(220)
        surface.blit(panel, (padding, padding))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (padding, padding, panel_width, panel_height), 2)
        
        y_offset = padding * 2
        
        # Level and XP
        level_text = self.font_small.render(f"Level: {self.player.level}", True, CYAN)
        surface.blit(level_text, (padding * 2, y_offset))
        y_offset += 25
        
        # Health
        health_text = self.font_small.render(f"Health: {self.player.health:.0f}/{self.player.max_health}", True, RED)
        surface.blit(health_text, (padding * 2, y_offset))
        self._draw_bar(surface, padding * 2, y_offset + 18, 150, 10, 
                      self.player.health / self.player.max_health, GREEN)
        y_offset += 35
        
        # Hunger
        hunger_text = self.font_small.render(f"Hunger: {self.player.hunger:.0f}/{self.player.max_hunger}", True, YELLOW)
        surface.blit(hunger_text, (padding * 2, y_offset))
        self._draw_bar(surface, padding * 2, y_offset + 18, 150, 10, 
                      self.player.hunger / self.player.max_hunger, (255, 200, 0))
        y_offset += 35
        
        # Stamina
        stamina_text = self.font_small.render(f"Stamina: {self.player.stamina:.0f}/{self.player.max_stamina}", True, CYAN)
        surface.blit(stamina_text, (padding * 2, y_offset))
        self._draw_bar(surface, padding * 2, y_offset + 18, 150, 10, 
                      self.player.stamina / self.player.max_stamina, CYAN)
    
    def _draw_inventory(self, surface):
        """Draw inventory panel in top-right"""
        panel_width = 200
        panel_height = 120
        padding = 10
        x = SCREEN_WIDTH - panel_width - padding
        y = padding
        
        # Background
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill(BLACK)
        panel.set_alpha(220)
        surface.blit(panel, (x, y))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (x, y, panel_width, panel_height), 2)
        
        # Title
        title = self.font_medium.render("Inventory", True, YELLOW)
        surface.blit(title, (x + 10, y + 5))
        
        # Items
        y_offset = y + 35
        for item, count in self.player.inventory.items():
            item_text = self.font_small.render(f"{item}: {count}", True, WHITE)
            surface.blit(item_text, (x + 10, y_offset))
            y_offset += 25
    
    def _draw_minimap(self, surface):
        """Draw minimap in bottom-right"""
        minimap_size = 100
        minimap_x = SCREEN_WIDTH - minimap_size - 10
        minimap_y = SCREEN_HEIGHT - minimap_size - 10
        
        # Background
        pygame.draw.rect(surface, BLACK, (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(surface, YELLOW, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Player position
        player_x = minimap_x + (self.player.x / SCREEN_WIDTH) * minimap_size
        player_y = minimap_y + (self.player.y / SCREEN_HEIGHT) * minimap_size
        pygame.draw.circle(surface, RED, (int(player_x), int(player_y)), 3)
        
        # Title
        title = self.font_small.render("Map", True, YELLOW)
        surface.blit(title, (minimap_x + 5, minimap_y - 20))
    
    def _draw_info(self, surface):
        """Draw game info and controls"""
        controls = [
            "WASD: Move | Shift: Sprint | Space: Attack",
            "Ctrl+S: Save | P: Pause | Tab: Inventory"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            surface.blit(text, (10, SCREEN_HEIGHT - 50 + i * 20))
    
    def _draw_debug_info(self, surface):
        """Draw debug information"""
        debug_info = [
            f"Pos: {self.player.x:.0f}, {self.player.y:.0f}",
            f"Kills: {self.player.kills}",
            f"Exp: {self.player.experience}/{self.player.exp_to_next_level}",
        ]
        
        for i, info in enumerate(debug_info):
            text = self.font_small.render(info, True, CYAN)
            surface.blit(text, (SCREEN_WIDTH - 200, 200 + i * 20))
    
    def _draw_bar(self, surface, x, y, width, height, ratio, color):
        """Draw a progress bar"""
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(surface, color, (x, y, width * max(0, ratio), height))
        pygame.draw.rect(surface, WHITE, (x, y, width, height), 1)
