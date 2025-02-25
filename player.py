import pygame as pg

class Player:
    red, green = 0, 200
    asset_path = 'assets/characters/knight/png/'

    def __init__(self, pos_x, pos_y):
        self.idle = []
        self.run = []
        self.attack = []
        self.dead = []
        for i in range(10):
            self.idle.append(pg.transform.scale(pg.image.load(f'{Player.asset_path}Idle ({i+1}).png'), (100, 120)))
            self.run.append(pg.transform.scale(pg.image.load(f'{Player.asset_path}Run ({i+1}).png'), (100, 120)))
            self.attack.append(pg.transform.scale(pg.image.load(f'{Player.asset_path}Attack ({i+1}).png'), (100, 120)))
            self.dead.append(pg.transform.scale(pg.image.load(f'{Player.asset_path}Dead ({i+1}).png'), (100, 120)))

        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.respawn_position = (pos_x, pos_y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 23, self.rect.height - 18)
        
        self.vel_y = 0
        self.jumped = False
        self.jump_strength = -15
        
        self.direction = 1  # 1 for right, -1 for left
        self.walk_count = 0
        self.animation_speed = 3
        self.animation_counter = 0
        
        self.health = 100
        self.is_alive = True
        self.lives = 3
        self.is_attacking = False
        self.has_attacked = True
        self.attacking_speed = 1
        self.in_water = False
        self.water_entry_time = None
        self.dead_animation_played = False
        
        self.jump_sound = pg.mixer.Sound('assets/music/jump_sound.wav')
        self.sword_sound = pg.mixer.Sound('assets/music/sword_slash.wav')
        self.in_water_sound = pg.mixer.Sound('assets/music/water_bubbles.wav')
        self.game_over_sound = pg.mixer.Sound('assets/music/game_over_2.wav')
        self.hurt_sound = pg.mixer.Sound('assets/music/hurt.wav')
        self.water_sound_loaded = False
        
    def __del__(self):
        print(f'Player deleted')
        
    def update(self, keys, screen_width, tiles):
        if not self.is_alive:
            if not self.dead_animation_played:
                self.animate(self.dead)
                if self.walk_count == len(self.dead) - 1:
                    self.dead_animation_played = True
            # pg.mixer.music.play(-1)
            return
        #     if self.lives ==0:
        #         return 0
        #     else:
        #         self.respawn()
        # else: pass
                
        Player.red = 180 if self.health<40 else 0
        Player.green = 0 if self.health<40 else 200
        dx = 0
        dy = 0
        self.hitbox = pg.Rect(self.rect.x + 15, self.rect.y + 10, self.rect.width - 35, self.rect.height - 18)
        #Horizoontal Movement and attack controls
        if keys[pg.K_RIGHT]:
            dx = 5 if not self.in_water else 2
            if self.direction == -1:
                self.flip_images()
                self.direction = 1
            self.animate(self.run)
        elif keys[pg.K_LEFT]:
            dx = -5 if not self.in_water else -2
            if self.direction == 1:
                self.flip_images()
                self.direction = -1
            self.animate(self.run)
        elif keys[pg.K_SPACE]:
            self.is_attacking = True
            self.animate(self.attack)
        else:
            self.animate(self.idle)

        # Vertical movement
        if keys[pg.K_UP] and not self.jumped:
            self.jump()
            self.jump_sound.play()
        
        
        #Adding gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Collision detection
        for tile in tiles[0]:
            # Check for collision in the x direction
            if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                if dx > 0:  # Moving right
                    dx = tile[1].left - self.hitbox.right
                elif dx < 0:  # Moving left
                    dx = tile[1].right - self.hitbox.left
                # Check for collision in the y direction
            if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox.width, self.hitbox.height):
                if self.vel_y < 0:  # Moving up
                    dy = tile[1].bottom - self.hitbox.top
                    self.vel_y = 0
                elif self.vel_y >= 0:  # Moving down
                    dy = tile[1].top - self.hitbox.bottom
                    self.vel_y = 0
                    self.jumped = False
        
        self.in_water = False 
        for water in tiles[1]:
            if water[1].colliderect(self.hitbox):
                self.in_water = True
                dy = 1
                self.vel_y = 0
                if self.water_entry_time is None:
                    self.water_entry_time = pg.time.get_ticks()
                break
        else:
            self.in_water = False
            self.water_entry_time = None
        if self.in_water and self.water_entry_time is not None:
            self.decrease_health(1)
            if not self.water_sound_loaded:
                pg.mixer.music.pause()
                self.water_sound_loaded = True
                self.in_water_sound.play()
            

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Right Border check
        if self.rect.x >= screen_width - 50:
            self.rect.x = screen_width - 50
        # Left Border check
        if self.rect.x <= 0:
            self.rect.x = 0

    def jump(self):
        self.jumped = True
        self.vel_y = self.jump_strength
    
    def decrease_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            # self.lives -= 1 
    def respawn(self):
        self.is_alive = True
        self.health = 100  # Reset health
        self.rect.topleft = self.respawn_position  # Respawn at starting position
        self.dead_animation_played = False  # Reset dead animation
        
    def perform_attack(self, enemy=None):
        if enemy != None and self.rect.colliderect(enemy.rect):
            if not self.has_attacked:
                enemy.decrease_health(30)
                self.has_attacked = True

    def animate(self, animation):
        current_speed = self.attacking_speed if animation is self.attack else self.animation_speed
        self.animation_counter += 1
        if self.animation_counter >= current_speed:
            self.walk_count = (self.walk_count + 1) % len(animation)
            self.image = animation[self.walk_count]
            self.animation_counter = 0
            if self.walk_count == 0 and self.is_attacking:
                self.sword_sound.play()
                self.has_attacked = False  # Reset attack flag at the end of the attack animation
                self.is_attacking = False
        if self.in_water:
            self.image.set_alpha(120)
        else:
            self.image.set_alpha(255)
    
    

    def flip_images(self):
        for i in range(len(self.idle)):
            self.idle[i] = pg.transform.flip(self.idle[i], True, False)
            self.run[i] = pg.transform.flip(self.run[i], True, False)
            self.attack[i] = pg.transform.flip(self.attack[i], True, False)
            self.dead[i] = pg.transform.flip(self.dead[i], True, False)
           
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pg.draw.rect(screen, (255,255,255), self.rect, 2)
        # pg.draw.rect(screen, (255,0,0), self.hitbox, 2)
        pg.draw.rect(screen, (Player.red, Player.green, 0), (20,20,self.health * 1.5 ,15))
