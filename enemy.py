import pygame as pg

class Thorn():
    def __init__(self, pos_x, pos_y):
        self.image = pg.transform.scale(pg.image.load('assets/characters/thorn.png'),(40,40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.max_y = pos_y
        self.vel_y = 0
        
    def update(self, player):
        if self.rect.colliderect(player.hitbox):
            player.image.set_alpha(100)
            player.decrease_health(5)
            player.hurt_sound.play()
            player.jump()
        else:
            player.image.set_alpha(255)
    

    # Equality comparison (==)
    def __eq__(self, other):
        if isinstance(other, Thorn):
            return self.rect.topleft == other.rect.topleft
        return False
            
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # pg.draw.rect(screen, (255,0,0), self.rect, 2)


class Zombie():
    asset_path = 'assets/characters/zombie/png/male/'

    def __init__(self, pos_x, pos_y, horz_boundary):
        self.horiz_boundary = horz_boundary
        self.idle = []
        self.walk = []
        self.attack = []
        self.dead = []
        for i in range(15):
            if i < 15:  
                self.idle.append(pg.transform.scale(pg.image.load(f'{Zombie.asset_path}Idle ({i+1}).png'), (100, 120)))
            if i < 10:  
                self.walk.append(pg.transform.scale(pg.image.load(f'{Zombie.asset_path}Walk ({i+1}).png'), (100, 120)))
            if i < 8:  
                self.attack.append(pg.transform.scale(pg.image.load(f'{Zombie.asset_path}Attack ({i+1}).png'), (100, 120)))
            if i < 12:  
                self.dead.append(pg.transform.scale(pg.image.load(f'{Zombie.asset_path}Dead ({i+1}).png'), (100, 120)))
        self.image = self.walk[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.walk_count = 0
        self.direction = 1 # 1 for right, -1 for left
        self.animation_speed = 4
        self.animation_counter = 0
        self.health = 100
        self.is_alive = True
        self.is_attacking = False
        self.has_attacked = False  #flag for tracking if zombie has attacked in each cycle        
        self.attacking_speed = 6
        self.dead_animation_played = False
        self.sound = pg.mixer.Sound('assets/music/zombie_bite.wav')
      
    def update(self, player):    
        if not self.is_alive:
            self.image.set_alpha(128)
            if not self.dead_animation_played:
                self.animate(self.dead)
                if self.walk_count == len(self.dead) - 1:
                    self.dead_animation_played = True
            return
         
          
        if self.rect.x < player.hitbox.x:
            self.rect.x += 2
            if self.direction == -1:
                self.rect.x += 3
                self.flip_images()
                self.direction = 1
        elif self.rect.x > player.hitbox.x:
            self.rect.x -= 2
            if self.direction == 1:
                self.rect.x -= 3
                self.flip_images()
                self.direction = -1
            

        # Check if the zombie is near the player and attack
        if abs(self.rect.x - player.hitbox.x) < 60:
            if player.is_alive and self.is_alive:
                if player.is_attacking:
                    player.perform_attack(self)
                self.perform_attack(player)
        else:
            self.is_attacking = False
            self.animate(self.walk)
        if(self.rect.x < self.horiz_boundary[0]):
            self.rect.x = self.horiz_boundary[0]
        if(self.rect.x > self.horiz_boundary[1]):
            self.rect.x = self.horiz_boundary[1]
            
    
    def decrease_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
               
    def perform_attack(self, player):
        if self.rect.colliderect(player.hitbox):
            self.is_attacking = True
            self.animate(self.attack)
            if not self.has_attacked:
                self.sound.play()
                player.decrease_health(10)
                player.hurt_sound.play()
                self.has_attacked = True
        else:
            self.is_attacking = False
            self.has_attacked = False
            self.animate(self.idle)
    
    def animate(self, animation):
        current_speed = self.attacking_speed if animation is self.attack else self.animation_speed
        self.animation_counter += 1
        if self.animation_counter >= current_speed:
            self.walk_count = (self.walk_count + 1) % len(animation)
            self.image = animation[self.walk_count]
            self.animation_counter = 0
            if self.walk_count == len(animation)//2 and self.is_attacking:
                self.has_attacked = False  # Reset attack flag at the end of the attack animation

    def flip_images(self):
        for i in range(len(self.idle)):
            self.idle[i] = pg.transform.flip(self.idle[i], True, False)
        for i in range(len(self.walk)):
            self.walk[i] = pg.transform.flip(self.walk[i], True, False)
        for i in range(len(self.attack)):
            self.attack[i] = pg.transform.flip(self.attack[i], True, False)
        for i in range(len(self.dead)):
            self.dead[i] = pg.transform.flip(self.dead[i], True, False)

    def draw(self, screen):
        pg.draw.rect(screen, (200,0,0), (self.rect.x + 20, self.rect.y, self.health/100 * 50, 5))
        screen.blit(self.image, self.rect.topleft)
        # pg.draw.rect(screen, (255,0,0), self.rect, 2)
        
        

    

        
# just copied and pasted from other entity
# class Dragon:
#     red, green = 0, 200
#     asset_path = 'assets/characters/Dragon/png/'

#     def __init__(self, pos_x, pos_y):
#         self.idle = []
        
#         for i in range(5):
#             self.idle.append(pg.transform.scale(pg.image.load(f'{Dragon.asset_path}Fly ({i+1}).png'), (160,250)))
#         for i in range(5):
#             self.idle[i] = pg.transform.flip(self.idle[i],True, False)
#         self.image = self.idle[0]
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (pos_x, pos_y)
#         self.width = self.image.get_width()
#         self.height = self.image.get_height()
#         self.hitbox = pg.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 23, self.rect.height - 18)
        
#         self.vel_y = 0
#         self.jumped = False
#         self.jump_strength = -15
        
#         self.direction = 1  # 1 for right, -1 for left
#         self.walk_count = 0
#         self.animation_speed = 5
#         self.animation_counter = 0
        
#         self.health = 100
#         self.is_alive = True
#         self.is_attacking = False
#         self.has_attacked = True
#         self.attacking_speed = 1
#         self.in_water = False
#         self.water_entry_time = None
#         self.dead_animation_played = False

#     def update(self,keys, screen_width, tiles):
#         if not self.is_alive:
#             if not self.dead_animation_played:
#                 self.animate(self.dead)
#                 if self.walk_count == len(self.dead) - 1:
#                     self.dead_animation_played = True
#             return
#         Dragon.red = 180 if self.health<40 else 0
#         Dragon.green = 0 if self.health<40 else 200
#         dx = 0
#         dy = 0
#         self.hitbox = pg.Rect(self.rect.x + 15, self.rect.y + 10, self.rect.width - 35, self.rect.height - 18)
#         #Horizoontal Movement and attack controls
#         # if keys[pg.K_RIGHT]:
#         #     pass
#         # elif keys[pg.K_RIGHT]:
#         #     pass
#         # else:
#         self.animate(self.idle)

#         # Vertical movement
        
        
        
#         #Adding gravity
#         self.vel_y += 1
#         if self.vel_y > 10:
#             self.vel_y = 10
#         dy += self.vel_y

#         # Collision detection
#         for tile in tiles[0]:
#             # Check for collision in the x direction
#             if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height):
#                 if dx > 0:  # Moving right
#                     dx = tile[1].left - self.hitbox.right
#                 elif dx < 0:  # Moving left
#                     dx = tile[1].right - self.hitbox.left
#                 # Check for collision in the y direction
#             if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox.width, self.hitbox.height):
#                 if self.vel_y < 0:  # Moving up
#                     dy = tile[1].bottom - self.hitbox.top
#                     self.vel_y = 0
#                 elif self.vel_y >= 0:  # Moving down
#                     dy = tile[1].top - self.hitbox.bottom
#                     self.vel_y = 0
#                     self.jumped = False
        
#         self.in_water = False 
#         for water in tiles[1]:
#             if water[1].colliderect(self.hitbox):
#                 self.in_water = True
#                 dy = 1
#                 self.vel_y = 0
#                 if self.water_entry_time is None:
#                     self.water_entry_time = pg.time.get_ticks()
#                 break
#         else:
#             self.in_water = False
#             self.water_entry_time = None
#         # Check if the player has been in water for more than 3 seconds
#         if self.in_water and self.water_entry_time is not None:
#             self.decrease_health(1)
#             # current_time = pg.time.get_ticks()
#             # if current_time - self.water_entry_time > 3000:
#             #    pass
#             # else:
#             #     self.decrease_health(1)
            
       
#         # Update player position
#         self.rect.x += dx
#         self.rect.y += dy

#         # Right Border check
#         if self.rect.x >= screen_width - 50:
#             self.rect.x = screen_width - 50
#         # Left Border check
#         if self.rect.x <= 0:
#             self.rect.x = 0

#     def jump(self):
#         self.jumped = True
#         self.vel_y = self.jump_strength
    
#     def decrease_health(self, amount):
#         self.health -= amount
#         if self.health <= 0:
#             self.health = 0
#             self.is_alive = False

#     def perform_attack(self, enemy):
#         if self.rect.colliderect(enemy.rect):
#             if not self.has_attacked:
#                 enemy.decrease_health(30)
#                 self.has_attacked = True

#     def animate(self, animation):
#         current_speed = self.animation_speed
#         self.animation_counter += 1
#         if self.animation_counter >= current_speed:
#             self.walk_count = (self.walk_count + 1) % len(animation)
#             self.image = animation[self.walk_count]
#             self.animation_counter = 0
#             if self.walk_count == 0 and self.is_attacking:
#                 self.has_attacked = False  # Reset attack flag at the end of the attack animation
#                 self.is_attacking = False
#         if self.in_water:
#             self.image.set_alpha(120)
#         else:
#             self.image.set_alpha(255)
    
    

#     def flip_images(self):
#         for i in range(len(self.idle)):
#             self.idle[i] = pg.transform.flip(self.idle[i], True, False)
#             self.run[i] = pg.transform.flip(self.run[i], True, False)
#             self.attack[i] = pg.transform.flip(self.attack[i], True, False)
#             self.dead[i] = pg.transform.flip(self.dead[i], True, False)
            
#     def draw(self, screen):
#         screen.blit(self.image, self.rect)
#         # pg.draw.rect(screen, (255,255,255), self.rect, 2)
#         # pg.draw.rect(screen, (255,0,0), self.hitbox, 2)
#         pg.draw.rect(screen, (Dragon.red, Dragon.green, 0), (20,20,self.health * 1.5 ,15))
