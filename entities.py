# entities.py
import pygame
import math
from settings import *

class Enemy:
    def __init__(self, path):
        # Attributes from Design 
        self.hp = 5
        self.max_hp = self.hp 
        self.speed = 200.0  # Float for precision
        self.reward = 5
        self.path_index = 0
        self.path = path # Store path logic
        
        # Visuals (Loading the PNG)
        raw_image = pygame.image.load("assets/enemy.png").convert_alpha()
        
        # Scale it to fit the track (40x40 pixels)
        self.image = pygame.transform.scale(raw_image, (60, 60))
        
        # Start at the first point of the path
        start_pos = self.path[0]
        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        """ Moves the enemy. Matches 'move_along_path' logic. """
        self.move_along_path(dt)

    def draw(self, screen):
        # 1. Draw the actual plane 
        screen.blit(self.image, self.rect)
        
        # 2. Draw the Health Bar
        if self.hp > 0:
            health_percentage = self.hp / self.max_hp
            bar_width = 40
            bar_height = 6
            
            # ut the bar slightly above the enemy's head
            bar_x = self.rect.centerx - (bar_width / 2)
            bar_y = self.rect.top - 10 
            
            # Draw Red Background (Missing Health)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # Draw Green (Current Health)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percentage, bar_height))

    def move_along_path(self, dt):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            target_x, target_y = target
            
            # Calculate distance to target
            dir_x = target_x - self.x
            dir_y = target_y - self.y
            distance = math.hypot(dir_x, dir_y)
            
            if distance > 0:
                # Divide vector by distance) and multiply by constant speed
                move_x = (dir_x / distance) * self.speed * dt
                move_y = (dir_y / distance) * self.speed * dt
                
                # Doesn't overshooting the target
                if abs(move_x) > abs(dir_x): move_x = dir_x
                if abs(move_y) > abs(dir_y): move_y = dir_y
                
                self.x += move_x
                self.y += move_y
                
                self.rect.centerx = int(self.x)
                self.rect.centery = int(self.y)
                
            # Check if close to target node (snap to it)
            if distance < 5:
                self.path_index += 1

class Tower:
    def __init__(self, grid_x, grid_y):
        # --- NEW CYCLE 5 ADDITIONS ---
        self.grid_x = grid_x
        self.grid_y = grid_y
        # -----------------------------
        
        # Calculate the exact pixel center of the 64x64 tile
        self.pixel_x = (grid_x * 64) + 32
        self.pixel_y = (grid_y * 64) + 32
        
        
        # Base stats (from Design)
        self.range = 150
        self.damage = 1
        self.fire_rate = 1.0
        self.cooldown = 0
        self.cost = 100 # <--- CYCLE 6: TOWER COST
        
        # Visuals (Loading the PNG)
        raw_image = pygame.image.load("assets/tower.png").convert_alpha()
        
        # Scale it to fit nicely inside the 64x64 grid tile
        self.image = pygame.transform.scale(raw_image, (64, 64))
        self.rect = self.image.get_rect(center=(self.pixel_x, self.pixel_y))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, dt, enemy_list, projectile_list):
        # Decrease the cooldown timer
        if self.cooldown > 0:
            self.cooldown -= dt

        # Once tower is ready to shoot, fire the turret
        if self.cooldown <= 0:
            for enemy in enemy_list:
                # Calculate distance to enemy
                dist = math.hypot(enemy.rect.centerx - self.pixel_x, enemy.rect.centery - self.pixel_y)
                
                # If the enemy is inside the range circle AND is still alive
                if dist <= self.range and enemy.hp > 0:
                    # Fires, creates a projectile and reset cooldown
                    new_bullet = Projectile(self.pixel_x, self.pixel_y, enemy, self.damage)
                    projectile_list.append(new_bullet)
                    
                    self.cooldown = 1.0 / self.fire_rate
                    break # Only shoot one enemy at a time

# --- CYCLE 8: INHERITANCE & POLYMORPHISM ---

class SniperTower(Tower): # (Tower) means it inherits from the Tower class
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y) # Run the Parent's setup
        
        # Override the base stats (Polymorphism)
        self.range = 300      # Massive range
        self.damage = 5       # Massive damage
        self.fire_rate = 0.5  # Very slow (1 shot every 2 seconds)
        self.cost = 250       # Expensive
        
        # Visuals
        self.image.fill((255, 255, 0)) # Yellow square for Sniper

class RapidTower(Tower):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y) 
        
        # Override the base stats
        self.range = 100      # Short range
        self.damage = 1       # Low damage
        self.fire_rate = 5.0  # Very fast (5 shots per second!)
        self.cost = 150       # Medium price
        
        # Visuals
        self.image.fill((128, 0, 128)) # Purple square for Rapid Fire


class Projectile:
    def __init__(self, start_x, start_y, target, damage):
        self.x = float(start_x)
        self.y = float(start_y)
        self.target = target
        self.speed = 400.0 # Pixels per second
        self.damage = damage
        self.active = True

        # --- CYCLE 8: LOAD THE BULLET PNG ---
        raw_image = pygame.image.load("assets/bullet.png").convert_alpha()
        
        # Uncomment the line below if your bullet still has a white background!
        # raw_image.set_colorkey((255, 255, 255))
        
        # Scale the bullet (adjust these numbers if it's too big or small)
        self.original_image = pygame.transform.scale(raw_image, (40, 16)) 
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        if not self.active or self.target.hp <= 0:
            self.active = False
            return

        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.hypot(dx, dy)

        if distance < 10:
            self.target.hp -= self.damage
            self.active = False
            print(f"Hit! Enemy HP: {self.target.hp}")
            return

        # Move the bullet
        angle = math.atan2(dy, dx)
        self.x += math.cos(angle) * self.speed * dt
        self.y += math.sin(angle) * self.speed * dt
        
        # --- CYCLE 8: ROTATE THE BULLET ---
        # Pygame rotates counter-clockwise, so this code uses negative degrees
        angle_degrees = math.degrees(-angle)
        self.image = pygame.transform.rotate(self.original_image, angle_degrees)
        
        # Update the rect position so it draws in the right spot
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def draw(self, screen):
        if self.active:
            # Draw the PNG instead of the yellow circle
            screen.blit(self.image, self.rect)
