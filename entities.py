# entities.py
import pygame
import math
from settings import *

class Enemy:
    def __init__(self, path):
        # Attributes from Design 
        self.hp = 5
        self.speed = 200.0  # Float for precision
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
        
        
        # Base stats (from Design)
        self.range = 150
        self.damage = 1
        self.fire_rate = 1.0
        self.cooldown = 0
        self.cost = 100 # <--- CYCLE 6: TOWER COST
        
        # Visuals (blue square for now)
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE) 
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
class Projectile:
    def __init__(self, start_x, start_y, target, damage):
        self.x = float(start_x)
        self.y = float(start_y)
        self.target = target
        self.speed = 500.0 # Pixels per second
        self.damage = damage
        self.active = True # Used to delete the bullet when it hits

    def update(self, dt):
        # If the target is dead or bullet already hit, stop.
        if not self.active or self.target.hp <= 0:
            self.active = False
            return

        # Calculate angle to the target using Trigonometry
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.hypot(dx, dy)

        # Hit detection! If we are super close, deal damage and disappear
        if distance < 10:
            self.target.hp -= self.damage
            self.active = False
            print(f"Hit! Enemy HP: {self.target.hp}")
            return

        # Move the bullet towards the target
        angle = math.atan2(dy, dx)
        self.x += math.cos(angle) * self.speed * dt
        self.y += math.sin(angle) * self.speed * dt

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5) # Yellow bullet