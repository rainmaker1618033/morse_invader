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
        pygame.draw.circle(surface, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

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