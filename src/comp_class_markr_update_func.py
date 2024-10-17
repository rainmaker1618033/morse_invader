import pygame
import time
import random
import string

class MorseCodeEncoder:
    """
    A class to encode alpha-numeric characters into Morse code, allowing step-by-step conversion.

    This class provides functionality to convert individual characters into their Morse code
    equivalents and retrieve the code one element (dot or dash) at a time.

    Attributes:
        morse_code (dict): A dictionary mapping characters to their Morse code equivalents.
        current_code (str): The current Morse code sequence being processed.
        current_index (int): The current position in the Morse code sequence.
    """
    def __init__(self):
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
            'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
            'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
            'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.', '+': '.-.-.', '=': '-...-', 
            '/': '-..-.',' ': ' ',  # space
        }
        self.current_code = ""
        self.current_index = 0

    def select_character(self, char):
        if char in self.morse_code:
            self.current_code = self.morse_code[char]
            self.current_index = 0
        else:
            raise ValueError(f"Character not found in Morse code dictionary: {char}")

    def generate_random_character(self):
        characters = string.ascii_uppercase + string.digits + '+/='
        return random.choice(characters)        

    def next_dot_dash(self):
        if self.current_index < len(self.current_code):
            dot_dash = self.current_code[self.current_index]
            self.current_index += 1
            done_flag = self.current_index == len(self.current_code)
            if dot_dash == '.':
                return done_flag, True, False
            elif dot_dash == '-':
                return done_flag, False, True
            else:
                raise ValueError(f"Unexpected character in Morse code: {dot_dash}")
        else:
            raise IndexError("No more dots or dashes to return")

    def reset(self):
        self.current_index = 0

class RectangleMarker:
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
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = 1
        self.color = color
        self.move_count = 0
        self.move_distances = [(190, 93), (96, 103), (45, 115), (25, 98), (10, 90), (0, 0)]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def move_mkr(self, left_pressed, right_pressed, window_width, window_height):
        move_distance = self.move_distances[self.move_count % len(self.move_distances)]
        
        if left_pressed:
            self.x -= move_distance[0]
        if right_pressed:
            self.x += move_distance[0]
        
        if self.x <= 0 or self.x >= window_width - self.size:
            self.direction *= -1
        
        if left_pressed or right_pressed:
            self.y += move_distance[1]
        
        self.y = min(self.y, window_height - self.size)
        self.move_count += 1

    def reset_marker(self):
        self.x = self.start_x
        self.y = self.start_y
        self.move_count = 0



class CircleMarker:
    """
    A class to represent a circle marker with text in a Pygame window.

    This class encapsulates the properties and methods for creating and
    managing a circular marker with centered text, which can be drawn
    on a Pygame surface.

    Attributes:
        window_size (tuple): The size of the Pygame window (width, height).
        circle_center (list): The center coordinates of the circle [x, y].
        circle_radius (int): The radius of the circle in pixels.
        circle_color (tuple): The color of the circle in RGB format (r, g, b).
        font_size (int): The size of the font for the text in pixels.
        font_color (tuple): The color of the font in RGB format (r, g, b).
        text (str): The text to be displayed inside the circle.
        font (pygame.font.Font): The font object for rendering text.
        text_surface (pygame.Surface): The surface containing the rendered text.
        text_rect (pygame.Rect): The rectangle enclosing the text surface.
    """
    def __init__(self, window_size):
        self.window_size = window_size
        self.circle_center = [window_size[0] // 2, window_size[1] // 2]
        self.circle_radius = 100
        self.circle_color = (255, 0, 0)
        self.font_size = 50
        self.font_color = (255, 255, 255)
        self.text = "_"  # unknown character guard
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.circle_center)
        self.move_count = 0
        self.radii = [0, 40, 40, 30, 30, 25, 0]
        self.xy_trim = [(0, 0), (10, 5), (10, 5), (15, 10), (13, 11), (7, 0)] 

    def set_circle_attributes(self,x,y,radius):
        self.circle_center = [x,y]
        self.circle_radius = radius

    def set_font_attributes(self,TGT_LTR,NEW_SIZE):
        #self.font_size = random.randint(30, 100)
        self.text = TGT_LTR
        self.font_size = NEW_SIZE
        self.font = pygame.font.Font(None, int(self.font_size))
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.circle_center)

    def draw(self, window):
        pygame.draw.circle(window, self.circle_color, self.circle_center, self.circle_radius)
        window.blit(self.text_surface, self.text_rect)
    
    def get_radius_from_list(self, move_count):
        if 0 <= move_count < len(self.radii):
            xy_mod = self.xy_trim[move_count]
            return self.radii[move_count], xy_mod
        else:
            raise IndexError(f"Move count {move_count} is out of range. Valid range is 0 to {len(self.radii) - 1}.")     


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
        try:
            self.rectangle_marker.move_mkr(left_pressed, right_pressed, window_width, window_height)
        except AttributeError as e:
            print(f"AttributeError: {e}")
            print(f"Type of self.rectangle_marker: {type(self.rectangle_marker)}")
            print(f"Dir of self.rectangle_marker: {dir(self.rectangle_marker)}")
            raise

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


