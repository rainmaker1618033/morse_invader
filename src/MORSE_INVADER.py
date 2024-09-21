import pygame
import sys
import numpy as np
import pyaudio
import time
import random
import string


class MorseCodePlayer:
    """
    A class for playing Morse code audio.

    This class provides functionality to convert text to Morse code
    and play it as audio using PyAudio.

    Attributes:
        dit_duration (float): Duration of a dit (dot) in seconds.
        dah_duration (float): Duration of a dah (dash) in seconds.
        freq (int): Frequency of the audio tone in Hz.
        samplerate (int): Sample rate of the audio.
        morse_code (dict): Dictionary mapping characters to their Morse code representations.
    """

    def __init__(self, dit_duration=0.1, freq=700, samplerate=44100):
        """
        Initialize the MorseCodePlayer.

        Args:
            dit_duration (float, optional): Duration of a dit in seconds. Defaults to 0.1.
            freq (int, optional): Frequency of the audio tone in Hz. Defaults to 700.
            samplerate (int, optional): Sample rate of the audio. Defaults to 44100.
        """
        self.dit_duration = dit_duration
        self.dah_duration = 3 * dit_duration
        self.freq = freq
        self.samplerate = samplerate

       # Define Morse code dictionary -- Map CHAR to Morse Code Symbol
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
        """
        Generate an audio signal for a given Morse code symbol.
        Args:
            symbol (str): The Morse code symbol ('.', '-', or ' ').
        Returns:
            numpy.ndarray: The generated audio signal.
        """
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
        """
        Play a message as Morse code audio.
        This method converts the input message to Morse code and plays it as audio.
        Args:
            message (str): The message to be played as Morse code.
        """
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

### END OF CLASS -  MorseCodePlayer ###


# Define Morse Code mappings for LEFT and RIGHT arrow key presses

