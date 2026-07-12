"""
Main Game Class - Handles game loop and state management
"""

import pygame
import os
from config import *
from src.player import Player
from src.world import World
from src.ui import UI
from src.save_system import SaveSystem
from src.enemy import EnemyManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False
        self.show_menu = True
        self.frame_count = 0
        
        # Game objects
        self.player = None
        self.world = None
        self.ui = None
        self.save_system = SaveSystem()
        self.enemy_manager = None
        
        # Menu state
        self.menu_state = "main"  # main, load, settings, game
        self.saves = []
        self.selected_save = 0
        
    def load_game(self, save_file=None):
        """Initialize new game or load existing save"""
        if save_file and os.path.exists(save_file):
            game_data = self.save_system.load_game(save_file)
            self.player = Player(game_data['player']['x'], game_data['player']['y'])
            self.player.health = game_data['player']['health']
            self.player.hunger = game_data['player']['hunger']
            self.player.energy = game_data['player']['energy']
            self.player.stamina = game_data['player']['stamina']
            self.player.kills = game_data['player'].get('kills', 0)
            self.player.level = game_data['player'].get('level', 1)
            self.world = World(game_data.get('world_seed', 42))
        else:
            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.world = World()
        
        self.ui = UI()
        self.enemy_manager = EnemyManager()
        self.show_menu = False
        self.menu_state = "game"
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.show_menu:
                    self._handle_menu_input(event)
                else:
                    self._handle_game_input(event)
    
    def _handle_menu_input(self, event):
        """Handle menu navigation"""
        if self.menu_state == "main":
            if event.key == pygame.K_1:
                self.load_game()
            elif event.key == pygame.K_2:
                self.menu_state = "load"
            elif event.key == pygame.K_3:
                self.running = False
        elif self.menu_state == "load":
            if event.key == pygame.K_UP:
                self.selected_save = max(0, self.selected_save - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_save = min(len(self.saves) - 1, self.selected_save + 1)
            elif event.key == pygame.K_RETURN:
                if self.saves:
                    self.load_game(self.saves[self.selected_save])
            elif event.key == pygame.K_ESCAPE:
                self.menu_state = "main"
    
    def _handle_game_input(self, event):
        """Handle in-game input"""
        if event.key == pygame.K_ESCAPE:
            self.show_menu = True
            self.menu_state = "main"
        elif event.key == pygame.K_p:
            self.paused = not self.paused
        elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._save_game()
    
    def update(self):
        """Update game state"""
        if not self.paused and not self.show_menu:
            self.frame_count += 1
            self.player.update()
            self.world.update()
            self.enemy_manager.update(self.player, self.world)
            self.ui.update(self.player)
            
            # Auto-save
            if self.frame_count % AUTO_SAVE_INTERVAL == 0:
                self._save_game(auto=True)
            
            # Check game over
            if self.player.health <= 0:
                self.game_over = True
    
    def draw(self):
        """Render graphics"""
        self.screen.fill(DARK_GREEN)
        
        if self.show_menu:
            self._draw_menu()
        else:
            # Draw world
            self.world.draw(self.screen)
            
            # Draw enemies
            self.enemy_manager.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # Draw UI
            self.ui.draw(self.screen)
            
            # Draw pause overlay
            if self.paused:
                self._draw_pause_screen()
            
            # Draw game over
            if self.game_over:
                self._draw_game_over()
        
        pygame.display.flip()
    
    def _draw_menu(self):
        """Draw main menu"""
        if self.menu_state == "main":
            font_title = pygame.font.Font(None, 72)
            font_option = pygame.font.Font(None, 36)
            
            title = font_title.render("WOLF GAME", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            new_game = font_option.render("1. New Game", True, YELLOW)
            load_game = font_option.render("2. Load Game", True, WHITE)
            quit_game = font_option.render("3. Quit", True, WHITE)
            
            self.screen.blit(new_game, (SCREEN_WIDTH // 2 - new_game.get_width() // 2, 300))
            self.screen.blit(load_game, (SCREEN_WIDTH // 2 - load_game.get_width() // 2, 380))
            self.screen.blit(quit_game, (SCREEN_WIDTH // 2 - quit_game.get_width() // 2, 460))
        
        elif self.menu_state == "load":
            self._draw_load_menu()
    
    def _draw_load_menu(self):
        """Draw load game menu"""
        self.saves = self.save_system.list_saves()
        
        font_title = pygame.font.Font(None, 48)
        font_text = pygame.font.Font(None, 32)
        
        title = font_title.render("Load Game", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        if not self.saves:
            no_saves = font_text.render("No saves found", True, RED)
            self.screen.blit(no_saves, (SCREEN_WIDTH // 2 - no_saves.get_width() // 2, 200))
        else:
            for i, save_file in enumerate(self.saves):
                save_name = os.path.basename(save_file)
                color = YELLOW if i == self.selected_save else WHITE
                text = font_text.render(f"{'> ' if i == self.selected_save else '  '}{save_name}", True, color)
                self.screen.blit(text, (150, 150 + i * 50))
        
        back = font_text.render("ESC: Back", True, WHITE)
        self.screen.blit(back, (50, SCREEN_HEIGHT - 50))
    
    def _draw_pause_screen(self):
        """Draw pause menu overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 48)
        text = font.render("PAUSED", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))
        
        font_small = pygame.font.Font(None, 24)
        hint = font_small.render("Press P to resume", True, WHITE)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 
                               SCREEN_HEIGHT // 2 + 60))
    
    def _draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.Font(None, 72)
        font_text = pygame.font.Font(None, 36)
        
        title = font_title.render("GAME OVER", True, RED)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        
        stats = [
            f"Level: {self.player.level}",
            f"Kills: {self.player.kills}",
            f"Survived: {self.frame_count // 3600}h {(self.frame_count % 3600) // 60}m"
        ]
        
        for i, stat in enumerate(stats):
            text = font_text.render(stat, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350 + i * 50))
    
    def _save_game(self, auto=False):
        """Save current game state"""
        game_data = {
            'player': {
                'x': self.player.x,
                'y': self.player.y,
                'health': self.player.health,
                'hunger': self.player.hunger,
                'energy': self.player.energy,
                'stamina': self.player.stamina,
                'kills': self.player.kills,
                'level': self.player.level,
            },
            'world_seed': self.world.seed,
            'frame_count': self.frame_count,
        }
        
        self.save_system.save_game(game_data, auto=auto)
        if not auto:
            print("Game saved successfully!")
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
