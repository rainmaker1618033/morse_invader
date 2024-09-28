import pygame
import sys
import numpy as np
import pyaudio
import time
import random
import string
from Game_Classes import MorseCodePlayer, MorseCodeInterpreter,Marker,ScoreKeeper

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
#  MAIN INIT
# ---------------------------------

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Morse Invader")

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Font Size
font = pygame.font.Font(None, 36)

# Show instructions before starting the game
show_instructions()	

# Load background image
background_image = pygame.image.load("assets/images/background.jpg").convert()

# === Create Marker instance with specified color
BLK_SIZE = 25
marker_color = (0, 255, 0)  # Example color (green)  
marker = Marker((window_width // 2)-25, 55, BLK_SIZE, 10, 10, marker_color)
text_color = (165, 42, 42)  # RGB for brown

# === Create Morse Code Interpreter
morse_interpreter = MorseCodeInterpreter()

# === Create Morse Code Player
player = MorseCodePlayer()

# === Create ScoreKeeper
score_keeper = ScoreKeeper(font, window_width, window_height)

# Variables to track arrow key states
left_pressed = False
right_pressed = False

# Updated when player presses 'R' or 'r'  
morse_char_tgt = ""

# ---------------------------------
# Main loop
# ---------------------------------
move_flag = False

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
                    move_flag = True
                    #print('left_arrow')
                
                if event.key == pygame.K_RIGHT: # DASH SYMBOL EVENT -- marker moves right 
                    right_pressed = True
                    move_flag = True
                    #print('right_arrow')
					
                if move_flag == True: 
                    # event = Left/Right: Accumulate morse code symbols [ONLY]
                    morse_interpreter.handle_event(event)  
                    # NOTE 'RETURN' could only get handled here if move_flag is True, however,
                    # move_flag is cleared below each time the arrow key moves the cursor

                # ---------------
                # If the key press is RETURN [EMTER] key 
                #   If the code symbol is valid -- Play the morse symbol dot-dash sounds
                #   Depending if the code symbol matches the target -- adjust the hit/miss score
                #   Set the Answer String text depending on match case and clear the current morse code string
                #   Reset the marker to the starting point.
                # ---------------
                if event.key == pygame.K_RETURN: # Choose this key to verify the morse code entered by the player
				
                    if morse_interpreter.check_valid_morse_code() == True:  # Play code if valid 
                        player.play_morse_code(morse_interpreter.lookup_morse_code(morse_interpreter.morse_code))
                        #print('Play Morse Code if VALID')

                    if morse_char_tgt == morse_interpreter.current_morse_code():
                        score_keeper.increment_player_score()
                    else:
                        score_keeper.increment_game_score()

                    morse_interpreter.handle_event(event) #handle K_RETURN -> clear the string
                    #print('Classify MORSE LETTER STRING and clear string')

                    marker.reset_marker() # Reset marker to starting position
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
                    player.play_morse_code(morse_char_tgt)
                    #time.sleep(3)
                    morse_interpreter.morse_code = ""
                    marker.reset_marker() # Reset marker to starting position

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

    # Addition to display morse_char_tgt -- need to fix color
    TGT_CHAR_MSSG = 'Target Char: {}'.format(morse_char_tgt)
    tgt_char = font.render(TGT_CHAR_MSSG, True, morse_interpreter.answer_color)
    window.blit(tgt_char, (window_width - tgt_char.get_width() - 20, 40))

    ## where the code for R key was...

    # ------------------
    # Update Score and Marker Position
    # ------------------
   
    score_keeper.display_score(window)
   
    if move_flag == True:
        marker.move(left_pressed, right_pressed, window_width, window_height)
        move_flag = False   

    marker.draw(window)

    # Redraw the display
    #pygame.display.update()
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)
