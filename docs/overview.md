# Morse Invader Game

A Python-based educational game that helps players learn Morse code through an interactive space-invader style interface.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
  - [Class Structure](#class-structure)
  - [Game Flow](#game-flow)
  - [Component Interaction](#component-interaction)
- [Installation](#installation)
- [Game Components](#game-components)
- [How to Play](#how-to-play)
- [Configuration](#configuration)
- [Class Documentation](#class-documentation)

## Overview

Morse Invader is an educational game that combines classic arcade-style gameplay with Morse code learning. Players must match Morse code patterns displayed by a moving marker, making it an engaging way to learn and practice Morse code.

## Architecture

### Class Structure

```mermaid
classDiagram
    MorseInvaderGame *-- GameConfig
    MorseInvaderGame *-- GameState
    MorseInvaderGame *-- RectangleMarker
    MorseInvaderGame *-- CompositeMarker
    MorseInvaderGame *-- ScoreKeeper
    MorseInvaderGame *-- MorseCodeInterpreter
    MorseInvaderGame *-- MorseCodePlayer
    MorseInvaderGame *-- MorseCodeEncoder
    MorseInvaderGame *-- MarkerPause

    class MorseInvaderGame{
        -GameConfig config
        -GameState state
        -initialize_pygame()
        -initialize_game_objects()
        -handle_input()
        -update_game_marker()
        -update_display()
        +run()
    }

    class GameConfig{
        +WINDOW_SIZE: Tuple
        +BLOCK_SIZE: int
        +MARKER_COLOR: Tuple
        +TEXT_COLOR: Tuple
        +FONT_SIZE: int
        +UPDATE_INTERVAL: float
        +FPS: int
    }

    class GameState{
        +player_moving: bool
        +game_marker_moving: bool
        +left_pressed: bool
        +right_pressed: bool
        +morse_char_target: str
        +last_update_time: float
        +reset_movement()
    }
```

### Game Flow

```mermaid
stateDiagram-v2
    [*] --> Initialize: Start Game
    Initialize --> WaitingForInput: Game Ready
    
    WaitingForInput --> GenerateTarget: Press R
    GenerateTarget --> DisplayPattern: Show Morse Pattern
    DisplayPattern --> WaitingForInput: Pattern Complete
    
    WaitingForInput --> PlayerInput: Arrow Keys
    PlayerInput --> CodeValidation: Press Enter
    
    CodeValidation --> ScoreUpdate: Check Match
    ScoreUpdate --> WaitingForInput: Update Score
    
    WaitingForInput --> [*]: Quit Game
```

### Component Interaction

```mermaid
flowchart TB
    Player[Player Input] --> InputHandler[Input Handler]
    InputHandler --> MorseInterpreter[Morse Interpreter]
    InputHandler --> PlayerMarker[Player Marker]
    
    RandomGen[Random Generator] --> GameMarker[Game Marker]
    GameMarker --> Pattern[Pattern Display]
    
    MorseInterpreter --> Validator[Code Validator]
    PlayerMarker --> Validator
    Pattern --> Validator
    
    Validator --> ScoreKeeper[Score Keeper]
    Validator --> SoundPlayer[Sound Player]
    
    subgraph Game Loop
        InputHandler
        Pattern
        Validator
        ScoreKeeper
    end
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/morse-invader.git
cd morse-invader
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python morse_invader.py
```

## Game Components

The game consists of several key components:

- **Player Marker**: A controllable marker that players use to input Morse code
- **Game Marker**: An automated marker that displays the target Morse code pattern
- **Score System**: Tracks correct and incorrect attempts
- **Morse Code Interpreter**: Converts player inputs into Morse code and validates them
- **Sound System**: Provides audio feedback for Morse code patterns

## How to Play

1. Press `R` to generate a random character target
2. Use `LEFT` and `RIGHT` arrow keys to create Morse code patterns:
   - `LEFT` for dots (.)
   - `RIGHT` for dashes (-)
3. Press `ENTER` to submit your answer
4. Match the pattern shown by the game marker to score points

## Configuration

The game's behavior can be customized through the `GameConfig` class:

```python
WINDOW_SIZE: (800, 600)    # Game window dimensions
BLOCK_SIZE: 25            # Size of game blocks
UPDATE_INTERVAL: 0.5      # Time between marker updates (seconds)
FPS: 30                   # Frames per second
```

## Class Documentation

### GameConfig

```python
@dataclass
class GameConfig:
```
Stores game configuration settings including window size, colors, and timing parameters.

#### Attributes
- `WINDOW_SIZE`: Tuple[int, int] - Window dimensions (width, height)
- `BLOCK_SIZE`: int - Size of game blocks
- `MARKER_COLOR`: Tuple[int, int, int] - RGB color for markers
- `TEXT_COLOR`: Tuple[int, int, int] - RGB color for text
- `FONT_SIZE`: int - Size of game font
- `UPDATE_INTERVAL`: float - Time between updates
- `FPS`: int - Frames per second

### GameState

```python
class GameState:
```
Manages the current state of the game.

#### Methods
- `__init__()`: Initializes game state variables
- `reset_movement()`: Resets all movement-related states

#### Attributes
- `player_moving`: bool - Indicates if player marker is moving
- `game_marker_moving`: bool - Indicates if game marker is moving
- `left_pressed`: bool - Left arrow key state
- `right_pressed`: bool - Right arrow key state
- `morse_char_target`: str - Current target character
- `last_update_time`: float - Timestamp of last update

### MorseInvaderGame

```python
class MorseInvaderGame:
```
Main game class that coordinates all game components and handles the game loop.

#### Key Methods
- `initialize_pygame()`: Sets up Pygame environment
- `initialize_game_objects()`: Creates game objects
- `handle_input()`: Processes user input
- `update_game_marker()`: Updates game marker position
- `update_display()`: Refreshes game display
- `run()`: Main game loop
