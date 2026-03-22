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
test_enemy = Enemy(level_map.get_waypoints()) 
enemy_list.append(test_enemy)

tower_list = []
player_money = 500 # <--- CYCLE 6: STARTING BALANCE

projectile_list = []

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
                    
                    # Check if the player has enough gold
                    if player_money >= new_tower.cost: 
                        tower_list.append(new_tower)
                        
                        # Deduct the cost from the player's money
                        player_money -= new_tower.cost 
                        print(f"Tower Placed! Remaining money: {player_money}")
                    else:
                        print(f"Invalid: Insufficient funds. You only have {player_money} gold.")
                else:
                    print("Invalid: Tower already exists here.")

    # Updates
    for enemy in enemy_list:
        enemy.update(dt)
        
    for tower in tower_list:
        tower.update(dt, enemy_list, projectile_list)
        
    for proj in projectile_list:
        proj.update(dt)
        
    # Clean up inactive projectiles (bullets that hit their target)
    projectile_list = [p for p in projectile_list if p.active]
    
    # Clean up dead enemies and give the player money!
    for enemy in enemy_list:
        if enemy.hp <= 0:
            player_money += enemy.reward
            print(f"Enemy killed! +{enemy.reward} gold. Total: {player_money}")
    enemy_list = [e for e in enemy_list if e.hp > 0]

    # ----------------------------------------------
    # Drawing
    # ----------------------------------------------
    screen.fill(BLACK)
    
    # 1. Draw the map (Bottom Layer)
    level_map.draw(screen) 
    
    # 2. Draw placed towers
    for tower in tower_list:
        tower.draw(screen)
    
    # 3. Draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)

    # 4. Draw projectiles (Top Layer)
    for proj in projectile_list:
        proj.draw(screen)

    # --- CYCLE 3 & 4: MOUSE HOVER & GHOST TOWER ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_col = mouse_x // level_map.tile_size
    grid_row = mouse_y // level_map.tile_size
    grid_x = grid_col * level_map.tile_size
    grid_y = grid_row * level_map.tile_size
    
    highlight = pygame.Surface((level_map.tile_size, level_map.tile_size))
    highlight.set_alpha(128) 

    if level_map.is_buildable(mouse_x, mouse_y):
        # Draw Green valid box
        highlight.fill((0, 255, 0)) 
        screen.blit(highlight, (grid_x, grid_y))
        
        # Draw Ghost Tower (Transparent Blue Square)
        ghost_tower = pygame.Surface((40, 40))
        ghost_tower.fill(BLUE)
        ghost_tower.set_alpha(150) 
        ghost_rect = ghost_tower.get_rect(center=(grid_x + 32, grid_y + 32))
        screen.blit(ghost_tower, ghost_rect)
        
        # Draw the Range Indicator (White Circle)
        pygame.draw.circle(screen, WHITE, (grid_x + 32, grid_y + 32), 150, 2)
    else:
        # Draw Red invalid box
        highlight.fill((255, 0, 0)) 
        screen.blit(highlight, (grid_x, grid_y))
    # ----------------------------------------------

    pygame.display.flip()
pygame.quit()
sys.exit()