class MorseCodeInterpreter:
    """
    A class for interpreting Morse code input from user events.

    This class handles the interpretation of Morse code input,
    typically from arrow key presses in a pygame environment.

    Attributes:
        morse_code (str): A string representation of the current Morse code input.
        letter_message (str): A message containing the interpreted letter or error message.
        answer (bool): A flag indicating if the current Morse code is valid.
        morse_code_mappings (dict): A dictionary mapping pygame key events to Morse code symbols.
        morse_alphabet (dict): A dictionary mapping Morse code symbols to their corresponding letters or numbers.
    """

    def __init__(self):
        """
        Initialize the MorseCodeInterpreter.
        Sets up empty initial values for all attributes.
        """
        self.morse_code = ""
        self.letter_message = ""
        self.answer = None
        self.morse_code_mappings = {
            pygame.K_LEFT: ".",
            pygame.K_RIGHT: "-"
        }
        # Define Morse code reverse dictionary -- Map Morse Code Symbol to CHAR
        self.morse_alphabet = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z','-----': '0', '.----': '1',  '..---': '2', '...--': '3', 
            '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', 
            '----.': '9', '.-.-.' :'+', '-...-': '=', '-..-.': '/'
        }

    def handle_event(self, event):
        """
        Handle a pygame event, interpreting it as Morse code input.
        This method processes pygame key events, converting arrow key
        presses to Morse code dots and dashes.
        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.morse_code_mappings:
                self.morse_code += self.morse_code_mappings[event.key]
            elif event.key == pygame.K_RETURN:
                self.interpret_morse_code()

    def interpret_morse_code(self):
        """
        Interpret the current Morse code input.
        This method decodes the current Morse code string, sets the
        letter_message attribute, and resets the morse_code string.
        """
        if self.morse_code in self.morse_alphabet:
            self.letter_message = f'Code Letter: {self.morse_alphabet[self.morse_code]}'
            self.answer = True
        else:
            self.letter_message = f'Unknown Morse Code: {self.morse_code}'
            self.answer = False
        self.morse_code = ""

    def check_valid_morse_code(self):
        """
        Check if the current Morse code input is valid.
        Returns:
            bool: True if the current Morse code is valid, False otherwise.
        """
        self.answer = self.morse_code in self.morse_alphabet
        return self.answer

    def current_morse_code(self):
        """
        Get the letter corresponding to the current Morse code input.
        Returns:
            str: The letter corresponding to the current Morse code if valid,
                 an empty string otherwise.
        """
        return self.morse_alphabet.get(self.morse_code, "")
    
    def lookup_morse_code(self, code):
        """
        Lookup the character corresponding to a given Morse code string.
        Args:
            code (str): The Morse code string to look up.
        Returns:
            str: The character corresponding to the Morse code, or an empty string if not found.
        """
        return self.morse_alphabet.get(code, "")
    
    def clear_morse_code(self):
        """
        Clear the current Morse Code String
        """
        self.morse_code = ""
        

### END OF CLASS -  MorseCodeInterpreter ###


class Marker:
    """
    A class representing a movable marker on a pygame surface.

    This class handles the creation, movement, and drawing of a marker
    that moves in a symmetrical pattern based on user input.

    Attributes:
        x (int): Current x-coordinate of the marker.
        y (int): Current y-coordinate of the marker.
        start_x (int): Initial x-coordinate of the marker.
        start_y (int): Initial y-coordinate of the marker.
        size (int): Size of the marker (width and height).
        speed_x (int): Horizontal speed of the marker (not currently used).
        speed_y (int): Vertical speed of the marker (not currently used).
        direction (int): Direction of movement (1: right, -1: left).
        color (tuple): RGB color of the marker.
        move_count (int): Counter for tracking the number of moves made.
        move_distances (list): List of tuples containing (x, y) move distances.
    """

    def __init__(self, x, y, size, speed_x, speed_y, color):
        """
        Initialize the Marker.

        Args:
            x (int): Initial x-coordinate of the marker.
            y (int): Initial y-coordinate of the marker.
            size (int): Size of the marker (width and height).
            speed_x (int): Horizontal speed of the marker (not currently used).
            speed_y (int): Vertical speed of the marker (not currently used).
            color (tuple): RGB color of the marker.
        """
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
        self.move_distances = [(190, 93), (96, 103), (45, 115), (25, 98), (10, 90), (0, 0)]  # relative x,y for move[n]

    def draw(self, surface):
        """
        Draw the marker on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the marker on.
        """
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def move(self, left_pressed, right_pressed, window_width, window_height):
        """
        Move the marker based on user input and predefined move distances.

        The marker moves horizontally based on left/right key presses and
        vertically based on the predefined move_distances.

        Args:
            left_pressed (bool): Whether the left arrow key is pressed.
            right_pressed (bool): Whether the right arrow key is pressed.
            window_width (int): Width of the game window.
            window_height (int): Height of the game window.

        Note:
            The marker's y-coordinate is always increased, creating a downward movement.
            The x-coordinate change depends on which arrow key is pressed.
        """
        move_distance = self.move_distances[self.move_count % len(self.move_distances)]
        
        if left_pressed:
            self.x -= move_distance[0]
        if right_pressed:
            self.x += move_distance[0]
        
        if self.x <= 0 or self.x >= window_width - self.size:
            self.direction *= -1
        
        if left_pressed or right_pressed:
            self.y += move_distance[1]  # Adjust Y based on move_distance
        
        self.y = min(self.y, window_height - self.size)
        
        self.move_count += 1

    def reset_marker(self):
        """
        Reset the marker to its initial position.

        This method resets the x and y coordinates to their starting values
        and resets the move count to 0.
        """
        self.x = self.start_x
        self.y = self.start_y
        self.move_count = 0

### END OF CLASS -  Marker ###


class ScoreKeeper:
    """
    A class for keeping track of scores in a game.

    This class maintains separate scores for the player and the game,
    and provides methods to increment these scores and display them
    on a pygame window.

    Attributes:
        player_score (int): The player's current score.
        game_score (int): The game's current score.
    """

    def __init__(self, font, window_width, window_height):
        """
        Initialize the ScoreKeeper.

        Args:
            font (pygame.font.Font): The font to use for rendering the score.
            window_width (int): The width of the game window.
            window_height (int): The height of the game window.
        """
        self.player_score = 0
        self.game_score = 0
        self.font = font
        self.window_width = window_width
        self.window_height = window_height

    def increment_player_score(self):
        """Increment the player's score by 1."""
        self.player_score += 1

    def increment_game_score(self):
        """Increment the game's score by 1."""
        self.game_score += 1

    def display_score(self, window):
        """
        Display the current scores on the given pygame window.

        Args:
            window (pygame.Surface): The pygame window surface on which to display the scores.
        """
        score_text = f"Match: {self.player_score}  Miss: {self.game_score}"
        score_surface = self.font.render(score_text, True, (0, 0, 255))
        score_rect = score_surface.get_rect(center=(self.window_width // 2, (self.window_height - 200) // 2))
        window.blit(score_surface, score_rect)

### END OF CLASS -  ScoreKeeper ###



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

# ---------------------------------
#  SHow Game Instructions
# ---------------------------------	
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
#  Generate random alpha-numeric characters
#  1) Need to re-write this to use characters contained in class character maps
#  2) 
# ---------------------------------	
def generate_random_character():
    characters = string.ascii_uppercase + string.digits
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

# === Create Morse interpreter
morse_interpreter = MorseCodeInterpreter()
# === Create Morse Code Player
player = MorseCodePlayer()

# === Create an instance of the ScoreKeeper
# score_keeper = ScoreKeeper()
score_keeper = ScoreKeeper(font, window_width, window_height)

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
                #   Depending if the code symbol matches the target -- adjust the hit/miss score
                #   Set the Answer String text depending on match and clear the current morse code string
                #   Reset the marker to the starting point.
                # ---------------
                if event.key == pygame.K_RETURN: #Choose this key to verify the morse code entered by the player
				
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
    # Clear the current morse code string
    # Reset the market to Start
    # ------------------
    if Play_Rand_Char == True:
        morse_char_tgt = generate_random_character()
        #print('MORSE CHAR TGT :',morse_char_tgt)
        player.play_morse_code(morse_char_tgt)
        #time.sleep(3)
        Play_Rand_Char = False
        morse_interpreter.morse_code = ""
        marker.reset_marker() # Reset marker to starting position


    # ------------------
    # Update Score and Marker Position
    # ------------------
   
    score_keeper.display_score(window)
   
    if move_flag == True:
        marker.move(left_pressed, right_pressed, window_width, window_height)
        move_flag = False   

    marker.draw(window)

    # Redraw the display
    pygame.display.update()

    # Limit frames per second
    pygame.time.Clock().tick(30)
