import pygame as pg
from pygame import mixer
from ui import Button,display_text
from dungeon_map import Map
font_path = 'assets/Fonts/fontfile.ttf'
title_font = pg.font.Font(font_path, 72)
button_font = pg.font.Font(font_path, 36)
title_pos = 200 

class StateManager:    
    def __init__(self,screen, game_state):            
        self.sound_on = True
        self.screen = screen
        self.current_state = game_state
        self.previous_state = None
        self.quit = False
        self.start_button = Button("Start Game", button_font, (500, 350), 300, 40, self.start_game)
        self.setting_button = Button("Settings", button_font, (500, 400), 300, 40, self.settings)
        self.how_to_play_button = Button("How to play", button_font, (500, 450), 300, 40, self.how_to_play)
        self.exit_button = Button("Exit", button_font, (500, 500), 300, 40, self.quit_game)
        self.sound_button = Button("Sound: On", button_font, (500, 450), 300, 40, self.sound_toggle)
        self.back_button = Button("Back", button_font, (500, 500), 300, 40, self.go_back)
        self.dungeon = None
        self.music_loaded = False
        self.music = 'assets/music/background.mp3'
        self.level_music = 'assets/music/game_loop.mp3'
        self.level_music_loaded = False
        # pg.mixer.music.load(self.music)
        # pg.mixer.music.play(-1)
        # pg.mixer.music.set_volume(0.7)

    def handle_state(self, mouse_pos, keys):
        if self.current_state != 'inside_level':
            if self.sound_on and not self.music_loaded:
                pg.mixer.music.load(self.music)
                pg.mixer.music.play(-1)
                pg.mixer.music.set_volume(0.8)
                self.music_loaded = True
                self.level_music_loaded = False
        else:
            if self.sound_on and not self.level_music_loaded:
                pg.mixer.music.load(self.level_music)
                pg.mixer.music.play(-1)
                pg.mixer.music.set_volume(0.5)
                self.music_loaded = False
                self.level_music_loaded = True
                
        if self.current_state == "main_menu":
            display_text(self.screen, title_font, "Frost Legacy", (500, title_pos))

            # Draw main menu buttons
            self.start_button.draw(self.screen, mouse_pos)
            self.setting_button.draw(self.screen, mouse_pos)
            self.how_to_play_button.draw(self.screen, mouse_pos)
            self.exit_button.draw(self.screen, mouse_pos)

        elif self.current_state == "settings":
            display_text(self.screen, title_font, "Settings", (500, 350))

            # Draw sound toggle button
            self.sound_button.draw(self.screen, mouse_pos)

            # Draw back button
            self.back_button.draw(self.screen, mouse_pos)

        elif self.current_state == "how_to_play":
            display_text(self.screen, title_font, "How to Play", (500, title_pos))

            # Show game instructions
            self.show_instructions()

            # Draw back button
            self.back_button.draw(self.screen, mouse_pos)

        elif self.current_state == "level_map":
            self.dungeon_map = Map(self.screen)
            self.dungeon_map.draw()
            # Draw back button
            self.back_button.draw(self.screen, mouse_pos)
            
        elif self.current_state == 'inside_level':
            if self.dungeon != None: 
                if self.dungeon.state_handler(self.screen,keys) or self.dungeon.level_state.player.dead_animation_played or self.dungeon.level_state.go_back: #if stage is completed, go to dungeon_map
                    self.go_to_map()
                self.dungeon.level_state.sound_on = self.sound_on
            else:
                display_text(self.screen,font_path, 'Locked',(500,400))
                
        
            
               
    def handle_mouse_click(self, mouse_pos, event):
        # Check clicks on buttons
        if self.current_state == 'main_menu':
            self.start_button.check_click(mouse_pos, event)
            self.setting_button.check_click(mouse_pos, event)
            self.how_to_play_button.check_click(mouse_pos, event)
            self.exit_button.check_click(mouse_pos, event)
        elif self.current_state == 'settings':
            self.sound_button.check_click(mouse_pos, event)
        elif self.current_state == 'level_map':
            self.dungeon = self.dungeon_map.handle_click(mouse_pos, event) #attach level map here
            self.dungeon_loader()
        elif self.current_state == 'inside_level':
            if self.dungeon.level_state.pause:                    
                self.dungeon.level_state.resume_button.check_click(pg.mouse.get_pos(), event)
                self.dungeon.level_state.back_button.check_click(pg.mouse.get_pos(), event)
                # if self.dungeon.level_state.go_back == True:
                #     self.go_to_map()
            pass
                    
        if self.current_state != 'main_menu':
            self.back_button.check_click(mouse_pos, event)
        return self.quit
    
    def start_game(self):
        self.previous_state = self.current_state
        self.current_state = "level_map"
        print("Start Game clicked")
    
    def settings(self):
        self.previous_state = self.current_state
        self.current_state = "settings"
        print("Settings clicked")

    def how_to_play(self):
        self.previous_state = self.current_state
        self.current_state = "how_to_play"
        print("How to Play clicked")

    def quit_game(self):
        self.quit = True
        print("Exit clicked")

    def sound_toggle(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            mixer.music.play(-1)
        else:
            mixer.music.stop()
        self.sound_button.text = f"Sound: {'On' if self.sound_on else 'Off'}"
        print(f"Sound {'On' if self.sound_on else 'Off'}")

    def show_instructions(self):
        instructions = [
            "1. Use arrow keys to move and jump.",
            "2. Press Space to attack.",
            "3. Press ESC to pause the game.",
            "4. Avoid obstacles, defeat enemies and reach the goal."
        ]
        for i, line in enumerate(instructions):
            display_text(self.screen, button_font, line, (300, 300 + (i * 50)))

    def go_back(self):
        # Explicitly return to main_menu state
        self.current_state = "main_menu"
        print("Going back to main menu")
    
    def dungeon_loader(self):
        if self.dungeon != None:
            self.previous_state = self.current_state
            self.current_state = 'inside_level'
        # self.back_button.position = (500,50)
    
    def go_to_map(self):
        self.current_state = 'level_map'
        self.previous_state = 'main_menu'
        # pg.mixer.music.load(self.music)
        # pg.mixer.music.play(-1)
        print('gone to map')
 
    
    

