import pygame
import sys
from settings import *
from entities import Enemy, Tower
from map import Map  # <--- NEW IMPORT

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence - Cycle 2")
clock = pygame.time.Clock()

# --- Initialize Map ---
level_map = Map()  # <--- Create the map object

# --- Game State ---
enemy_list = [] 
tower_list = []

# Spawn test enemy using the MAP's waypoints
test_enemy = Enemy(level_map.get_waypoints()) 
enemy_list.append(test_enemy)

# --- Main Game Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # --- CYCLE 5: TOWER PLACEMENT ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 = Left Click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # 1. Get grid indices
            grid_col = mouse_x // level_map.tile_size
            grid_row = mouse_y // level_map.tile_size
            
            # 2. Check if the map tile is grass
            if level_map.is_buildable(mouse_x, mouse_y):
                
                # 3. Validation: Check if a tower is ALREADY on this tile
                position_empty = True
                for t in tower_list:
                    if t.grid_x == grid_col and t.grid_y == grid_row:
                        position_empty = False
                        break 
                
                # 4. If empty, append a new tower to the list
                if position_empty:
                    new_tower = Tower(grid_col, grid_row)
                    tower_list.append(new_tower)
                    print("Tower Placed!")
                else:
                    print("Invalid: Tower already exists here.")
            else:
                print("Invalid: Cannot build on the path.")
        # --------------------------------

    # Updates
    for enemy in enemy_list:
        enemy.update(dt)

    # Drawing
    screen.fill(BLACK)
    
    level_map.draw(screen) 
    
    for enemy in enemy_list:
        enemy.draw(screen)

    # --- CYCLE 3 & 4: MOUSE HOVER & GHOST TOWER ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    grid_col = mouse_x // level_map.tile_size
    grid_row = mouse_y // level_map.tile_size
    grid_x = grid_col * level_map.tile_size
    grid_y = grid_row * level_map.tile_size
    
    highlight = pygame.Surface((level_map.tile_size, level_map.tile_size))
    highlight.set_alpha(128) 

    level_map.draw(screen) 
    
    # --- CYCLE 5: DRAW PLACED TOWERS ---
    for tower in tower_list:
        tower.draw(screen)
    # -----------------------------------
    
    for enemy in enemy_list:
        enemy.draw(screen)
    
    if level_map.is_buildable(mouse_x, mouse_y):
        # 1. Draw Green valid box
        highlight.fill((0, 255, 0)) 
        screen.blit(highlight, (grid_x, grid_y))
        
        # 2. Draw Ghost Tower (Transparent Blue Square)
        ghost_tower = pygame.Surface((40, 40))
        ghost_tower.fill(BLUE)
        ghost_tower.set_alpha(150) # Make it semi-transparent
        ghost_rect = ghost_tower.get_rect(center=(grid_x + 32, grid_y + 32))
        screen.blit(ghost_tower, ghost_rect)
        
        # 3. Draw the Range Indicator (White Circle)
        # It is 150 here because that matches the self.range in the Tower class
        pygame.draw.circle(screen, WHITE, (grid_x + 32, grid_y + 32), 150, 2)
        
    else:
        # Draw Red invalid box
        highlight.fill((255, 0, 0)) 
        screen.blit(highlight, (grid_x, grid_y))
    # ----------------------------------------------

    pygame.display.flip()

pygame.quit()
sys.exit()
