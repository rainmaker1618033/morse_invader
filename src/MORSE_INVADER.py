import pygame
import sys
import numpy as np
import pyaudio
import time
import random
import string
from MorseCode_Classes import MorseCodePlayer, MorseCodeInterpreter,MorseCodeEncoder
from Game_Classes import RectangleMarker, CircleMarker, ScoreKeeper, MarkerPause


######## COMPOSITE CLASSES ################

class CompositeMarker:
    def __init__(self, x, y, size, speed_x, speed_y, color, window_size):
        self.rectangle_marker = RectangleMarker(x, y, size, speed_x, speed_y, color)
        self.circle_marker = CircleMarker(window_size)
        self.encoder = MorseCodeEncoder()
        #print(f"Type of self.rectangle_marker: {type(self.rectangle_marker)}")
        #print(f"Methods of self.rectangle_marker: {[method for method in dir(self.rectangle_marker) if callable(getattr(self.rectangle_marker, method))]}")

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
    
    def set_circle_attributes(self, x, y, radius):
        self.circle_marker.set_circle_attributes(x, y, radius)

    def set_font_attributes(self, TGT_LTR, NEW_SIZE):
        self.circle_marker.set_font_attributes(TGT_LTR, NEW_SIZE)

    def get_radius_from_list(self, move_count):
        return self.circle_marker.get_radius_from_list(move_count)

######## END OF CLASSES ################

# ---------------------------------
#  Show Game Instructions
# ---------------------------------	
# Instruction text
instructions = [
    "    Welcome to Morse Invader!",
	" ",	
    " While Forever",
	"   1) Press 'R' to play a random Morse code character.",
    "   2) Press left and right arrow keys to enter matching Morse code.",
    "   3) Press 'Enter' to see if your Morse code matches.",
	" ",	
    "Press 'Enter' to start the game."
]	

def show_instructions():
    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showing = False

        window.fill((0, 0, 0))  # Fill the screen with black
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, (0, 0, 255))  # Render text in blue
            window.blit(instruction_text, (20, 20 + i * 40))

        pygame.display.update()
        pygame.time.Clock().tick(30)

### END OF FUNCTIONS ###


# ---------------------------------
#  MAIN INIT GRAPHICS
# ---------------------------------

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Morse Invader")

# Set up the game window
window_size = (800, 600)
window_width = window_size[0]
window_height = window_size[1]
window = pygame.display.set_mode(window_size)

# Font Size
font = pygame.font.Font(None, 36)

# Show instructions before starting the game
show_instructions()	

