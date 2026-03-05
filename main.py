import time
from game import Game
from data_manager import load_csv, load_json
from ui import (
    print_splash_screen, print_language_menu, print_difficulty_menu,
    print_transition_screen, print_role_screen, print_debate_screen, 
    print_voting_screen, print_end_screen, print_time_menu, clear_screen
)
from timer import DebateTimer

def main():
    # Load raw data
    texts = load_json('texts.json')

# --- GLOBAL APP LOOP FOR RF5.2 (RESTART MECHANISM) ---
    while True:
        game = Game()
        
        # --- ESTADO_INICIO ---
        print_splash_screen()
        
        # Language Selection
        while True:
            print_language_menu()
            lang_choice = input(">> ").strip()
            if lang_choice == "1":
                game.language = "es"
                break
            elif lang_choice == "2":
                game.language = "en"
                break
                
        lang_texts = texts[game.language]
        
        # Difficulty Selection
        while True:
            print_difficulty_menu(lang_texts)
            diff_choice = input(">> ").strip()
            if diff_choice == "1":
                game.difficulty = "easy"
                break
            elif diff_choice == "2":
                game.difficulty = "medium"
                break
            elif diff_choice == "3":
                game.difficulty = "hard"
                break
                
        # Time Selection
        while True:
            print_time_menu(lang_texts)
            time_choice = input(">> ").strip()
            if time_choice == "1":
                game.debate_duration = 180  # 3 minutes in seconds
                break
            elif time_choice == "2":
                game.debate_duration = 300  # 5 minutes in seconds
                break
            elif time_choice == "3":
                game.debate_duration = 600  # 10 minutes in seconds
                break
            elif time_choice == "4":
                game.debate_duration = 0    # 0 means infinite/no time
                break

        # Load words based on selected language and difficulty
        words = load_csv('words.csv', game.language, game.difficulty)
        
        # --- ESTADO_SETUP ---
        game.state = "ESTADO_SETUP"
        print(f"\n--- {lang_texts['menu_lang']} ---") # Using as generic header
        
        while True:
            # Prompt for player name
            name = input(f"\n{lang_texts['setup_enter_name']} ")
            
            # If user presses Enter without typing, try to start the game
            if not name.strip():
                if game.can_start():
                    break
                else:
                    print(lang_texts['err_min'])
                    continue
                    
            # Attempt to add player and show corresponding message from texts.json
            success, msg_key = game.add_player(name)
            print(lang_texts[msg_key])

        # Start Game Logic
        if game.setup_match(words):
            # --- ESTADO_REPARTO ---
            for player in game.players:
                print_transition_screen(player.name, lang_texts)
                print_role_screen(player, game.secret_word, lang_texts)
                
            print(f"\n{lang_texts['setup_finished']}")
            time.sleep(2)
            
            game.state = "ESTADO_DEBATE"
            winner = None

            #Keep track of the remaining time across voting sessions
            debate_time = game.debate_duration
            
            # --- MAIN GAME LOOP ---
            while game.state != "ESTADO_FIN":
                
                if game.state == "ESTADO_DEBATE":
                    print_debate_screen(game.players, lang_texts)
                    
                    # Check if playing with a time limit
                    if debate_time > 0:
                        timer = DebateTimer(duration_seconds=debate_time, texts=lang_texts)
                        timer.start()
                        
                        while timer.running:
                            comando = input().strip().lower()
                            if comando in ['r', 'm']:
                                timer.stop()
                                debate_time = timer.remaining 
                                game.state = "ESTADO_VOTACION"
                                break
                                
                        if timer.time_up:
                            game.state = "ESTADO_FIN"
                            winner = "impostor"
                    else:
                        # Playing with NO time limit
                        while True:
                            comando = input().strip().lower()
                            if comando in ['r', 'm']:
                                game.state = "ESTADO_VOTACION"
                                break
                
                elif game.state == "ESTADO_VOTACION":
                    alive_players = print_voting_screen(game.players, lang_texts)
                    
                    try:
                        opcion = int(input(f"{lang_texts['vote_select']} "))
                        if 1 <= opcion <= len(alive_players):
                            # Get the selected player and eliminate them
                            selected = alive_players[opcion - 1]
                            selected.alive = False 
                            
                            # Check if the eliminated player was the impostor
                            if selected.role == "impostor":
                                print(f"\n>> {selected.name} {lang_texts['vote_was_impostor']}")
                                winner = "citizens"
                                game.state = "ESTADO_FIN"
                            else:
                                print(f"\n>> {selected.name} {lang_texts['vote_was_not_impostor']}")
                                
                                # Check if there are any citizens left alive
                                alive_citizens = [p for p in game.players if p.role == "citizen" and p.alive]
                                
                                if len(alive_citizens) == 0:
                                    # No citizens left, impostor survives and wins
                                    winner = "impostor"
                                    game.state = "ESTADO_FIN"
                                else:
                                    # Citizens still alive, continue game
                                    game.state = "ESTADO_DEBATE"
                            
                            # pause to read the result
                            time.sleep(3) 
                        else:
                            print(lang_texts['err_out_of_range'])
                            time.sleep(1)
                    except ValueError:
                        print(lang_texts['err_invalid_number'])
                        time.sleep(1)
                        
            # --- ESTADO_FIN ---
            impostor = next(p for p in game.players if p.role == "impostor")
            print_end_screen(winner, impostor.name, game.secret_word, lang_texts)
        
        # --- RF5.2 IMPLEMENTATION: RESTART OPTION ---
            play_again = input(f"\n{lang_texts['end_play_again']} ").strip().lower()
            if play_again == 'q':
                clear_screen()
                break

if __name__ == "__main__":
    main()


'''
AI Assistance Disclaimer:
This project incorporates concepts and suggestions generated through NotebookLM. The Gemini AI model served as a technical consultant to ensure the desired architecture, specific libraries, and general best practices.
'''