import pygame
import sys
import time
from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np
import pyaudio
import random
import string
from MorseCode_Classes import MorseCodePlayer, MorseCodeInterpreter,MorseCodeEncoder
from Game_Classes import RectangleMarker, CircleMarker, ScoreKeeper, MarkerPause, StartSequence

class CompositeMarker:
    """Comibines three classes to enable simpler implementation of game marker"""
    def __init__(self, x, y, size, speed_x, speed_y, color, window_size):
        self.rectangle_marker = RectangleMarker(x, y, size, speed_x, speed_y, color)
        self.circle_marker = CircleMarker(window_size)
        self.encoder = MorseCodeEncoder()

    def draw_marker(self, surface):
        self.rectangle_marker.draw(surface)
    
    def move_mkr(self, left_pressed, right_pressed, window_width, window_height):
        self.rectangle_marker.move_mkr(left_pressed, right_pressed, window_width, window_height)

    def reset_marker(self):
        self.rectangle_marker.reset_marker()

    def encode_character(self, char):
        self.encoder.select_character(char)

    def generate_random_character(self):
        return self.encoder.generate_random_character()        

    def next_dot_dash(self):
        return self.encoder.next_dot_dash()

    def reset_encoder(self):
        self.encoder.reset()

    def draw_circle(self, surface):
        self.circle_marker.draw(surface)

    def clear_text(self):
        self.circle_marker.clear_text()
    
    def set_circle_attributes(self, x, y, radius):
        self.circle_marker.set_circle_attributes(x, y, radius)

    def set_font_attributes(self, TGT_LTR, NEW_SIZE):
        self.circle_marker.set_font_attributes(TGT_LTR, NEW_SIZE)

    def get_radius_from_list(self, move_count):
        return self.circle_marker.get_radius_from_list(move_count)


@dataclass
class GameConfig:
    """Game configuration settings"""
    WINDOW_SIZE: Tuple[int, int] = (800, 600)
    BLOCK_SIZE: int = 25
    MARKER_COLOR: Tuple[int, int, int] = (173, 216, 230)  # Light Blue
    TEXT_COLOR: Tuple[int, int, int] = (165, 42, 42)  # Brown
    FONT_SIZE: int = 36
    UPDATE_INTERVAL: float = 0.5  # 500ms in seconds
    FPS: int = 30

class GameState:
    """Manages the game's current state"""
    def __init__(self):
        self.player_moving = False
        self.game_marker_moving = False
        self.left_pressed = False
        self.right_pressed = False
        self.morse_char_target = ""
        self.last_update_time = time.time()

    def reset_movement(self):
        self.player_moving = False
        self.left_pressed = False
        self.right_pressed = False