# ---------------------------------
#  MISC SETUP
# ---------------------------------
# Load background image
background_image = pygame.image.load("assets/images/background.jpg").convert()
## original size of rectangular marker -- needed?
BLK_SIZE = 25  
# Light Blue -- Green (0, 255, 0)  
marker_color = (173, 216, 230) 
# RGB for brown -- used for default message color
text_color = (165, 42, 42)  
# === Variables to track arrow-key states
left_pressed = False
right_pressed = False
# used to initially pause game_marker movement
game_marker_pause = MarkerPause()
# ---------------------------------
#  INIT GAME CLASSES
# ---------------------------------
# === Marker for Player Position
player_marker = RectangleMarker((window_width // 2)-25, 55, BLK_SIZE, 10, 10, marker_color)
PLAYER_MARKER_MOVING = False # player has not hit left/right arrow keys
# === Game Marker Position
game_marker = CompositeMarker((window_width // 2)-25, 55, BLK_SIZE, 10, 10, marker_color, window_size)
GAME_MARKER_MOVING = False # Game Target Circle is not displayed 
# === Create ScoreKeeper
score_keeper = ScoreKeeper(font, window_width, window_height)

# ---------------------------------
#  INIT MORSE CODE CLASSES
# ---------------------------------
# === Create Morse Code Interpreter
morse_interpreter = MorseCodeInterpreter()
# Updated when player presses 'R' or 'r'  
morse_char_tgt = ""
# === Create Morse Code Player
code_player = MorseCodePlayer()
# ==== Create an instance of MorseCodeEncoder  
encoder = MorseCodeEncoder()

# ---------------------------------
# Main loop
# ---------------------------------
# Set up the interval timer for game maker update
interval = 0.5  # 500ms in seconds
start_time = time.time()

max_count_events = 0

while True:
    elapsed_time = time.time()
    
    #events = pygame.event.get()
    #print(f"Number of events in the queue: {len(events)}")
    #if len(events) > max_count_events:
    #        max_count_events = len(events)
    #        print('MAX COUNT :',max_count_events)

    #for event in pygame.event.get():
    #for event in events:
    event = pygame.event.poll()
    if event.type == pygame.NOEVENT:
        continue
		
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    else:  # else process event.key
        if event.type == pygame.KEYDOWN:
            # ---------------
            # Handle left/right keyboard events to move marker and accumulate morse code symbols
            # ---------------
            if event.key == pygame.K_LEFT:  # DOT SYMBOL EVENT -- marker moves left 
                left_pressed = True
                PLAYER_MARKER_MOVING = True
                morse_interpreter.letter_message = ""  # Blank the previous letter_message
                #print('left_arrow')
            
            if event.key == pygame.K_RIGHT: # DASH SYMBOL EVENT -- marker moves right 
                right_pressed = True
                PLAYER_MARKER_MOVING = True
                morse_interpreter.letter_message = ""  # Blank the previous letter_message
                #print('right_arrow')
				
            if PLAYER_MARKER_MOVING == True:  # if Left/Right event occured: 
                morse_interpreter.handle_event(event)  # Accumulate morse code symbols, 
                # 'RETURN'/update letter_message text' is handled in its own IF CASE below

            # ---------------
            # If the key press is RETURN [EMTER] key 
            #   If the code symbol is valid -- Play the morse symbol dot-dash sounds
            #   Adjust the Game score
            #   Reset the marker to the starting point.
            # ---------------
            if event.key == pygame.K_RETURN: # Choose this key to verify the morse code entered by the player
			
                if morse_interpreter.check_valid_morse_code() == True:  # Play code if valid 
                    code_player.play_morse_code(morse_interpreter.lookup_morse_code(morse_interpreter.morse_code))
                if morse_char_tgt == morse_interpreter.current_morse_code():
                    score_keeper.increment_player_score()
                else:
                    score_keeper.increment_game_score()
                morse_interpreter.handle_event(event) #handle K_RETURN -> clear the dot-dash string
                player_marker.reset_marker() # Reset marker to starting position


            # ---------------
            # If event.key == pygame.K_r or event.key == pygame.K_R:
            #   Play a random character  
            # Clear the current morse code string
            # Reset the market to Start
            # ---------------
            if event.key == pygame.K_r:
                if GAME_MARKER_MOVING is False:
                    morse_char_tgt = game_marker.encoder.generate_random_character()
                    print('INIT GAME MRKR - MORSE CHAR TGT :',morse_char_tgt)
                    game_marker.encode_character(morse_char_tgt)
                    code_player.play_morse_code(morse_char_tgt)
                    morse_interpreter.morse_code = ""
                    player_marker.reset_marker() # Reset marker to starting position   
                    game_marker_pause.set_count(4) # wait 3 update times before first moving the marker                 
                    GAME_MARKER_MOVING = True

        # ----------------            
        # else clear selected flag if its KEYUP
        # ----------------
        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT:
                left_pressed = False
                #print('negate left_arrow')
            elif event.key == pygame.K_RIGHT:
                right_pressed = False
                #print('negate right_arrow')
            elif event.key == pygame.K_r:
                #print('R key up')
                pass

    # END OF ELSE PROCESS EVENT CLAUSE
    
    # Clear the screen
    window.blit(background_image, (0, 0))
     
    # ------------------
    #  Display accumulated Morse Code or '___________' if none is entered
    # ------------------
    if len(morse_interpreter.morse_code) > 0 :
        Morse_Message = 'Morse Code Symbol: {}'.format(morse_interpreter.morse_code)
    else:     
        Morse_Message = '_________________:'
        #morse_interpreter.letter_message = ""

    MSSG1 = font.render(Morse_Message, True, text_color)
    window.blit(MSSG1, (20, 20))

    # ------------------ 
    #  Display Interpreted Morse Code Character or '___________' if player hasn't hit RETURN
    # ------------------    
    if  morse_interpreter.letter_message != "":
        mssg = font.render(morse_interpreter.letter_message, True, morse_interpreter.answer_color)
    else:     
        mssg = font.render('_________________:', True, text_color)   
        
    window.blit(mssg, (window_width - mssg.get_width() - 20, 20))


    # ------------------
    # Update Game Marker Position
    # ------------------
    # Check if the interval has passed and GAME_MARKER needs updating
    if elapsed_time - start_time >= interval and GAME_MARKER_MOVING:  
        ready_to_move = game_marker_pause.update()  # wait 3 pause states
        print((lambda x: True if x else False)(ready_to_move))
        if ready_to_move :

            # encode current morse_char_tgt char into 'next' left/right = dot/dash
            move_done_flag, left_pressed, right_pressed = game_marker.next_dot_dash()
            # next marker position based on left/right; move_count++
            game_marker.move_mkr(left_pressed, right_pressed, window.get_width(), window.get_height())

            move_count = game_marker.rectangle_marker.move_count
            radius, xy_mod = game_marker.get_radius_from_list(move_count)
            # add corrected x/y offset to marker postions
            x_mod = xy_mod[0] + game_marker.rectangle_marker.x
            y_mod = xy_mod[1] + game_marker.rectangle_marker.y

            game_marker.set_circle_attributes(x_mod, y_mod, radius)
            game_marker.set_font_attributes(morse_char_tgt, radius)  # radius determins font size

            if move_done_flag:  # if the game marker has reached its destination    
                GAME_MARKER_MOVING = False
                game_marker.reset_marker() # Reset marker to starting position            
                print('WAIT FOR NEXT KEY PRESS')
            else:
                # reset the timer for next update
                start_time = elapsed_time
                print('*')

    # ------------------
    # Update Score and Marker Position
    # ------------------
    score_keeper.display_score(window)
   
    if PLAYER_MARKER_MOVING == True:
        player_marker.move_mkr(left_pressed, right_pressed, window_width, window_height)
        PLAYER_MARKER_MOVING = False   

    
    player_marker.draw(window)
    game_marker.draw_circle(window)


    #marker_gpos.draw(window)

    # Redraw the display
    #pygame.display.update()
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)
