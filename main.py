import pygame
import sys
from settings import *
from entities import Enemy, FastEnemy, BossEnemy, Tower, SniperTower, RapidTower 
from map import Map
from wave import WaveManager

# --- Setup ---
pygame.init()
pygame.font.init() # <--- CYCLE 9: INITIALIZE FONTS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence - Cycle 9")
clock = pygame.time.Clock()

ui_font = pygame.font.SysFont('Arial', 24, bold=True)

# --- Initialize Map ---
level_map = Map("levels/map.txt")  # <--- Create the map object

# --- Game State ---
enemy_list = [] 

tower_list = []
player_money = 500
player_lives = 5
projectile_list = []

current_selection = 1 # 1=Basic, 2=Sniper, 3=Rapid

warning_text=""
warning_timer=0.0

wave_manager = WaveManager(level_map)

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

                # --- CYCLE 11: RESTART GAME ---
            elif event.key == pygame.K_r:
                # 1. Remove all the entities off the map
                enemy_list.clear()
                tower_list.clear()
                projectile_list.clear()
                
                # 2. Reset the players stats
                player_money = 500
                player_lives = 5
                current_selection = 1
                
                # 3. Create a brand new WaveManager to reset the waves
                wave_manager = WaveManager(level_map)
                print("Game Restarted!")
            
 # --- CYCLE 5 & 12: TOWER PLACEMENT AND SELLING ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_col = mouse_x // level_map.tile_size
            grid_row = mouse_y // level_map.tile_size
            
            # --- LEFT CLICK: BUY TOWER ---
            if event.button == 1: 
                if level_map.is_buildable(mouse_x, mouse_y):
                    position_empty = True
                    for t in tower_list:
                        if t.grid_x == grid_col and t.grid_y == grid_row:
                            position_empty = False
                            break 
                    
                    if position_empty:
                        if current_selection == 1: new_tower = Tower(grid_col, grid_row)
                        elif current_selection == 2: new_tower = SniperTower(grid_col, grid_row)
                        elif current_selection == 3: new_tower = RapidTower(grid_col, grid_row)
                        
                        # Check if the player has enough gold
                        if player_money >= new_tower.cost:
                            tower_list.append(new_tower)
                            player_money -= new_tower.cost
                            # Clear any warnings if successful
                            warning_timer = 0.0 
                        else:
                            # --- TRIGGER: NOT ENOUGH GOLD ---
                            warning_text = "Insufficient funds!"
                            warning_timer = 2.0
                    else:
                        # --- TRIGGER: TOWER ALREADY EXISTS ---
                        warning_text = "Position occupied!"
                        warning_timer = 2.0
                else:
                    # --- TRIGGER: INVALID PLACEMENT ---
                    warning_text = "Cannot build on the path!"
                    warning_timer = 2.0
            
            # --- RIGHT CLICK: SELL TOWER ---
            elif event.button == 3:
                for t in tower_list:
                    # If there is a tower at the coordinates of the right-click
                    if t.grid_x == grid_col and t.grid_y == grid_row:
                        refund = t.cost // 2  # Calculate 50% refund (integer division)
                        player_money += refund
                        tower_list.remove(t)  # Delete the tower
                        print(f"Tower Sold! Refunded {refund} gold.")
                        break # Stop searching once the tower has been found and sold

    # --- Updates ---
    
    # Update warning timer
    if warning_timer > 0:
        warning_timer -= dt
    
    # 1. Check for Game Over
    if player_lives <= 0:
        wave_manager.game_over = True
        
    # 2. Update the Wave Manager (This spawns the enemies)
    wave_manager.update(dt, enemy_list)
    
     # 1. Move everything 
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
            player_lives -= 1   # Lose 1 life
            enemy.hp = 0        # Force the enemy to "die" so it gets deleted
            
    # 4. Officially delete them from the game
    enemy_list = [e for e in enemy_list if e.hp > 0]

    # --- DRAWING ---
    
    # 1. WIPE THE SCREEN CLEAN EVERY FRAME
    screen.fill((20, 20, 20)) # Fills the empty space with dark grey
    
    # 2. Draw the Map
    level_map.draw(screen)
    
    # 3. Draw placed towers
    for tower in tower_list:
        tower.draw(screen)
    
    # 3. Draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)

    # 4. Draw projectiles (Top Layer)
    for proj in projectile_list:
        proj.draw(screen)

    # --- CYCLE 3 & 4: MOUSE HOVER & PREVIEW TOWER ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_col = mouse_x // level_map.tile_size
    grid_row = mouse_y // level_map.tile_size
    grid_x = grid_col * level_map.tile_size
    grid_y = grid_row * level_map.tile_size
    
    highlight = pygame.Surface((level_map.tile_size, level_map.tile_size))
    highlight.set_alpha(128) 

    # Check if we are hovering over a valid grass tile
    if level_map.is_buildable(mouse_x, mouse_y):
        
        # 1. Dynamically create the correct preview tower based on keyboard selection
        if current_selection == 1:
            preview_tower = Tower(grid_col, grid_row)
        elif current_selection == 2:
            preview_tower = SniperTower(grid_col, grid_row)
        elif current_selection == 3:
            preview_tower = RapidTower(grid_col, grid_row)
            
        # 2. Make the preview image semi-transparent
        preview_image = preview_tower.image.copy()
        preview_image.set_alpha(150)
        
        # 3. Draw the preview image
        screen.blit(preview_image, preview_tower.rect)
        
        # 4. Draw the dynamic range circle
        center_x = (grid_col * level_map.tile_size) + (level_map.tile_size // 2)
        center_y = (grid_row * level_map.tile_size) + (level_map.tile_size // 2)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), preview_tower.range, 2)
    else:
        # Draw Red invalid box
        highlight.fill((255, 0, 0)) 
        screen.blit(highlight, (grid_x, grid_y))

    # --- CYCLE 9 & 10: DRAW USER INTERFACE (GUI) 
    # 1. Drawing a dark grey UI bar at the top of the screen
    pygame.draw.rect(screen, (40, 40, 40), (0, 0, SCREEN_WIDTH, 40))
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (SCREEN_WIDTH, 40), 2) # White border line

    # 2. Render Base Health and Gold
    lives_text = ui_font.render(f"Lives: {player_lives}", True, (255, 100, 100)) # Light Red
    money_text = ui_font.render(f"Gold: {player_money}", True, (255, 215, 0))       # Gold
    
    # 3. Render Selected Tower (Shortened slightly to stop text clipping)
    if current_selection == 1: 
        tower_info = "Basic (100g) | DMG:1 | SPD:Med"
    elif current_selection == 2: 
        tower_info = "Sniper (250g) | DMG:5 | SPD:Slow"
    elif current_selection == 3: 
        tower_info = "Rapid (150g) | DMG:1 | SPD:Fast"
        
    selection_text = ui_font.render(f"Selected: {tower_info}", True, (255, 255, 255))

    # 4. Render Wave Status
    if wave_manager.game_over:
        wave_text = ui_font.render("GAME OVER", True, (255, 0, 0))
    elif wave_manager.game_won:
        wave_text = ui_font.render("YOU WIN!", True, (0, 255, 0))
    else:
        status = f"Wave: {wave_manager.current_wave + 1}/{len(wave_manager.waves)}"
        if not wave_manager.wave_active:
            countdown = int(wave_manager.wave_delay - wave_manager.wave_timer)
            status += f" (Next in {countdown}s)"
        wave_text = ui_font.render(status, True, (200, 200, 255)) # Light blue text

    # 5. Blit (Draw) the text onto the screen with actual spacing this time
    screen.blit(lives_text, (10, 10))
    screen.blit(money_text, (160, 10))
    screen.blit(selection_text, (330, 10))
    
    # Aligningthe wave text so it stays perfectly on the right side of the screen
    wave_rect = wave_text.get_rect(topright=(SCREEN_WIDTH - 20, 10))
    screen.blit(wave_text, wave_rect)

    # --- DRAW WARNING MESSAGE ---
    if warning_timer > 0:
        # Render the text in bright red
        warning_surface = ui_font.render(warning_text, True, (255, 50, 50))
        
        # Center it on the screen
        warning_rect = warning_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Draw a black box behind the text so it stands out against the grass
        bg_rect = warning_rect.inflate(20, 10) # Makes the box slightly larger than the text
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 50, 50), bg_rect, 2) # Red border
        
        # Blit the text
        screen.blit(warning_surface, warning_rect)
    
    # ----------------------------------------------

    pygame.display.flip()
pygame.quit()
sys.exit()
