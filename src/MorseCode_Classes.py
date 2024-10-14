import pygame
import numpy as np
import pyaudio
import time


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
        self.answer_color = (165, 42, 42)  # BROWN
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
            self.answer_color = (165, 42, 42)  # BROWN
        else:
            self.letter_message = f'Unknown Morse Code: {self.morse_code}'
            self.answer = False
            self.answer_color = (255, 0, 0)  # RED

        # Print to debug
        # print(f'Clearing morse_code: {self.morse_code}')
        
        # clear the accumlated dot dash string
        self.morse_code = ""

    def check_valid_morse_code(self):
        """
        Check if the current Morse code input is valid.
        Returns:
            bool: True if the current Morse code is valid, False otherwise.
        """
        # Print to debug
        # print(f'Checking morse_code: {self.morse_code}')

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
        """
        Initialize the MorseCodeEncoder with a Morse code dictionary and reset state.

        Sets up the Morse code dictionary and initializes the current_code to an empty string
        and current_index to 0.
        """
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
        """
        Select a character and set the current Morse code sequence for encoding.

        Args:
            char (str): The character to be converted to Morse code.

        Raises:
            ValueError: If the character is not found in the Morse code dictionary.

        Returns:
            None
        """
        if char in self.morse_code:
            self.current_code = self.morse_code[char]
            self.current_index = 0
        else:
            raise ValueError(f"Character not found in Morse code dictionary: {char}")

    def next_dot_dash(self):
        """
        Return the next dot or dash in the current Morse code sequence.

        Returns:
            tuple: A tuple containing:
                - done_flag (bool): True if this is the last element in the sequence, False otherwise.
                - left_press (bool): True for a dot, False for a dash.
                - right_press (bool): True for a dash, False for a dot.

        Raises:
            IndexError: If there are no more dots or dashes to return.
            ValueError: If an unexpected character is encountered in the Morse code sequence.

        Example:
            >>> encoder = MorseCodeEncoder()
            >>> encoder.select_character('A')
            >>> encoder.next_dot_dash()
            (False, True, False)  # Returns a dot
            >>> encoder.next_dot_dash()
            (True, False, True)   # Returns a dash and signals end of sequence
        """
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
        """
        Reset the current index to 0.

        This method allows restarting the encoding process for the current character
        without selecting a new character.

        Returns:
            None
        """
        self.current_index = 0

### END OF CLASS -  MorseCodeEncoder ###