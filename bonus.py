import pygame as pg

class Apple:
    def __init__(self, pos_x, pos_y):
        self.image = pg.image.load('assets/others/bonus/apple.png')
        self.original_image = pg.transform.scale(self.image, (20,20))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.scale_factor = 0
        self.scale_direction = 0.3  # positive for increasing, - for decreasing
        self.used = False
        self.sound = pg.mixer.Sound('assets/music/bonus.wav')
    def animate(self):
        if abs(self.scale_factor) >= 3:
            self.scale_direction *= -1  # Reverse direction
        self.scale_factor += self.scale_direction
        new_size = 20 + self.scale_factor
        self.image = pg.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self, player):
        if self.rect.colliderect(player.hitbox):
            # if player.health <= 95:
                self.used = True
                self.sound.play()
                player.health = min(100, player.health + 5)
           
    def draw(self, screen):
        if not self.used:
            self.animate()
            screen.blit(self.image, self.rect.topleft)


class HealingPotion:
    def __init__(self, pos_x, pos_y):
        self.image = pg.image.load('assets/others/bonus/potion.png')
        self.original_image = pg.transform.scale(self.image, (40, 40))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.scale_factor = 0
        self.scale_direction = 0.3  # positive for increasing, - for decreasing
        self.used = False
        self.sound = pg.mixer.Sound('assets/music/bonus.wav')
    def animate(self):
        if abs(self.scale_factor) >= 6:
            self.scale_direction *= -1  # Reverse direction
        self.scale_factor += self.scale_direction
        new_size = 40 + self.scale_factor
        self.image = pg.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)

    
    def update(self, player):
        if self.rect.colliderect(player.hitbox):
            # if player.health <= 85:
                self.used = True
                self.sound.play()
                player.health = min(100, player.health + 15)
            
    def draw(self, screen):
        if not self.used:
            self.animate()
            screen.blit(self.image, self.rect.topleft)