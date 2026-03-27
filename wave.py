from entities import Enemy, FastEnemy, BossEnemy

class WaveManager:
    def __init__(self, level_map):
        self.level_map = level_map
        # Define how many enemies spawn in each wave
        self.waves = [5, 10, 15, 25] 
        self.current_wave = 0
        self.enemies_to_spawn = self.waves[self.current_wave]
        
        self.spawn_timer = 0.0
        self.spawn_interval = 1.0 # 1 second between enemy spawns
        
        self.wave_timer = 0.0
        self.wave_delay = 5.0 # 5 second interval between waves
        
        self.wave_active = True
        self.game_over = False
        self.game_won = False

    def update(self, dt, enemy_list):
        # Stop spawning if the game is over
        if self.game_over or self.game_won:
            return

        # If the wave is running and there are still enemies to spawn
        if self.wave_active:
            if self.enemies_to_spawn > 0:
                self.spawn_timer += dt
                if self.spawn_timer >= self.spawn_interval:
                    # --- CYCLE 13: SPAWN ADVANCED ENEMIES ---
                    wave_num = self.current_wave + 1 
                    
                    if wave_num % 4 == 0:
                        # BOSS WAVE: Spawn normal enemies, but the VERY LAST enemy is the Boss
                        if self.enemies_to_spawn == 1:
                            new_enemy = BossEnemy(self.level_map.waypoints)
                        else:
                            new_enemy = Enemy(self.level_map.waypoints)
                            
                    elif wave_num == 3:
                        # WAVE 3: Mixed wave. Alternate between Fast and Normal
                        if self.enemies_to_spawn % 2 == 0:
                            new_enemy = FastEnemy(self.level_map.waypoints)
                        else:
                            new_enemy = Enemy(self.level_map.waypoints)
                            
                    elif wave_num % 2 == 0:
                        # WAVE 2: All Fast enemies
                        new_enemy = FastEnemy(self.level_map.waypoints)
                        
                    else:
                        # WAVE 1: Standard enemies
                        new_enemy = Enemy(self.level_map.waypoints)
                    
                    # Make enemies tougher each wave! (+5 Max HP per wave)
                    new_enemy.max_hp += (self.current_wave * 5)
                    new_enemy.hp = new_enemy.max_hp
                    
                    enemy_list.append(new_enemy)

                    
                    # Reset spawn timer
                    self.enemies_to_spawn -= 1
                    self.spawn_timer = 0.0
                    
            # Check if wave is finished (All spawned AND all dead/reached end)
            elif len(enemy_list) == 0:
                self.wave_active = False
                self.wave_timer = 0.0
                self.current_wave += 1
                
                # Check for win condition
                if self.current_wave >= len(self.waves):
                    self.game_won = True
                    
        # If wave is NOT active, run the countdown timer for the next wave
        else:
            self.wave_timer += dt
            if self.wave_timer >= self.wave_delay:
                self.wave_active = True
                self.enemies_to_spawn = self.waves[self.current_wave]

