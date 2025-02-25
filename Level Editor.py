# This file is for building levels of tha game but not the game itself

import pygame as pg
import pickle
from os import path

# Initialize Pygame
pg.init()

info = pg.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 65

# # Screen dimensions
# screen_width = 1493
# screen_height = 880
tile_size = 40

# Create screen
screen = pg.display.set_mode((screen_width, screen_height))

# Load background image
assets = 'assets/others'  # Update this path to your assets folder
bg_image = pg.image.load(f'{assets}/BG/BG.png')
bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))


#Load tile images
tile_img = []
no_of_tile = 13
for i in range(no_of_tile):  # Assuming there are 13 different tile images
    img = pg.image.load(f'{assets}/Tiles/{i+1}.png')
    img = pg.transform.scale(img, (tile_size, tile_size))
    tile_img.append(img)

no_of_object = 5
object_img = []
for i in range(no_of_tile, no_of_object+no_of_tile):  # Assuming there are 5 different tile images
    img = pg.image.load(f'{assets}/Object/{i+1}.png')
    img = pg.transform.scale(img, (tile_size, tile_size)) if i!=14 else pg.transform.scale(img, (160,200)) 
    object_img.append(img)

# Define game variables
clicked = False
level = 1
font = pg.font.SysFont('Futura', 24)

# Define colours
white = (255, 255, 255)
green = (144, 201, 120)

# Create empty tile list
rows = screen_height // tile_size
columns = screen_width // tile_size + 1

world_data = []
for row in range(rows):
    r = [0] * columns
    world_data.append(r)

# Draw world function
def draw_world():
    for r in range(rows):
        for col in range(columns):
            data = world_data[r][col]
            if data > 0:
                
                if data <= no_of_tile: #land tiles
                    if data <= no_of_tile:
                        screen.blit(tile_img[data-1], (col * tile_size, r * tile_size)) 
                    # elif data == no_of_tile: # Rock
                    #         tile_img[data -1] = pg.transform.scale(tile_img[data -1], (80,50))
                    #         screen.blit(tile_img[data -1], (col*tile_size, r*tile_size - 9))    
                                   
                elif data <= no_of_object + no_of_tile:
                    if data == 14: # Ice crystal
                        screen.blit(object_img[data - no_of_tile -1], (col*tile_size, r*tile_size))
                    elif data == 15: # Tree
                        object_img[data - no_of_tile -1] = pg.transform.scale(object_img[data - no_of_tile -1], (160,200))
                        screen.blit(object_img[data - no_of_tile -1], (col*tile_size, r*tile_size))
                        
                    elif data == 16: # Sign board
                        screen.blit(object_img[data - no_of_tile -1], (col*tile_size, r*tile_size))
                        
                    elif data == 17: # Igloo house
                        screen.blit(object_img[data - no_of_tile -1], (col*tile_size, r*tile_size))
                        
                    elif data == 18: # Snowman
                        object_img[data - no_of_tile -1] = pg.transform.scale(object_img[data - no_of_tile -1], (100, 109))
                        screen.blit(object_img[data - no_of_tile -1], (col*tile_size, r*tile_size+12))
                draw_text(f'{data}', font, white, col * tile_size + 20, r * tile_size + 20)
                        
                    
                        


def draw_grid():
    for i in range(0, screen_height, tile_size):
        pg.draw.line(screen, (255, 255, 255), (0, i), (screen_width, i))
    for i in range(0, screen_width, tile_size):
        pg.draw.line(screen, (255, 255, 255), (i, 0), (i, screen_height))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Main loop
run = True
clicked = False
last_pos = (0,rows - 1)

load_action, save_action = False, False

    
total_images = no_of_tile + no_of_object
while run:
    screen.blit(bg_image, (0, 0))
    draw_grid()
    draw_world()
    if save_action:
        # Save level data
        with open(f'levels/Level{level}_data', 'wb') as pickle_out:
            pickle.dump(world_data, pickle_out)
    if load_action:
        #load level data
        if path.exists(f'levels/Level{level}_data'):
            with open(f'levels/Level{level}_data', 'rb') as pickle_in:
                world_data = pickle.load(pickle_in)

    # Text showing current level
    draw_text(f'Level: {level}', font, white, 80, 10)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # Mouse clicks to change tiles
        if event.type == pg.MOUSEBUTTONDOWN and not clicked:
            clicked = True
            pos = pg.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            last_pos = (x, y)
            # Check that the coordinates are within the tile area
            if x < columns and y < rows:
                #update tile value
                if pg.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > total_images:
                        world_data[y][x] = 0
                elif pg.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = total_images
        if event.type == pg.MOUSEBUTTONUP:
            clicked = False
            last_pos = (0, rows-1)
        # Up and down key presses to change level number
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                level += 1
            if event.key == pg.K_DOWN:
                level -= 1
            if event.key == pg.K_s:
                save_action = True
            if event.key == pg.K_l:
                load_action = True
        if event.type == pg.KEYUP:
            load_action, save_action = False, False
        
    # Handle dragging
    if clicked:
        pos = pg.mouse.get_pos()
        x = pos[0] // tile_size
        y = pos[1] // tile_size
        if (x, y) != last_pos and x < columns and y < rows:
            if pg.mouse.get_pressed()[0] == 1:
                world_data[y][x] = world_data[last_pos[1]][last_pos[0]]
            elif pg.mouse.get_pressed()[2] == 1:
                world_data[y][x] = world_data[last_pos[1]][last_pos[0]]
            last_pos = (x, y)

    pg.display.update()

pg.quit()