import pygame
import numpy as np

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
        # pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        # now draw a cicle instead of a square
        pygame.draw.circle(surface, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
        #print('MARKER DRAW NOW')

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
        """
        Initialize the CircleMarker with default values.

        Args:
            window_size (tuple): The size of the Pygame window (width, height).

        Note:
            This method sets up default values for the circle and text attributes.
            The circle is initially placed at the center of the window with a red color,
            and the text is set to "_" with white color.
        """
        self.window_size = window_size
        self.circle_center = [window_size[0] // 2, window_size[1] // 2]
        self.circle_radius = 100
        self.circle_color = (255, 0, 0)  # Red
        self.font_size = 50
        self.font_color = (255, 255, 255)  # White
        self.text = "_"  # Unknown character guard
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.circle_center)

    def set_circle_attributes(self, x, y, radius):
        """
        Set the attributes of the circle.

        Args:
            x (int): The x-coordinate of the circle center.
            y (int): The y-coordinate of the circle center.
            radius (int): The radius of the circle in pixels.

        Note:
            This method updates the circle's position and size. It does not
            update the text position, which should be done separately if needed.
        """
        self.circle_center = [x, y]
        self.circle_radius = radius

    def set_font_attributes(self, target_letter, new_size):
        """
        Set the attributes of the font and update the text.

        Args:
            target_letter (str): The text to be displayed inside the circle.
            new_size (int): The new size of the font in pixels.

        Note:
            This method updates the text content and font size, and recreates
            the text surface and rectangle to reflect these changes.
        """
        self.text = target_letter
        self.font_size = new_size
        self.font = pygame.font.Font(None, int(self.font_size))
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.circle_center)

    def draw(self, window):
        """
        Draw the circle and the text on the Pygame window.

        Args:
            window (pygame.Surface): The Pygame window surface to draw on.

        Note:
            This method draws the circle first, then blits the text surface
            onto the window at the position specified by text_rect.
        """
        pygame.draw.circle(window, self.circle_color, self.circle_center, self.circle_radius)
        window.blit(self.text_surface, self.text_rect)
        
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