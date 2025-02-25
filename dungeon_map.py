import pygame as pg
from levelmanager import Level
from os import path
import pickle
from ui import BlackScreen, display_text
from player import Player
pg.init()

info = pg.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 65

background = pg.image.load("assets/map/b3.png")
background = pg.transform.scale(background, (screen_width, screen_height))
stage_indicator_img = pg.transform.scale(pg.image.load('assets/others/Object/logo.png'),(50,60))
font_path = 'assets/Fonts/fontfile.ttf'
title_font = pg.font.Font(font_path, 72)
button_font = pg.font.Font(font_path, 36)
title_pos = 200
level_path = 'levels/saved_level_data/level_progress'
# Colors
BROWN = (181, 101, 29)
BLACK = (0,0,0)
class Dungeon:
    """Represents a single dungeon with levels and interaction."""
    def __init__(self, image_path, position, levels, name, number):
        self.image = self.load_image(image_path, (150, 150))
        self.rect = self.image.get_rect()
        self.position = position
        self.locked = True  # By default, dungeons are locked
        self.level_list = levels  # List of levels in this dungeon
        # self.level_state = Level()
        self.level_loaded = False
        self.name = name  # Dungeon name
        self.number = number # order/position
        self.completed = False        
        # Load font for the dungeon name
        self.font = pg.font.SysFont('Comic Sans MS', 20)

    def load_image(self, path, size):
        """Helper function to load and resize image."""
        img = pg.image.load(path)
        return pg.transform.scale(img, size)

    def apply_shadow(self):
        """Apply a shadow effect (dimmed) on the dungeon image."""
        shadow_surface = pg.Surface(self.image.get_size(), pg.SRCALPHA)  # Transparent surface
        shadow_surface.fill((0, 0, 0, 200))  # Semi-transparent black
        self.image.blit(shadow_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    
    
    def unlock(self):
        self.locked = False
        
    
               
    def draw(self, screen):
        if self.locked:
            self.apply_shadow()  # Apply shadow to locked dungeons
        
        # Draw the dungeon image on the screen.
        screen.blit(self.image, self.position)
        
        # Render the dungeon name text
        text = self.font.render(self.name, True, BLACK)        
        text_rect = text.get_rect(center=(self.position[0] + self.image.get_width() / 2, self.position[1] + self.image.get_height() + 10))
        screen.blit(text, text_rect)
    
    

    def is_clicked(self, mouse_pos):
        """Check if the dungeon image is clicked."""
        rect = pg.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
        return rect.collidepoint(mouse_pos)
    
       
    def state_handler(self,screen,keys):
        if not self.level_loaded:
            with open(level_path,'rb') as pickle_in:
                current_progress = pickle.load(pickle_in)
            if current_progress[0] > self.number:
                self.write = False
                self.level = self.level_list[-1]
            else:
                self.level = current_progress[1]
                self.write = True
            self.level_state = Level(screen, self.level)
            self.level_state.load_objects()
            self.level_loaded = True
        else:
            # if not self.level.complete:
            self.level_state.update(keys)
            self.level_state.draw()
            if self.level_state.complete:
                self.level_loaded = False
                next_level = self.level + 1
                next_dungeon = self.number + 1 if self.level == self.level_list[-1] else self.number
                self.completed = True if self.level == self.level_list[-1] else False
                if self.write:
                    if path.exists(level_path):
                        with open(level_path,'wb') as pickle_out:
                            current_progress = (next_dungeon, next_level) # (dungeon ,level)  
                            pickle.dump(current_progress, pickle_out)
        return self.completed
        
        


class Map:
    """Represents the entire map, including dungeons and the paths between them."""
    def __init__(self, screen):
        self.screen = screen        
        self.click_sound =  pg.mixer.Sound('assets/music/click.wav')
        self.dungeons = [
            Dungeon("assets/map/island.png", (screen_width * 0.08, screen_height * 0.13), [1, 2, 3], "Frozen Village",0),
            Dungeon("assets/map/ruin1.png", (screen_width * 0.404, screen_height * 0.105), [4], "Glacial Ruin",1),
            Dungeon("assets/map/cave.png", (screen_width * 0.15, screen_height * 0.73), [5], "Cavern of Frost",2),
            Dungeon("assets/map/ruin.png", (screen_width * 0.600, screen_height * 0.725), [6], "Frozen Spire",3),
            Dungeon("assets/map/heart.png", (screen_width * 0.90, screen_height * 0.35), [7], "Heart of Frost",4)
        ]
        if not path.exists(level_path):
            with open(level_path,'wb') as pickle_out:
                self.current_progress = (0,1) # (dungeon ,level)  
                pickle.dump(self.current_progress, pickle_out)
        else:
            with open(level_path,'rb') as pickle_in:
                self.current_progress = pickle.load(pickle_in)
            
        # Initially unlocked stages
        for i,dungeon in enumerate(self.dungeons):
            if i <= self.current_progress[0]:
                dungeon.unlock()
    def draw(self):
        """Draw the map, including all dungeons and paths."""
        self.screen.blit(background, (0, 0))
        self.draw_paths(self.screen)           
        self.draw_dungeons(self.screen)    
       
    def draw_paths(self, screen):
        """Draw the paths (dotted lines) between the stages."""
        level_paths = [
            ("Frozen Village", "Glacial Ruin"),
            ("Glacial Ruin", "Cavern of Frost"),
            ("Cavern of Frost", "Frozen Spire"),
            ("Frozen Spire", "Heart of Frost")
        ]
        level_positions = {
            "Frozen Village": (screen_width * 0.08, screen_height * 0.33),
            "Glacial Ruin": (screen_width * 0.375, screen_height * 0.165),
            "Cavern of Frost": (screen_width * 0.20, screen_height * 0.66),
            "Frozen Spire": (screen_width * 0.559, screen_height * 0.825),
            "Heart of Frost": (screen_width * 0.90, screen_height * 0.55)
        }

        def draw_dotted_line(surface, color, start_pos, end_pos, dash_length):
            x1, y1 = start_pos
            x2, y2 = end_pos
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if length == 0:
                return
            dx = (x2 - x1) / length * dash_length
            dy = (y2 - y1) / length * dash_length

            for i in range(0, int(length // dash_length), 2):
                start = (x1 + i * dx, y1 + i * dy)
                end = (x1 + (i + 1) * dx, y1 + (i + 1) * dy)
                pg.draw.line(surface, color, start, end, 2)

        for path in level_paths:
            start = level_positions[path[0]]
            end = level_positions[path[1]]
            draw_dotted_line(screen, BROWN, start, end, 10)

    def draw_dungeons(self, screen):
        """Draw all dungeons on the map."""
        for i,dungeon in enumerate(self.dungeons):
            dungeon.draw(screen)
            if i == self.current_progress[0]:
                screen.blit(stage_indicator_img, (dungeon.position[0] + 60 ,dungeon.position[1] - 50))
                
    
    
    def handle_click(self, mouse_pos, event):
        """Handle mouse click event on dungeons."""
        for i, dungeon in enumerate(self.dungeons):
            if dungeon.is_clicked(mouse_pos) and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.click_sound.play()
                if dungeon.locked:
                    print(f"Stage {i+1} {dungeon.name} is locked.")
                    display_text(self.screen,title_font, 'Locked',(500,400))
                    return None
                else:
                    print(f"Stage {i+1} {dungeon.name} clicked. Levels: {', '.join(map(str, dungeon.level_list))}")
                    return dungeon 


