# Radicchio Kitchens: Employee Training Module

## Overview
Radicchio Kitchens is a First-Person Chef/Horror Simulator designed as an employee training module. Players take on the role of a chef in a high-pressure kitchen environment, tasked with prepping ingredients while managing their sanity. As the pressure mounts and sanity slips, the game transitions into a psychological horror experience, testing the player's ability to maintain composure under duress.

## Features
-   **Prep Mode**: Slice ingredients to earn score. Accuracy and timing are key.
-   **Trauma Mode**: When sanity drops, players enter a "nerve path" minigame where they must trace a path without deviating to avoid injury.
-   **Sanity System**: Missing ingredients or failing the trauma minigame reduces sanity.
-   **Progressive Visuals**: As the player fails, the game's visuals (specifically the chef's left hand) deteriorate, reflecting the physical and mental toll.
-   **Dynamic Feedback**: Visual and audio cues provide immediate feedback on slicing accuracy and game state.

## Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Vargr013/Radicchio-Kitchens-.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Radicchio-Kitchens-
    ```
3.  **Install dependencies:**
    Ensure you have Python installed. The game relies on `pygame`.
    ```bash
    pip install pygame
    ```

## Usage
Run the game using Python:
```bash
python main.py
```

## Controls
-   **Mouse Movement**: Move the knife/cursor.
-   **Left Click (Hold)**: Slice through ingredients.
-   **Mouse Follow**: In Trauma Mode, carefully follow the white nerve path.

## Project Structure
-   `main.py`: Entry point of the application. Handles the main game loop.
-   `settings.py`: Configuration file for game constants, colors, and asset paths.
-   `sprites.py`: Contains sprite classes for `ChefHand`, `Cursor`, `Ingredient`, and `NervePath`.
-   `state_manager.py`: Manages game states (`PREP`, `TRAUMA`), scoring, sanity, and logic updates.
-   `assets/`: Directory for game assets (images, sounds).

## License
This project is for educational purposes.
