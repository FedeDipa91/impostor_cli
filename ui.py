import os
from colorama import init, Fore, Style

# Initialize colorama with autoreset to restore color after each print
init(autoreset=True)

def clear_screen():
    # Detect OS: use 'cls' for Windows, 'clear' for Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def format_title(text):
    # Apply CYAN and BRIGHT style as per visual guide
    return f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

# Screen visuals

def print_transition_screen(player_name, texts):
    clear_screen()
    print("-" * 50)
    print(f"{Fore.MAGENTA}{texts['transition_title']}{Style.RESET_ALL}")
    print("-" * 50)
    print(f"\n{texts['transition_pass_to']}")
    print(f">> {Fore.WHITE}{Style.BRIGHT}{player_name.upper()}{Style.RESET_ALL} <<\n")
    print(texts['transition_look_away'])
    
    # Pause until user presses ENTER
    input(f"\n{texts['transition_ready']}")

def print_role_screen(player, secret_word, texts):
    clear_screen()
    print("-" * 50)
    print(f"{texts['reveal_player']} {Fore.WHITE}{Style.BRIGHT}{player.name.upper()}{Style.RESET_ALL}")
    print("-" * 50)
    
    if player.role == "citizen":
        print(f"\n    {Fore.BLUE}{texts['reveal_citizen']}{Style.RESET_ALL}\n")
        print(texts['reveal_word'])
        print(f"> {Fore.YELLOW}{secret_word}{Style.RESET_ALL} <\n")
        print(texts['reveal_mission_citizen'])
    else:
        # Impostor doesn't receive the secret word
        print(f"\n    {Fore.RED}{texts['reveal_impostor']}{Style.RESET_ALL}\n")
        print(texts['reveal_mission_impostor'])
        
    print("-" * 50)
    input(f"\n{texts['reveal_hide']}")
    clear_screen()

def print_debate_screen(players, texts):
    clear_screen()
    print("=" * 50)
    print(f"{Fore.CYAN}        {texts['debate_title']}{Style.RESET_ALL}")
    print("=" * 50 + "\n")
    
    print(texts['debate_participants'])
    for player in players:
        if player.alive:
            # Alive players in green
            print(f"{Fore.GREEN} - {player.name}{Style.RESET_ALL}")
        else:
            # Eliminated players in red and dim
            print(f"{Fore.RED}{Style.DIM} - {player.name} {texts['debate_eliminated']}{Style.RESET_ALL}")
            
    print(f"\n{Fore.WHITE}{texts['debate_press_meeting']}{Style.RESET_ALL}\n")

def print_voting_screen(players, texts):
    clear_screen()
    print(f"{Fore.RED}{Style.BRIGHT}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}               {texts['vote_title']}{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}{texts['vote_who']}{Style.RESET_ALL}\n")
    
    # Only alive players can be voted for
    alive_players = [p for p in players if p.alive]
    
    for i, player in enumerate(alive_players, 1):
        print(f"{i}. {player.name}")
        
    print()
    return alive_players

def print_end_screen(winner, impostor_name, secret_word, texts):
    clear_screen()
    print("=" * 50)
    if winner == "impostor":
        print(f"      {Fore.RED}{Style.BRIGHT}{texts['end_game_impostor_won']}{Style.RESET_ALL}")
    else:
        print(f"      {Fore.GREEN}{Style.BRIGHT}{texts['end_game_citizens_won']}{Style.RESET_ALL}")
    print("=" * 50 + "\n")
    
    print(f"{texts['end_impostor_was']} {Fore.RED}{impostor_name.upper()}{Style.RESET_ALL}")
    print(f"{texts['end_word_was']} {Fore.YELLOW}{secret_word}{Style.RESET_ALL}\n")

def print_splash_screen():
    clear_screen()
    splash_art = f"""{Fore.CYAN}{Style.BRIGHT}\
***********************************************************************
*                                                                     *
* ██╗███╗   ███╗██████╗  ██████╗ ███████╗████████╗ ██████╗ ██████╗    *
* ██║████╗ ████║██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗   *
* ██║██╔████╔██║██████╔╝██║   ██║███████╗   ██║   ██║   ██║██████╔╝   *
* ██║██║╚██╔╝██║██╔═══╝ ██║   ██║╚════██║   ██║   ██║   ██║██╔══██╗   *
* ██║██║ ╚═╝ ██║██║     ╚██████╔╝███████║   ██║   ╚██████╔╝██║  ██║   *
* ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   *
*                                                                     *
* [ PRESS ENTER TO START ]                                            *
***********************************************************************{Style.RESET_ALL}"""
    
    print(splash_art)
    input()

def print_language_menu():
    clear_screen()
    # Hardcoded just for this screen since language is not selected yet
    print(f"{Fore.YELLOW}> SELECT LANGUAGE / SELECCIONAR IDIOMA{Style.RESET_ALL}")
    print("-" * 50)
    print("1. ESPAÑOL")
    print("2. ENGLISH\n")

def print_difficulty_menu(texts):
    clear_screen()
    print(f"{Fore.YELLOW}{texts['menu_diff']}{Style.RESET_ALL}")
    print("-" * 50)
    print(f"1. {texts['diff_easy']}")
    print(f"2. {texts['diff_medium']}")
    print(f"3. {texts['diff_hard']}\n")

def print_time_menu(texts):
    clear_screen()
    print(f"{Fore.YELLOW}{texts['menu_time']}{Style.RESET_ALL}")
    print("-" * 50)
    print(f"1. {texts['time_3m']}")
    print(f"2. {texts['time_5m']}")
    print(f"3. {texts['time_10m']}")
    print(f"4. {texts['time_none']}\n")


'''
AI Assistance Disclaimer:
This project incorporates concepts and suggestions generated through NotebookLM. The Gemini AI model served as a technical consultant to ensure the desired architecture, specific libraries, and general best practices.
'''