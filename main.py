import pygame as pg
from pygame import mixer
from world import Snowflake
from statesmanager import StateManager

pg.init()

# mixer.music.load("assets/music/background.mp3")
# mixer.music.play(-1)

clock = pg.time.Clock()
FPS = 60

info = pg.display.Info()
screen_width = info.current_w 
screen_height = info.current_h - 65
# screen_width = 1493
# screen_height = 880
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Frost Legacy')
time_passed = pg.time.get_ticks()
main_screen = pg.image.load('assets/others/BG/Mainscreen.jpeg')
main_screen = pg.transform.scale(main_screen, (screen.get_width(), screen.get_height()))


num_snowflakes = 200
snowflakes = [Snowflake(screen_width, screen_height) for _ in range(num_snowflakes)]

game_state = "main_menu"  # Track the state of the game (main menu, game started, settings, etc.)
previous_state = None  # Track previous state for back button functionality
state = StateManager(screen , game_state)

quit = False
while not quit:
    mouse_pos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()
    
    screen.blit(main_screen, (0, 0))
    state.handle_state(mouse_pos, keys)
    

    # Handle mouse click events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True
            
        if state.handle_mouse_click(mouse_pos, event): #returns true if exit button is clicked
            quit = True
        

    # Snowflakes
    for snowflake in snowflakes:
        snowflake.update()
        snowflake.draw(screen)
    
    clock.tick(FPS)
    pg.display.update()

pg.mixer.music.stop()
pg.quit()
