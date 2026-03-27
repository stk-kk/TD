import pygame
from settings import *

class Map:
    def __init__(self, filename):
        self.tile_size = 64 
        self.grid_map = []
        
        # --- CYCLE 13: FILE HANDLING ---
        # Opens the text file and read the map layout
        with open(filename, 'r') as file:
            for line in file:
                # Remove hidden characters and convert string numbers to integers
                row = [int(char) for char in line.strip()]
                self.grid_map.append(row)
        
        self.waypoints = [
            (96, 96), (416, 96), (416, 288), (800, 288), (800, 96), 
            (1120, 96), (1120, 480), (608, 480), (608, 608), (416, 608), 
            (416, 480), (288, 480), (288, 608), (96, 608), (96, 96)
        ]

    def draw(self, screen):
        for row_index, row in enumerate(self.grid_map):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if tile == 1:
                    color = (34, 139, 34)
                else:
                    color = (139, 69, 19)
                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))
                pygame.draw.rect(screen, (50, 50, 50), (x, y, self.tile_size, self.tile_size), 1)

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