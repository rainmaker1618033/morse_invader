import pygame
import numpy as np

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
        """
        Draw the marker on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the marker on.
        """
        # pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        # now draw a cicle instead of a square
        pygame.draw.circle(surface, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
        #print('MARKER DRAW NOW')

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


### END OF CLASS -  RectangleMarker ###

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
        self.circle_radius = 10
        self.circle_color = (255, 0, 0)
        self.font_size = 10
        self.font_color = (255, 255, 255)
        self.text = "."  # unknown character guard
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


### END OF CLASS -  CircleMarker ###


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
        self.player_score = 0
        self.game_score = 0
        self.font = font
        self.window_width = window_width
        self.window_height = window_height

    def increment_player_score(self):
        self.player_score += 1

    def increment_game_score(self):
        self.game_score += 1

    def display_score(self, window):
        score_text = f"Match: {self.player_score}  Miss: {self.game_score}"
        score_surface = self.font.render(score_text, True, (0, 0, 255))
        score_rect = score_surface.get_rect(center=(self.window_width // 2, (self.window_height - 200) // 2))
        window.blit(score_surface, score_rect)

### END OF CLASS -  ScoreKeeper ###