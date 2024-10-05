import pygame
import sys
import numpy as np
import pyaudio
import time
import random
import string
from MorseCode_Classes import MorseCodePlayer, MorseCodeInterpreter,MorseCodeEncoder
from Game_Classes import Marker, CircleMarker, ScoreKeeper

# ---------------------------------
#  Return radius and trim_xy position for circle marker based on move_count
# ---------------------------------	
def get_radius_from_list(move_count):
    radii = [0, 40, 40, 30, 30, 25, 0]
    xy_trim = [(0, 0), (10, 5), (10, 5), (15, 10), (13, 11), (7, 0)] 
    xy_mod = xy_trim[move_count]
    if 0 <= move_count < len(radii):
        return radii[move_count],xy_mod
    else:
        return "Index out of range"
    
# --------------------------------------
#  Update and Draw Game Marker Positions
# --------------------------------------	
def update_game_state(window, background_image, encoder, marker, game_marker, rand_char):

    # Clear the screen
    window.blit(background_image, (0, 0))

    # determine the next postion for the game marker
    done_flag, left_pressed, right_pressed = encoder.next_dot_dash()
    marker.move(left_pressed, right_pressed, window.get_width(), window.get_height())

    # use marker count status as index for cicle radius lookup
    new_radius, xy_mod = get_radius_from_list(marker.move_count)
    new_font_size = new_radius
    x_mod = xy_mod[0]
    y_mod = xy_mod[1]

    # Draw the game marker circle with scaled font
    game_marker.set_circle_attributes((marker.x)+x_mod, (marker.y)+y_mod, new_radius)
    game_marker.set_font_attributes(rand_char, new_font_size)
    game_marker.draw(window)

    # Update the display
    pygame.display.flip()

    if done_flag:  
        marker.reset_marker() # Reset marker to starting position
        # rand_char = generate_random_character()  
        # encoder.select_character(rand_char)

    return done_flag

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


# ---------------------------------
#  Generate random alpha-numeric and '+\='characters
# ---------------------------------	
def generate_random_character():
    characters = string.ascii_uppercase + string.digits + '+/='
    return random.choice(characters)
        
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

# Load background image
background_image = pygame.image.load("assets/images/background.jpg").convert()

# ---------------------------------
#  INIT GANE CLASSES
# ---------------------------------

# === Create Marker instance with specified color
BLK_SIZE = 25
#marker_color = (0, 255, 0)  # Example color (green)  
marker_color = (173, 216, 230) # Light Blue

# Marker for Player Position
marker_upos = Marker((window_width // 2)-25, 55, BLK_SIZE, 10, 10, marker_color)
text_color = (165, 42, 42)  # RGB for brown

# Variables to track arrow key states
left_pressed = False
right_pressed = False

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


# ---------------------------------
# Main loop
# ---------------------------------
PLAYER_MARKER_MOVING = False

while True:
    
    for event in pygame.event.get():
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
                    #print('left_arrow')
                
                if event.key == pygame.K_RIGHT: # DASH SYMBOL EVENT -- marker moves right 
                    right_pressed = True
                    PLAYER_MARKER_MOVING = True
                    #print('right_arrow')
					
                if PLAYER_MARKER_MOVING == True: 
                    # event = Left/Right: Accumulate morse code symbols [ONLY]
                    morse_interpreter.handle_event(event)  
                    # NOTE 'RETURN' could only get handled here if PLAYER_MARKER_MOVING is True, however,
                    # PLAYER_MARKER_MOVING is cleared below each time the arrow key moves the cursor

                # ---------------
                # If the key press is RETURN [EMTER] key 
                #   If the code symbol is valid -- Play the morse symbol dot-dash sounds
                #   Adjust the Game score
                #   Set the Answer String text depending on match case and clear the current morse code string
                #   Reset the marker to the starting point.
                # ---------------
                if event.key == pygame.K_RETURN: # Choose this key to verify the morse code entered by the player
				
                    if morse_interpreter.check_valid_morse_code() == True:  # Play code if valid 
                        code_player.play_morse_code(morse_interpreter.lookup_morse_code(morse_interpreter.morse_code))
                        #print('Play Morse Code if VALID')

                    if morse_char_tgt == morse_interpreter.current_morse_code():
                        score_keeper.increment_player_score()
                    else:
                        score_keeper.increment_game_score()

                    morse_interpreter.handle_event(event) #handle K_RETURN -> clear the string
                    #print('Classify MORSE LETTER STRING and clear string')

                    marker_upos.reset_marker() # Reset marker to starting position
                    #print('Reset Marker Pos')

                # ---------------
                # Play a random character if player typed 'R' or 'r'    
                # i.e. event.key == pygame.K_r or event.key == pygame.K_R:
                # Clear the current morse code string
                # Reset the market to Start
                # ---------------
                if event.key == pygame.K_r:
                    morse_char_tgt = generate_random_character()
                    #print('MORSE CHAR TGT :',morse_char_tgt)
                    code_player.play_morse_code(morse_char_tgt)
                    #time.sleep(3)
                    morse_interpreter.morse_code = ""
                    marker_upos.reset_marker() # Reset marker to starting position

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

    # END OF FOR LOOP SCOPE
    
    # Clear the screen
    window.blit(background_image, (0, 0))
     
    # ------------------
    #  Display accumulated Morse Code or '___________' if none is entered
    # ------------------
    if len(morse_interpreter.morse_code) > 0 :
        Morse_Message = 'Morse Code Symbol: {}'.format(morse_interpreter.morse_code)
    else:     
        Morse_Message = '_________________:'

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

    # Temporary Addition to display morse_char_tgt  
    # Replace with circle marker
    TGT_CHAR_MSSG = 'Target Char: {}'.format(morse_char_tgt)
    tgt_char = font.render(TGT_CHAR_MSSG, True, morse_interpreter.answer_color)
    window.blit(tgt_char, (window_width - tgt_char.get_width() - 20, 40))

    # ------------------
    # Update Score and Marker Position
    # ------------------
    score_keeper.display_score(window)
   
    if PLAYER_MARKER_MOVING == True:
        marker_upos.move(left_pressed, right_pressed, window_width, window_height)
        PLAYER_MARKER_MOVING = False   

    marker_upos.draw(window)

    # Redraw the display
    #pygame.display.update()
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)