# --------------------------------------
#  Initialize Main
# --------------------------------------	

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Draw Text in Circle")

# Set up the display
window_size = (800, 600)
window_width = window_size[0]
window_height = window_size[1]
window = pygame.display.set_mode(window_size)


# Load background image
background_image = pygame.image.load("background.jpg").convert()

# Create an instance of marker
BLK_SIZE = 25
marker_color = (0, 255, 0)  # Example color (green)  

comb_marker = CompositeMarker((window_width // 2)-25, 55, BLK_SIZE, 10, 10, marker_color, window_size)
GAME_MARKER_MOVING = False # Target Circle is/not being displayed 

# Set up the interval timer
interval = 0.5  # 500ms in seconds
start_time = time.time()
# game_marker_flag = False

# morse_char_tgt = '' # Initialize morse_char_tgt -- set to "" as a guard
# Wont get used until GAME_MARKER_MOVING

# Update the display
window.blit(background_image, (0, 0))
pygame.display.flip()

# --------------------------------------
# Main loop
# --------------------------------------	

running = True
while running:
    elapsed_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print(f"Key pressed: {pygame.key.name(event.key)}")
            if event.key == pygame.K_RETURN: # Choose RETURN key to launch game marker
                if GAME_MARKER_MOVING is False:
                    morse_char_tgt = comb_marker.encoder.generate_random_character()
                    comb_marker.encode_character(morse_char_tgt)
                    GAME_MARKER_MOVING = True
                    #print('INIT GAME MARKER')

    # If the update interval has passed -- and GAME_MARKER needs updating
    if elapsed_time - start_time >= interval and GAME_MARKER_MOVING:    

        # encode current morse_char_tgt char into 'next' left/dot or right/dash
        move_done_flag, left_pressed, right_pressed = comb_marker.next_dot_dash()
        # next marker position based on left/right pressed; move_count++
        comb_marker.move_mkr(left_pressed, right_pressed, window.get_width(), window.get_height())
        move_count = comb_marker.rectangle_marker.move_count
        # next cicrcle marker radius and position
        try:
            radius, xy_mod = comb_marker.get_radius_from_list(move_count)
            # add corrected x/y offset to marker postions
            x_mod = xy_mod[0] + comb_marker.rectangle_marker.x
            y_mod = xy_mod[1] + comb_marker.rectangle_marker.y
        except IndexError as e:
            print(f"Error: {e}")
            _=input('hit any key to exit')
            pygame.quit() 

        # Clear the screen
        window.blit(background_image, (0, 0))

        comb_marker.set_circle_attributes(x_mod, y_mod, radius)
        comb_marker.set_font_attributes(morse_char_tgt, radius)  # radius determins font size
        comb_marker.draw_circle(window)

        # Update the display
        pygame.display.flip()
    
        if move_done_flag:  # if the game marker has reached its destination    
            GAME_MARKER_MOVING = False
            comb_marker.reset_marker() # Reset marker to starting position
            #print('WAIT FOR NEXT KEY PRESS')
        else:
            # reset the timer for next update
            start_time = elapsed_time
            #print('UPDATE INTERVAL')

# Quit Pygame
pygame.quit()        