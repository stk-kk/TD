import pygame
from settings import *

class Map:
    def __init__(self):
        # 1 = Grass (Buildable), 0 = Path (Not Buildable)
        # This matches your design: "tiles and path which indicate different sections"
        # 11 rows, 20 columns
        # self.grid_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # 11 Rows, 20 Columns (Fills a 1280x720 screen)
         self.grid_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        # Define the exact coordinates the enemy must follow
        # These correspond roughly to the '0's in the grid above
        # UPDATED WAYPOINTS: Calculated to exactly follow the 0s in the grid_map
        # Formula used: (ColIndex * 64) + 32, (RowIndex * 64) + 32
        # self.waypoints = [
            (96, 96),    # 1. Start at top-left 
            (96, 352),   # 2. Down to bottom-left 
            (352, 352),  # 3. Right along the bottom 
            (736, 160),  # 4. Up the right side 
            (480, 160),  # 5. Left along the top 
            (480, 224),  # 6. Down a step 
            (288, 224),  # 7. Left a step
            (288, 96)    # 8. Up to the end of the maze
        ]
        
        # UPDATED WAYPOINTS: Fills the 1280x720 screen
        # Formula: (ColIndex * 64) + 32, (RowIndex * 64) + 32
        self.waypoints = [
            (96, 96),     # 1. Start: Top-Left (Row 1, Col 1)
            (416, 96),    # 2. Right to (Row 1, Col 6)
            (416, 288),   # 3. Down to (Row 4, Col 6)
            (800, 288),   # 4. Right to (Row 4, Col 12)
            (800, 96),    # 5. Up to (Row 1, Col 12)
            (1120, 96),   # 6. Right to (Row 1, Col 17)
            (1120, 480),  # 7. Down to (Row 7, Col 17)
            (608, 480),   # 8. Left to (Row 7, Col 9)
            (608, 608),   # 9. Down to (Row 9, Col 9)
            (416, 608),   # 10. Left to (Row 9, Col 6)
            (416, 480),   # 11. Up to (Row 7, Col 6)
            (288, 480),   # 12. Left to (Row 7, Col 4)
            (288, 608),   # 13. Down to (Row 9, Col 4)
            (96, 608)     # 14. End: Left to Bottom-Left (Row 9, Col 1)
        
        # 8. Up to the end of the maze
        ]
        
        self.tile_size = 64 

    def draw(self, screen):
        """ Draws the grid to the screen for visualization """
        for row_index, row in enumerate(self.grid_map):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                
                # Draw Grass (Green) or Path (Brown)
                if tile == 1:
                    color = (34, 139, 34) # Forest Green
                else:
                    color = (139, 69, 19) # Saddle Brown
                
                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))
                
                # Draw grid lines (helps with testing alignment)
                pygame.draw.rect(screen, (50, 50, 50), (x, y, self.tile_size, self.tile_size), 1)

    

    def get_waypoints(self):
        return self.waypoints
    
    def is_buildable(self, mouse_x, mouse_y):
        """ Checks if the tile under the mouse is grass (1) or path (0) """
        #  Convert pixel coordinates to grid indices using integer division
        col = mouse_x // self.tile_size
        row = mouse_y // self.tile_size

        #  Prevent crashing if the mouse goes outside the game window
        if row < 0 or row >= len(self.grid_map) or col < 0 or col >= len(self.grid_map[0]):
            return False

        #  Check the array: return True if it's grass (1)
        if self.grid_map[row][col] == 1:
            return True
        else:
            return False
        
        
