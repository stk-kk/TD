import pygame
from settings import *

class Map:
    # --- CYCLE 15: ADD DIFFICULTY PARAMETER ---
    def __init__(self, filename, difficulty="normal"):
        self.tile_size = 64 
        self.grid_map = []
        self.difficulty = difficulty # Store the difficulty!
        
        with open(filename, 'r') as file:
            for line in file:
                row = [int(char) for char in line.strip()]
                self.grid_map.append(row)
        
        if "map2" in filename:
            self.waypoints = [(96, 96), (1120, 96), (1120, 544), (96, 544), (96, 96)]
        else:
            self.waypoints = [
                (96, 96), (416, 96), (416, 288), (800, 288), (800, 96), 
                (1120, 96), (1120, 480), (608, 480), (608, 608), (416, 608), 
                (416, 480), (288, 480), (288, 608), (96, 608), (96, 96)
            ]

    def draw(self, screen):
        for row_idx, row in enumerate(self.grid_map):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                
                # --- CYCLE 15: DYNAMIC TILE COLORS ---
                if self.difficulty == "hard":
                    # Hard Mode Colors (Red Theme)
                    grass_color = (100, 20, 20)  # Dark, ominous red
                    path_color = (200, 50, 50)   # Bright red path
                else:
                    # Normal Mode Colors (Standard Green/Brown)
                    grass_color = (34, 139, 34)  # Forest Green
                    path_color = (210, 180, 140) # Tan/Dirt

                # Draw Path (0) or Grass (1)
                if tile == 0:
                    pygame.draw.rect(screen, path_color, (x, y, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(screen, grass_color, (x, y, self.tile_size, self.tile_size))
                    # Optional: Grid lines for grass
                    pygame.draw.rect(screen, (20, 100, 20) if self.difficulty == "normal" else (60, 10, 10), (x, y, self.tile_size, self.tile_size), 1)

    def get_waypoints(self):
        return self.waypoints
    
    def is_buildable(self, mouse_x, mouse_y):
        col = mouse_x // self.tile_size
        row = mouse_y // self.tile_size
        if row < 0 or row >= len(self.grid_map) or col < 0 or col >= len(self.grid_map[0]):
            return False
        if self.grid_map[row][col] == 1:
            return True
        else:
            return False