import pygame as pg
import random
tile_size = 40
assets = 'assets/others'	#assets path

class World():
    def __init__(self, data):
        self.world_data = data
        self.no_of_object = 5
        self.no_of_tile = 13
        self.total_tile = self.no_of_tile + self.no_of_object
        self.tile_img = []
        self.tile_list = []
        object_img = []
        self.obj_list = []
        self.water_list = []
        #loading tile images
        for i in range(self.no_of_tile): 
            if i!=12: #other than rock
                img = pg.image.load(f'{assets}/Tiles/{i+1}.png')
                img = pg.transform.scale(img, (tile_size, tile_size))
                self.tile_img.append(img)
            else: #for rock
                img = pg.image.load(f'{assets}/Tiles/{i+1}.png')
                img = pg.transform.scale(img, (40,40))
                self.tile_img.append(img)

        
        for i in range(self.no_of_tile, self.total_tile):  # objects
            img = pg.image.load(f'{assets}/Object/{i+1}.png')
            if i!=14:
                img = pg.transform.scale(img, (tile_size, tile_size)) #if i!=14 else pg.transform.scale(img, (160,200))
            object_img.append(img)
    
        # Create tile list with rectangles for collision detection
        for r, row in enumerate(data):
            for c, item in enumerate(row):
                if item > 0 and (item!= 10 and item!= 11): # 10 and 11 are for water
                    if item <= self.no_of_tile: # 1 to 13
                        img = self.tile_img[item-1]
                        img_rect = img.get_rect()
                        img_rect.x = c * tile_size
                        img_rect.y = r * tile_size 
                        self.tile_list.append((img, img_rect))
                    elif item > self.no_of_tile and item <= self.total_tile: # 14 to 18
                        img = object_img[item-self.no_of_tile-1]
                        img_rect = img.get_rect()
                        img_rect.x = c * tile_size
                        img_rect.y = r * tile_size
                        if item == 14:  # Ice crystal
                            self.obj_list.append((img, img_rect))
                        elif item == 15:  # Tree
                            img = pg.transform.scale(img, (160, 200))
                            img_rect = img.get_rect()
                            img_rect.x = c * tile_size
                            img_rect.y = r * tile_size
                            self.obj_list.append((img, img_rect))
                        elif item == 16:  # Sign board
                            self.obj_list.append((img, img_rect))
                        elif item == 17:  # Igloo house
                            self.obj_list.append((img, img_rect))
                        elif item == 18:  # Snowman
                            img = pg.transform.scale(img, (100, 109))
                            img_rect = img.get_rect()
                            img_rect.x = item * tile_size
                            img_rect.y = r * tile_size + 12
                            self.obj_list.append((img, img_rect))
                
                elif item == 10 or item == 11:
                    img = self.tile_img[item-1]
                    img_rect = img.get_rect()
                    img_rect.x = c * tile_size
                    img_rect.y = r * tile_size
                    self.water_list.append((img, img_rect))
                    
    
    def draw_world(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pg.draw.rect(screen, (255,255,255), tile[1], 1)
        for water in self.water_list:
            screen.blit(water[0], water[1])
            # pg.draw.rect(screen, (255,255,255), water[1], 1)
        for obj in self.obj_list:
            screen.blit(obj[0], obj[1])
            # pg.draw.rect(screen, (255,255,255), obj[1], 1)

    def get_tiles(self):
        return (self.tile_list, self.water_list)
    



class Snowflake:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0 , screen_height)
        self.size = random.randint(2, 4)
        self.speed = random.uniform(1, 4)
        self.drift = random.uniform(-1, 1)
        self.opacity = random.randint(190,200)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.y += self.speed
        self.x += self.drift
        if self.y > self.screen_height:
            self.y = random.randint(-self.screen_height//2, 0)
            self.x = random.randint(0, self.screen_width)
            self.speed = random.uniform(1, 3)
            self.drift = random.uniform(-1, 1)
            self.opacity = random.randint(190, 200)
        if self.x > self.screen_width or self.x < 0:
            self.x = random.randint(0, self.screen_width)

    def draw(self, screen):
        snowflake_surface = pg.Surface((self.size * 2, self.size * 2), pg.SRCALPHA)
        pg.draw.circle(snowflake_surface, (255, 255, 255, self.opacity), (self.size, self.size), self.size)
        screen.blit(snowflake_surface, (self.x, self.y))