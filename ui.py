import pygame as pg
pg.init()
assets = 'assets/others'

   
def display_text(screen,font, text, position, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class BlackScreen:
    def __init__(self, screen):
        self.surface = screen
        self.image = pg.image.load(f'{assets}/BG/blackscreen.jpg')
        self.image = pg.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.animation_played = False

    def fade(self, start_time, direction=1):
        elapsed_time = pg.time.get_ticks() - start_time
        if elapsed_time < 4000:
            self.animation_played = False
            if direction == 1:
                alpha_value = 255 - (elapsed_time // 16)
            else:
                alpha_value = elapsed_time // 16
                print(start_time, elapsed_time)
            self.image.set_alpha(alpha_value)
        else:
            if direction == 1:
                self.image.set_alpha(0) 
            else:
                self.image.set_alpha(255)
                print(4)
            self.animation_played = True
        self.surface.blit(self.image, (0, 0))

        
 

class Button:
    def __init__(self, text, font, position, width, height, action=None,color=(0, 0, 0),hover=(26, 173, 223)): #(0, 150, 255)
        self.text = text
        self.font = font
        self.position = position
        self.width = width
        self.height = height
        self.default_color = color
        self.hover_color = hover
        self.action = action
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.clicked = False  # Track click status
        self.click_sound =  pg.mixer.Sound('assets/music/click.wav')

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.default_color

        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not self.clicked:  # Only trigger once per click
                self.clicked = True
                if self.action:
                    self.click_sound.set_volume(0.5)
                    self.click_sound.play()
                    self.action()  # Trigger the action (function passed in constructor)

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False

