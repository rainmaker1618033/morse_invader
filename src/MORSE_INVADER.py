import pygame
import sys
import numpy as np
import pyaudio
import time
import random
import string

def generate_random_character():
    characters = string.ascii_uppercase + string.digits
    return random.choice(characters)

# ---------------------------------
#  Morse Code Class - Play dot dash sounds
# ---------------------------------

class MorseCodePlayer:
    def __init__(self, dit_duration=0.1, freq=700, samplerate=44100):
        self.dit_duration = dit_duration
        self.dah_duration = 3 * dit_duration
        self.freq = freq
        self.samplerate = samplerate

        # Define Morse code dictionary
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
            'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
            'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
            'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.', '+': '.-.-.', '=': '-...-', 
            '/': '-..-.',' ': ' ',  # space
        }

    def generate_signal(self, symbol):
        if symbol == '.':
            duration = self.dit_duration
        elif symbol == '-':
            duration = self.dah_duration
        else:
            duration = 0.0  # for spaces

        t = np.linspace(0, duration, int(duration * self.samplerate), endpoint=False)
        signal = np.sin(2 * np.pi * self.freq * t)
        return signal

    def play_morse_code(self, message):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.samplerate,
                        output=True)

        for char in message:
            if char.upper() in self.morse_code:
                code = self.morse_code[char.upper()]
                for symbol in code:
                    signal = self.generate_signal(symbol)
                    stream.write(signal.astype(np.float32).tobytes())
                    time.sleep(self.dit_duration)  # pause between symbols
                time.sleep(self.dit_duration * 2)  # pause between characters
            else:
                time.sleep(self.dit_duration * 4)  # pause between words

        stream.stop_stream()
        stream.close()
        p.terminate()
        
    
    def play_a_dot(self):
        signal = self.generate_signal('.')
        self._play_signal(signal)

    def play_a_dash(self):
        signal = self.generate_signal('-')
        self._play_signal(signal)

    def _play_signal(self, signal):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.samplerate,
                        output=True)
        stream.write(signal.astype(np.float32).tobytes())
        time.sleep(len(signal) / self.samplerate)  # wait for signal to finish
        
        stream.stop_stream()
        stream.close()
        p.terminate()


# ---------------------------------
#  Morse Code Class - Interpret Arrow Keys as Morse Code Input
# ---------------------------------

# Define Morse Code mappings for LEFT and RIGHT arrow key presses
morse_code_mappings = {
    pygame.K_LEFT: ".",
    pygame.K_RIGHT: "-"
}

# Define Morse Code alphabet
morse_alphabet = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z',
            '-----': '0', '.----': '1',  '..---': '2', '...--': '3', '....-': '4', '.....': '5',
            '-....': '6', '--...': '7', '---..': '8', '----.': '9', '.-.-.' :'+', '-...-': '=', '-..-.': '/',
}


class MorseCodeInterpreter:
    def __init__(self):
        self.current_input = []
        self.morse_code = ""
        self.letter_message = ""
        self.answer = None
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in morse_code_mappings:
                self.current_input.append(morse_code_mappings[event.key])
                self.morse_code += morse_code_mappings[event.key]
            elif event.key == pygame.K_RETURN:
                self.interpret_morse_code() #interpret morse string

    def interpret_morse_code(self): # decode string and reset it
        if self.morse_code in morse_alphabet:
            self.letter_message = 'Code Letter: {}'.format(morse_alphabet[self.morse_code])
            self.answer = True
        else:
            self.letter_message = 'Unknown Morse Code: {}'.format(self.morse_code)
            self.answer = False
        self.morse_code = ""
        self.current_input = []
        
    def check_valid_morse_code(self):
        if self.morse_code in morse_alphabet:
            self.answer = True
        else:            
            self.answer = False
        return self.answer

    def current_morse_code(self):
        if self.morse_code in morse_alphabet:
            return morse_alphabet[self.morse_code]
        else:
            return ""

# ---------------------------------
#  Marker Movement Class 
#  Movement design depends on symetry for characters placement on the background.
#  For each move (x,y)  x can be +/- depending on arrow key, y is always positive
# ---------------------------------

