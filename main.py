import pygame
import sys
from settings import *
from entities import Enemy, Tower, SniperTower, RapidTower  # <--- NEW IMPORTS
from map import Map  # <--- NEW IMPORT

# --- Setup ---
pygame.init()
pygame.font.init() # <--- CYCLE 9: INITIALIZE FONTS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence - Cycle 9")
clock = pygame.time.Clock()

ui_font = pygame.font.SysFont('Arial', 24, bold=True)

# --- Initialize Map ---
level_map = Map()  # <--- Create the map object

# --- Game State ---
enemy_list = [] 
test_enemy = Enemy(level_map.get_waypoints()) 
enemy_list.append(test_enemy)

tower_list = []
player_money = 500
player_health = 100
projectile_list = []

current_selection = 1 # 1=Basic, 2=Sniper, 3=Rapid

# --- Main Game Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- CYCLE 8: SELECT TOWER TYPE ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_selection = 1
                print("Selected: Basic Tower (100g)")
            elif event.key == pygame.K_2:
                current_selection = 2
                print("Selected: Sniper Tower (250g)")
            elif event.key == pygame.K_3:
                current_selection = 3
                print("Selected: Rapid Tower (150g)")
            
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
                
                # 4. If empty, append the SELECTED tower to the list
                if position_empty:
                    # Instantiate the correct class based on selection
                    if current_selection == 1:
                        new_tower = Tower(grid_col, grid_row)
                    elif current_selection == 2:
                        new_tower = SniperTower(grid_col, grid_row) # Instantiate Child Class
                    elif current_selection == 3:
                        new_tower = RapidTower(grid_col, grid_row)  # Instantiate Child Class
                    
                    # Check if the player has enough gold
                    if player_money >= new_tower.cost: 
                        tower_list.append(new_tower)
                        player_money -= new_tower.cost 
                        print(f"Tower Placed! Remaining money: {player_money}")
                    else:
                        print(f"Invalid: Insufficient funds. You need {new_tower.cost} gold.")
                else:
                    print("Invalid: Tower already exists here.")

  # --------------------------------------------------------
    # --- Updates ---
    # 1. Move everything (THIS IS WHAT WAS MISSING!)
    for enemy in enemy_list:
        enemy.update(dt) 
        
    for tower in tower_list:
        tower.update(dt, enemy_list, projectile_list)
        
    for proj in projectile_list:
        proj.update(dt)
        
    # 2. Clean up inactive projectiles (bullets that hit their target)
    projectile_list = [p for p in projectile_list if p.active]
    
    # 3. Clean up dead enemies OR enemies that reached the base
    for enemy in enemy_list:
        if enemy.hp <= 0:
            player_money += enemy.reward
            
        # Check if the enemy reached the last waypoint on the path
        elif enemy.path_index >= len(enemy.path) - 1:
            player_health -= 10 # Take 10 damage!
            enemy.hp = 0        # Force the enemy to "die" so it gets deleted
            
    # 4. Officially delete them from the game
    enemy_list = [e for e in enemy_list if e.hp > 0]
    # --------------------------------------------------------
    # ----------------------------------------------
    # Drawing
    # ----------------------------------------------
    
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

    # --- CYCLE 9: DRAW USER INTERFACE (GUI) ---
    # 1. Drawing a dark grey UI bar at the top of the screen
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (SCREEN_WIDTH, 40), 2) # White border line

    # 2. Render Text 
    health_text = ui_font.render(f"Base Health: {player_health}", True, (255, 100, 100)) # Light Red text
    money_text = ui_font.render(f"Gold: {player_money}", True, (255, 215, 0))          # Gold text
    
    # 3. Determine which tower text to show based on your keyboard selection
    if current_selection == 1: 
        tower_info = "Basic (100g) | DMG: 1 | SPD: Normal"
    elif current_selection == 2: 
        tower_info = "Sniper (250g) | DMG: 5 | SPD: Slow"
    elif current_selection == 3: 
        tower_info = "Rapid (150g) | DMG: 1 | SPD: Fast"
        
    selection_text = ui_font.render(f"Selected: {tower_info}", True, (255, 255, 255))

    # 4. Blit (Draw) the text onto the screen
    screen.blit(health_text, (20, 10))
    screen.blit(money_text, (200, 10))
    screen.blit(selection_text, (400, 10))

    # ----------------------------------------------

    pygame.display.flip()
pygame.quit()
sys.exit()
