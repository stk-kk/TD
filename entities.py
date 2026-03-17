# entities.py
import pygame
from settings import *

class Enemy:
    def __init__(self, path):
        # Attributes from Design 
        self.hp = 10
        self.speed = 2.0  # Float for precision
        self.reward = 5
        self.path_index = 0
        self.path = path # Store path logic
        
        # Visuals (Placeholder red square for now)
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        
        # Start at the first point of the path
        start_pos = self.path[0]
        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        """ Moves the enemy. Matches 'move_along_path' logic. """
        self.move_along_path(dt)

    def move_along_path(self, dt):
        # 1. Target the next node
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            target_x, target_y = target
            
            # Simple movement logic (We will upgrade this to Vectors later)
            dir_x = target_x - self.x
            dir_y = target_y - self.y
            
            # Move towards target
            # Note: This is a simplified version for the skeleton
            self.x += (dir_x * 0.05) * self.speed 
            self.y += (dir_y * 0.05) * self.speed
            
            # Update physical position
            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)
            
            # Check if close to target node (snap to it)
            if abs(dir_x) < 5 and abs(dir_y) < 5:
                self.path_index += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Tower:
    def __init__(self, grid_x, grid_y):
        # --- NEW CYCLE 5 ADDITIONS ---
        self.grid_x = grid_x
        self.grid_y = grid_y
        # -----------------------------
        
        # Calculate the exact pixel center of the 64x64 tile
        self.pixel_x = (grid_x * 64) + 32
        self.pixel_y = (grid_y * 64) + 32
        
        # ... (keep the rest of your stats and visual code exactly the same)
        
        # Base stats (from Design)
        self.range = 150
        self.damage = 1
        self.fire_rate = 1.0
        self.cooldown = 0
        
        # Visuals (blue square for now)
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect(center=(self.pixel_x, self.pixel_y))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