class MorseInvaderGame:
    def __init__(self):
        self.config = GameConfig()
        self.state = GameState()
        self.initialize_pygame()
        self.initialize_game_objects()

    def initialize_pygame(self):
        """Initialize Pygame and create the game window"""
        pygame.init()
        pygame.display.set_caption("Morse Invader")
        self.window = pygame.display.set_mode(self.config.WINDOW_SIZE)
        self.font = pygame.font.Font(None, self.config.FONT_SIZE)
        self.background = pygame.image.load("assets/images/background.png")
        self.clock = pygame.time.Clock()

    def initialize_game_objects(self):
        """Initialize game objects and components"""
        window_center = self.config.WINDOW_SIZE[0] // 2
        
        # Initialize game components
        self.player_marker = RectangleMarker(
            window_center - 25, 55, 
            self.config.BLOCK_SIZE, 10, 10, 
            self.config.MARKER_COLOR
        )
        
        self.game_marker = CompositeMarker(
            window_center - 25, 55,
            self.config.BLOCK_SIZE, 10, 10,
            self.config.MARKER_COLOR,
            self.config.WINDOW_SIZE
        )
        
        self.score_keeper = ScoreKeeper(self.font, *self.config.WINDOW_SIZE)
        self.morse_interpreter = MorseCodeInterpreter()
        self.code_player = MorseCodePlayer()
        self.encoder = MorseCodeEncoder()
        self.marker_pause = MarkerPause()

    def handle_input(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event)
                
        return True

    def handle_keydown(self, event):
        """Handle keyboard press events"""
        if event.key == pygame.K_LEFT:
            self.handle_movement_key(True, False)
        elif event.key == pygame.K_RIGHT:
            self.handle_movement_key(False, True)
        elif event.key == pygame.K_RETURN:
            self.handle_return_key()
        elif event.key == pygame.K_r:
            self.handle_random_character()

    def handle_keyup(self, event):
        """Handle keyboard release events"""
        if event.key == pygame.K_LEFT:
            self.state.left_pressed = False
        elif event.key == pygame.K_RIGHT:
            self.state.right_pressed = False

    def handle_movement_key(self, left: bool, right: bool):
        """Handle movement key presses"""
        self.state.left_pressed = left
        self.state.right_pressed = right
        self.state.player_moving = True
        self.morse_interpreter.letter_message = ""
        self.morse_interpreter.handle_arrow_keys(left,right)

    def handle_return_key(self):
        """Handle return key press"""
        if self.morse_interpreter.check_valid_morse_code():
            self.code_player.play_morse_code(
                self.morse_interpreter.lookup_morse_code(
                    self.morse_interpreter.morse_code
                )
            )
            
        if self.state.morse_char_target == self.morse_interpreter.current_morse_code():
            self.score_keeper.increment_player_score()
        else:
            self.score_keeper.increment_game_score()

        self.morse_interpreter.handle_return_key()
        self.morse_interpreter.morse_code = ""
        self.state.morse_char_target = "."
            
        self.reset_game_state()

    def handle_random_character(self):
        """Handle generating a random character target"""
        if not self.state.game_marker_moving:
            self.state.morse_char_target = self.game_marker.encoder.generate_random_character()
            self.game_marker.encode_character(self.state.morse_char_target)
            self.code_player.play_morse_code(self.state.morse_char_target)
            
            self.morse_interpreter.morse_code = ""
            self.player_marker.reset_marker()
            self.marker_pause.set_count(8)
            self.state.game_marker_moving = True

    def update_game_marker(self):
        """Update game marker position and state"""
        current_time = time.time()
        if (current_time - self.state.last_update_time >= self.config.UPDATE_INTERVAL 
            and self.state.game_marker_moving):
            
            if self.marker_pause.update():
                move_done, left, right = self.game_marker.next_dot_dash()
                self.game_marker.move_mkr(
                    left, right,
                    self.config.WINDOW_SIZE[0],
                    self.config.WINDOW_SIZE[1]
                )
                
                self.update_marker_visuals()
                
                if move_done:
                    self.state.game_marker_moving = False
                    self.game_marker.reset_marker()
                else:
                    self.state.last_update_time = current_time
            else:
                self.reset_game_marker_position()

    def update_marker_visuals(self):
        """Update visual aspects of the game marker"""
        move_count = self.game_marker.rectangle_marker.move_count
        radius, xy_mod = self.game_marker.get_radius_from_list(move_count)
        
        x_mod = xy_mod[0] + self.game_marker.rectangle_marker.x
        y_mod = xy_mod[1] + self.game_marker.rectangle_marker.y
        
        self.game_marker.set_circle_attributes(x_mod, y_mod, radius)
        self.game_marker.set_font_attributes(self.state.morse_char_target, radius)

    def reset_game_state(self):
        """Reset game state after input verification"""
        self.morse_interpreter.handle_event(pygame.event.Event(pygame.K_RETURN))
        self.player_marker.reset_marker()
        self.game_marker.reset_marker()
        self.reset_game_marker_position()

    def reset_game_marker_position(self):
        """Reset game marker to starting position"""
        self.game_marker.set_circle_attributes(
            (self.config.WINDOW_SIZE[0] // 2) - 15,
            65,
            10
        )
        self.game_marker.clear_text()

    def update_display(self):
        """Update game display"""
        self.window.blit(self.background, (0, 0))
        self.draw_morse_code()
        self.draw_interpreted_code()
        self.score_keeper.display_score(self.window)
        
        if self.state.player_moving:
            self.player_marker.move_mkr(
                self.state.left_pressed,
                self.state.right_pressed,
                self.config.WINDOW_SIZE[0],
                self.config.WINDOW_SIZE[1]
            )
            self.state.player_moving = False
        
        self.player_marker.draw(self.window)
        self.game_marker.draw_circle(self.window)
        pygame.display.flip()

    def draw_morse_code(self):
        """Draw current morse code input"""
        message = (f'Morse Code Symbol: {self.morse_interpreter.morse_code}'
                  if self.morse_interpreter.morse_code
                  else '_________________:')
        
        text_surface = self.font.render(message, True, self.config.TEXT_COLOR)
        self.window.blit(text_surface, (20, 20))

    def draw_interpreted_code(self):
        """Draw interpreted morse code character"""
        if self.morse_interpreter.letter_message:
            message = self.morse_interpreter.letter_message
            color = self.morse_interpreter.answer_color
        else:
            message = '_________________:'
            color = self.config.TEXT_COLOR
            
        text_surface = self.font.render(message, True, color)
        self.window.blit(
            text_surface,
            (self.config.WINDOW_SIZE[0] - text_surface.get_width() - 20, 20)
        )

    def run(self):
        """Main game loop"""
        running = True
        self.reset_game_marker_position()
        while running:
            running = self.handle_input()
            self.update_game_marker()
            self.update_display()
            self.clock.tick(self.config.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    start_sequence = StartSequence()
    start_sequence.run_intro()
    game = MorseInvaderGame()
    game.run()