# Create move distances table
#move_distances = [(200, 85), (100, 100), (35, 115), (25, 100), (5, 100), (0, 0)]
move_distances = [(190, 93), (96, 103), (45, 115), (25, 98), (10, 90), (0, 0)]  #relative x,y for move[n]
class Marker:
    def __init__(self, x, y, size, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = 1  # Initial direction (1: right, -1: left)
        self.color = color
        self.move_count = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        #print(self.x,' : ',self.y)

    def move(self, left_pressed, right_pressed, window_width, window_height, move_distances):
        move_distance = move_distances[self.move_count % len(move_distances)]

        if left_pressed:
            #self.x -= self.speed_x
            self.x -= move_distance[0]
        if right_pressed:
            #self.x += self.speed_x
            self.x += move_distance[0]
        if self.x <= 0 or self.x >= window_width - self.size:
            self.direction *= -1
        if left_pressed or right_pressed:
            self.y += move_distance[1]  # Adjust Y based on move_distance
        self.y = min(self.y, window_height - self.size)
        
        #print('move count',self.move_count,'x: ',self.x,'y: ',self.y)        
        self.move_count += 1
        
    def reset_marker(self):
        self.x = self.start_x
        self.y = self.start_y
        self.move_count = 0   # max at bottom of screen
        #print('start pos ',self.x,' : ',self.y)
		
# ---------------------------------
#  ScoreKeeper class
# ---------------------------------	
class ScoreKeeper:
    def __init__(self):
        self.player_score = 0
        self.game_score = 0

    def increment_player_score(self):
        self.player_score += 1

    def increment_game_score(self):
        self.game_score += 1

    def display_score(self, window):
        score_text = f"Match: {self.player_score}  Miss: {self.game_score}"
        score_surface = font.render(score_text, True, (0, 0, 255))
        score_rect = score_surface.get_rect(center=(window_width // 2, (window_height - 200) // 2))
        window.blit(score_surface, score_rect)

# ---------------------------------
#  SHow Game Instructions
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

# === Create Morse interpreter
morse_interpreter = MorseCodeInterpreter()
# === Create Morse Code Player
player = MorseCodePlayer()
# === Create an instance of the ScoreKeeper
score_keeper = ScoreKeeper()

# Variables to track arrow key states
left_pressed = False
right_pressed = False

# Generate random char when player presses 'R' or 'r' and play it
Play_Rand_Char = False
morse_char_tgt = ""

# ---------------------------------
# Main loop
# ---------------------------------
move_flag = False

while True:
    #Handle left/right keyboard events to accumulate morse code symbols
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:  # else process event.key
            if event.type == pygame.KEYDOWN:
                # ---------------
                # If the key press is an arrow key set the move_flag
                # Accumlate the code symbol and move the marker right or left as needed
                # ---------------
                if event.key == pygame.K_LEFT:  # DOT SYMBOL EVENT -- marker moves left 
                    left_pressed = True
                    move_flag = True
                    #print('left_arrow')
                
                if event.key == pygame.K_RIGHT: # DASH SYMBOL EVENT -- marker moves right 
                    right_pressed = True
                    move_flag = True
                    #print('right_arrow')
					
                if move_flag == True: #Handle left/right keyboard events to accumulate morse code symbols
                    morse_interpreter.handle_event(event)  

                # ---------------
                # If the key press is RETURN key 
                #   If the code symbol is valid -- Play the morse symbol dot-dash sounds
                #   Adjust the hit/miss score
                # ---------------
                if event.key == pygame.K_RETURN: #Choose this key to verify the morse code entered by the player
				
                    if morse_interpreter.check_valid_morse_code() == True:  # Play code if valid 
                        player.play_morse_code(morse_alphabet[morse_interpreter.morse_code])
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
                # If the key press is R
                #   Enable -- Select a Random Alphabetic Character
                # ---------------
                #if event.key == pygame.K_r or event.key == pygame.K_R:
                if event.key == pygame.K_r:
                    Play_Rand_Char = True
                    #print('R key down')

                # ---------------
                # Expore using  SPACE instead of R to geneerate new symbol
                # Note need to clean up keypress in following section
                # ---------------
                #if event.key == pygame.K_SPACE:
                #    Play_Rand_Char = True
                #    #print('R key down')

            # ----------------            
            # Clear key_press events on KEYUP
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
    #  Dispay Morse Code STRING and Interp ALPHA Char message
    # ------------------
    Morse_Message = 'Morse Code Symbol: {}'.format(morse_interpreter.morse_code)
    MSSG1 = font.render(Morse_Message, True, text_color)
    window.blit(MSSG1, (20, 20))
    
    if morse_interpreter.answer == True : 
        #answer_color = (0, 255, 0)  # GREEN
        answer_color = (165, 42, 42)  # BROWN
    else:
        answer_color = (255, 0, 0)  # RED


    mssg = font.render(morse_interpreter.letter_message, True, answer_color)
    window.blit(mssg, (window_width - mssg.get_width() - 20, 20))

    # Addition to display morse_char_tgt -- need to fix color
    TGT_CHAR_MSSG = 'Target Char: {}'.format(morse_char_tgt)
    tgt_char = font.render(TGT_CHAR_MSSG, True, answer_color)
    window.blit(tgt_char, (window_width - tgt_char.get_width() - 20, 40))

    # ------------------
    # Play a random character if player typed 'R' or 'r'
    # ------------------
    if Play_Rand_Char == True:
        morse_char_tgt = generate_random_character()
        #print('MORSE CHAR TGT :',morse_char_tgt)
        player.play_morse_code(morse_char_tgt)
        #time.sleep(3)
        Play_Rand_Char = False

    # Display the score
    score_keeper.display_score(window)

    # ------------------
    # Update Marker Position
    # ------------------
    # Move Marker
    if move_flag == True:
        marker.move(left_pressed, right_pressed, window_width, window_height, move_distances)
        move_flag = False   

    marker.draw(window)

    # Redraw the display
    pygame.display.update()
    # Limit frames per second
    pygame.time.Clock().tick(30)
