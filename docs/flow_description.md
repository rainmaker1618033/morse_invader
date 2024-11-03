# Technical Diagrams

This document contains the technical diagrams representing the Morse Invader game architecture and flows.

## Application Flow Diagram

```mermaid
graph TD
    A[Start Game] --> B[MorseInvaderGame]
    
    B --> C[Initialize Components]
    C --> C1[GameConfig]
    C --> C2[GameState]
    C --> C3[initialize_pygame]
    C --> C4[initialize_game_objects]
    
    C4 --> D1[Player Marker]
    C4 --> D2[Game Marker]
    C4 --> D3[Score Keeper]
    C4 --> D4[Morse Interpreter]
    C4 --> D5[Code Player]
    C4 --> D6[Encoder]
    C4 --> D7[Marker Pause]
    
    B --> E[Game Loop]
    E --> F[Handle Input]
    F --> F1[handle_keydown]
    F --> F2[handle_keyup]
    
    F1 --> G1[LEFT Key]
    F1 --> G2[RIGHT Key]
    F1 --> G3[RETURN Key]
    F1 --> G4[R Key]
    
    G1 --> H1[handle_movement_key]
    G2 --> H1
    G3 --> H2[handle_return_key]
    G4 --> H3[handle_random_character]
    
    E --> I[update_game_marker]
    I --> I1[update_marker_visuals]
    I --> I2[reset_game_marker_position]
    
    E --> J[update_display]
    J --> J1[draw_morse_code]
    J --> J2[draw_interpreted_code]
    J --> J3[update_score]
    J --> J4[update_markers]
    
    H1 --> K1[Move Player Marker]
    H2 --> K2[Verify Morse Code]
    H3 --> K3[Generate New Target]
    
    K2 --> L1[Update Score]
    K2 --> L2[Reset State]
    
    K3 --> M1[Set New Target]
    K3 --> M2[Play Sound]
    K3 --> M3[Reset Markers]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
    
    classDef init fill:#ddf,stroke:#333,stroke-width:1px
    classDef input fill:#fdd,stroke:#333,stroke-width:1px
    classDef update fill:#dfd,stroke:#333,stroke-width:1px
    classDef action fill:#ffd,stroke:#333,stroke-width:1px
    
    class C,C1,C2,C3,C4 init
    class F,F1,F2,G1,G2,G3,G4 input
    class I,I1,I2,J,J1,J2,J3,J4 update
    class H1,H2,H3,K1,K2,K3,L1,L2,M1,M2,M3 action
```

### Color Legend

- 🟣 Pink (Main Entry Points): Primary system entry points
- 🔵 Light Blue (Initialization): System initialization processes
- 🔴 Light Red (Input): Input handling processes
- 🟢 Light Green (Updates): State update processes
- 🟡 Light Yellow (Actions): Game actions and responses

### Flow Description

1. **Initialization Phase**
   - Game starts and initializes core components
   - Sets up configuration and game state
   - Initializes PyGame and game objects

2. **Game Loop Phase**
   - Handles continuous input processing
   - Updates game marker positions
   - Manages display updates
   - Processes game logic

3. **Input Processing**
   - Processes keyboard inputs (LEFT, RIGHT, RETURN, R)
   - Triggers appropriate game actions
   - Updates game state based on input

4. **Update Phase**
   - Updates marker positions
   - Updates visual elements
   - Updates game state
   - Updates display

5. **Action Phase**
   - Executes game actions based on input
   - Updates scores
   - Resets states as needed
   - Generates new targets

## Source Code

The source for these diagrams is maintained in the Mermaid format. To modify these diagrams:

1. Edit the Mermaid code within the ```mermaid blocks
2. Preview changes using the Mermaid Live Editor: [https://mermaid.live](https://mermaid.live)
3. Update this document with the verified changes

For more complex changes, consider using the Mermaid CLI:
```bash
mmdc -i diagrams.md -o output.png
```