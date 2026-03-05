# Impostor CLI
### Video Demo:  <https://youtube.com/shorts/8q738YZ1XRA?feature=share>
### Description:

Impostor CLI is a local multiplayer social deduction game built entirely for the terminal. Designed to be played with a group of friends (ranging from 3 to 15 players) sharing a single computer, the game transforms a standard command-line interface into a highly interactive and suspenseful party game. 

At the start of a match, players configure the game's language (English or Spanish), the difficulty level, and the duration of the debate phase [4, 5]. Once the setup is complete, the game uses a seamless "Pass & Play" mechanic. One player is secretly and randomly assigned the role of the "Impostor", while the rest become "Citizens". 

All Citizens are given a secret word that they must discuss, but the Impostor is left completely in the dark. The Citizens' goal is to figure out who the Impostor is through deductive reasoning and debate, without making the secret word too obvious. The Impostor's goal is to blend in, pretend they know the word, and survive until the time runs out.

## File Breakdown

The project was built using a modular architecture to separate the game logic, the user interface, the data management, and the asynchronous tasks. Here is a detailed breakdown of what each file contains and does:

*   **`main.py`**: This is the entry point of the application. It contains the global application loop that allows players to restart the game without exiting the terminal. More importantly, it houses the core State Machine that dictates the flow of the game, handling transitions between states such as `ESTADO_INICIO` (Start), `ESTADO_SETUP` (Setup), `ESTADO_REPARTO` (Role Distribution), `ESTADO_DEBATE` (Debate), `ESTADO_VOTACION` (Voting), and `ESTADO_FIN` (End).
*   **`game.py`**: This file contains the business logic of the application. It defines the `Game` class, which holds the current match settings, and the `Player` class, which tracks each user's name, role ("citizen" or "impostor"), and alive status. It handles the randomized assignment of roles and ensures that the player constraints (minimum 3, maximum 15) are respected.
*   **`ui.py`**: Dedicated entirely to the visual presentation. It uses the `colorama` library to render the "Retro Arcade" aesthetic, utilizing specific color palettes (e.g., Cyan for borders, Red for the Impostor, Blue for Citizens). It also contains the OS-level screen-clearing functions crucial for hiding sensitive information between turns.
*   **`timer.py`**: Contains the `DebateTimer` class, which inherits from Python's native `threading.Thread`. It manages the live background countdown during the debate phase, updating the terminal output dynamically while the main thread waits for user input.
*   **`data_manager.py`**: A utility module containing parser functions like `load_json()` and `load_csv()` to cleanly import external data into the game's memory.
*   **`texts.json` & `words.csv`**: External data files. The JSON file acts as an internationalization (i18n) dictionary holding all the string values for English and Spanish. The CSV file acts as the database for the secret words, categorized by language and difficulty.

## Design Choices

During the development of Impostor CLI, several technical challenges required specific design choices to ensure a smooth user experience:

**1. Multithreading for the Timer**
One of the biggest hurdles in building a terminal-based game is that the standard `input()` function blocks the execution of the program. I wanted the players to see a live countdown ticking down on the screen while still having the ability to type a command to call an "Emergency Meeting".
To solve this, I debated using `time.sleep()` in a loop, but it wouldn't allow simultaneous input. I opted to use the `threading` module, running the `DebateTimer` on a secondary thread that flushes the terminal line with the remaining time, leaving the main thread free to listen for the "M" (Meeting) keystroke.

**2. State Machine Architecture**
Instead of using deeply nested `while` loops that would make the code unreadable, I implemented a State Machine in `main.py` . This choice was crucial because the game flow isn't strictly linear. For instance, during the `ESTADO_VOTACION` (Voting Phase), if the players vote out an innocent Citizen, the game must pause the timer, process the elimination, and seamlessly transition back to the `ESTADO_DEBATE` (Debate Phase) with the exact remaining time. A state machine handles this complex routing.

**3. Strict "Pass & Play" Privacy**
Because 3 to 15 people are looking at the same screen, privacy was paramount. I debated how to hide previous terminal outputs. I chose to use Python's `os` module to detect the operating system and execute the native terminal clear commands (`cls` for Windows, `clear` for Mac/Linux). Combined with explicit "Press Enter to reveal" and "Press Enter to hide" transition screens, this completely secures the Impostor's identity.

**4. Internationalization (i18n) vs. Hardcoding**
To make the game accessible, I wanted to support both English and Spanish. I designed a JSON-based dictionary approach. The game simply looks up keys like `lang_texts['debate_title']`, making the Python code clean and allowing me to potentially add dozens of new languages in the future just by updating a single JSON file.


