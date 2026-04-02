import pygame
import sys
from settings import *
from entities import Enemy, FastEnemy, BossEnemy, Tower, SniperTower, RapidTower 
from map import Map
from wave import WaveManager

# Initialize Pygame and font system
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence - Final Build")
clock = pygame.time.Clock()

# Load UI font
ui_font = pygame.font.SysFont('Arial', 24, bold=True)

# Initialize map object from external text file
level_map = Map("levels/map.txt")

# Define game state variables and entity lists
enemy_list = [] 
tower_list = []
player_money = 500
player_lives = 5
projectile_list = []

# Track currently selected tower type (1=Basic, 2=Sniper, 3=Rapid)
current_selection = 1 

# Variables for displaying user warnings
warning_text = ""
warning_timer = 0.0

# Initialize the wave manager to handle enemy spawning
wave_manager = WaveManager(level_map)

# Define application states for the finite state machine
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"

# Set initial application state to the main menu
current_state = STATE_MENU

# Main application loop
running = True
while running:
    # Calculate delta time in seconds
    dt = clock.tick(FPS) / 1000.0 
    
    # Process application events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard inputs
        if event.type == pygame.KEYDOWN:
            # Tower selection keys
            if event.key == pygame.K_1: current_selection = 1
            elif event.key == pygame.K_2: current_selection = 2
            elif event.key == pygame.K_3: current_selection = 3
                
            # Reset game state to initial values
            elif event.key == pygame.K_r:
                enemy_list.clear()
                tower_list.clear()
                projectile_list.clear()
                player_money = 500
                player_lives = 5
                current_selection = 1
                wave_manager = WaveManager(level_map)
                print("Game Restarted.")

            # Toggle between playing and paused states
            elif event.key == pygame.K_p:
                if current_state == STATE_PLAYING:
                    current_state = STATE_PAUSED
                elif current_state == STATE_PAUSED:
                    current_state = STATE_PLAYING

        # Handle mouse inputs
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Mouse clicks while on the main menu
            if current_state == STATE_MENU:
                if event.button == 1:
                    # Define play button hitbox and check for collision
                    play_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 60)
                    if play_button_rect.collidepoint(mouse_x, mouse_y):
                        current_state = STATE_PLAYING
                        
            # Mouse clicks while actively playing the game
            elif current_state == STATE_PLAYING:
                grid_col = mouse_x // level_map.tile_size
                grid_row = mouse_y // level_map.tile_size
                
                # Left click logic for buying and placing towers
                if event.button == 1: 
                    if level_map.is_buildable(mouse_x, mouse_y):
                        # Check if the tile is already occupied by another tower
                        position_empty = True
                        for t in tower_list:
                            if t.grid_x == grid_col and t.grid_y == grid_row:
                                position_empty = False
                                break 
                        
                        # Instantiate the selected tower type if position is valid
                        if position_empty:
                            if current_selection == 1: new_tower = Tower(grid_col, grid_row)
                            elif current_selection == 2: new_tower = SniperTower(grid_col, grid_row)
                            elif current_selection == 3: new_tower = RapidTower(grid_col, grid_row)
                            
                            # Process purchase if the player has sufficient funds
                            if player_money >= new_tower.cost:
                                tower_list.append(new_tower)
                                player_money -= new_tower.cost
                                warning_timer = 0.0 
                            else:
                                warning_text = "Insufficient funds."
                                warning_timer = 2.0
                        else:
                            warning_text = "Position occupied."
                            warning_timer = 2.0
                    else:
                        warning_text = "Cannot build on the path."
                        warning_timer = 2.0
            
                # Right click logic for selling towers
                elif event.button == 3:
                    for t in tower_list:
                        if t.grid_x == grid_col and t.grid_y == grid_row:
                            # Calculate 50 percent refund and remove the tower
                            refund = t.cost // 2 
                            player_money += refund
                            tower_list.remove(t) 
                            break 


    # Update logic block, only executes when playing
    if current_state == STATE_PLAYING:
        
        # Decrease warning text timer
        if warning_timer > 0:
            warning_timer -= dt
        
        # Trigger game over condition if lives reach zero
        if player_lives <= 0:
            wave_manager.game_over = True
            
        # Process enemy spawning algorithm
        wave_manager.update(dt, enemy_list)
        
        # Update positions and states for all game entities
        for enemy in enemy_list:
            enemy.update(dt) 
            
        for tower in tower_list:
            tower.update(dt, enemy_list, projectile_list)
            
        for proj in projectile_list:
            proj.update(dt)
            
        # Filter out inactive projectiles
        projectile_list = [p for p in projectile_list if p.active]
        
        # Process enemy death and track path completion
        for enemy in enemy_list:
            # Award gold for defeated enemies
            if enemy.hp <= 0:
                player_money += enemy.reward
            # Deduct lives for enemies that reach the end of the path
            elif enemy.path_index >= len(enemy.path) - 1:
                player_lives -= 1   
                enemy.hp = 0        
                
        # Filter out defeated enemies
        enemy_list = [e for e in enemy_list if e.hp > 0]


    # Rendering block, handles drawing based on current application state
    
    if current_state == STATE_MENU:
        # Render the main menu screen
        screen.fill((30, 40, 50)) 
        
        # Render title text
        title_text = ui_font.render("TOWER DEFENCE", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3)))
        
        # Render play button and text
        play_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 60)
        pygame.draw.rect(screen, (0, 200, 0), play_btn)
        pygame.draw.rect(screen, (255, 255, 255), play_btn, 3) 
        
        play_text = ui_font.render("PLAY GAME", True, (255, 255, 255))
        screen.blit(play_text, play_text.get_rect(center=play_btn.center))


    elif current_state == STATE_PLAYING or current_state == STATE_PAUSED:
        # Render the active game environment
        screen.fill((20, 20, 20)) 
        level_map.draw(screen)
        
        # Draw all active entities
        for tower in tower_list:
            tower.draw(screen)
        for enemy in enemy_list:
            enemy.draw(screen)
        for proj in projectile_list:
            proj.draw(screen)

        # Render the transparent hover preview for tower placement
        if current_state == STATE_PLAYING:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_col = mouse_x // level_map.tile_size
            grid_row = mouse_y // level_map.tile_size
            grid_x = grid_col * level_map.tile_size
            grid_y = grid_row * level_map.tile_size
            
            highlight = pygame.Surface((level_map.tile_size, level_map.tile_size))
            highlight.set_alpha(128) 

            # Check if placement is valid and draw correct preview tower
            if level_map.is_buildable(mouse_x, mouse_y):
                if current_selection == 1: preview_tower = Tower(grid_col, grid_row)
                elif current_selection == 2: preview_tower = SniperTower(grid_col, grid_row)
                elif current_selection == 3: preview_tower = RapidTower(grid_col, grid_row)
                    
                preview_image = preview_tower.image.copy()
                preview_image.set_alpha(150)
                screen.blit(preview_image, preview_tower.rect)
                
                # Draw tower range indicator
                center_x = (grid_col * level_map.tile_size) + (level_map.tile_size // 2)
                center_y = (grid_row * level_map.tile_size) + (level_map.tile_size // 2)
                pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), preview_tower.range, 2)
            else:
                # Draw red highlight for invalid placement areas
                highlight.fill((255, 0, 0)) 
                screen.blit(highlight, (grid_x, grid_y))

        # Render top user interface bar
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, SCREEN_WIDTH, 40))
        pygame.draw.line(screen, (255, 255, 255), (0, 40), (SCREEN_WIDTH, 40), 2) 

        # Render player statistics
        lives_text = ui_font.render(f"Lives: {player_lives}", True, (255, 100, 100)) 
        money_text = ui_font.render(f"Gold: {player_money}", True, (255, 215, 0))       
        
        # Determine currently selected tower stats for display
        if current_selection == 1: tower_info = "Basic (100g) | DMG:1 | SPD:Med"
        elif current_selection == 2: tower_info = "Sniper (250g) | DMG:5 | SPD:Slow"
        elif current_selection == 3: tower_info = "Rapid (150g) | DMG:1 | SPD:Fast"
            
        selection_text = ui_font.render(f"Selected: {tower_info}", True, (255, 255, 255))

        # Render current wave status or game over conditions
        if wave_manager.game_over: wave_text = ui_font.render("GAME OVER", True, (255, 0, 0))
        elif wave_manager.game_won: wave_text = ui_font.render("YOU WIN", True, (0, 255, 0))
        else:
            status = f"Wave: {wave_manager.current_wave + 1}/{len(wave_manager.waves)}"
            if not wave_manager.wave_active:
                countdown = int(wave_manager.wave_delay - wave_manager.wave_timer)
                status += f" (Next in {countdown}s)"
            wave_text = ui_font.render(status, True, (200, 200, 255))

        # Blit UI elements to the screen
        screen.blit(lives_text, (10, 10))
        screen.blit(money_text, (160, 10))
        screen.blit(selection_text, (330, 10))
        
        wave_rect = wave_text.get_rect(topright=(SCREEN_WIDTH - 20, 10))
        screen.blit(wave_text, wave_rect)

        # Render warning popups
        if warning_timer > 0 and current_state == STATE_PLAYING:
            warning_surface = ui_font.render(warning_text, True, (255, 50, 50))
            warning_rect = warning_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            bg_rect = warning_rect.inflate(20, 10) 
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)
            pygame.draw.rect(screen, (255, 50, 50), bg_rect, 2) 
            screen.blit(warning_surface, warning_rect)
            
        # Render pause overlay
        if current_state == STATE_PAUSED:
            pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            pause_overlay.set_alpha(150) 
            pause_overlay.fill((0, 0, 0))
            screen.blit(pause_overlay, (0, 0))
            
            pause_text = ui_font.render("PAUSED - PRESS 'P' TO RESUME", True, (255, 255, 255))
            screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

    pygame.display.flip()
pygame.quit()
sys.exit()