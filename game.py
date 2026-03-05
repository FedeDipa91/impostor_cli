import random

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.alive = True

class Game:
    def __init__(self):
        self.state = "ESTADO_INICIO"
        self.players = []
        self.language = "es"
        self.difficulty = "easy"
    
    def add_player(self, name):
        name = name.strip()

        if not name:
            return False, "err_empty"
        if len(self.players) > 15:
            return False, "err_max"
        if any(p.name.lower() == name.lower()for p in self.players):
            return False, "err_dup"
        
        self.players.append(Player(name, "unassigned"))
        return True, "msg_player_added"
    
    def can_start(self):
        return len(self.players) >= 3
    
    def setup_match(self, words_list):
        #Security measure, don't start if not min_players
        if not self.can_start():
            return False

        #Select random word from list
        self.secret_word =random.choice(words_list)

        # All citizen by default
        for player in self.players:
            player.role = "citizen"

        # Pick random impostor
        impostor_player = random.choice(self.players)
        impostor_player.role = "impostor"

        # Move state to role assigments
        self.state = "ESTADO_REPARTO"
        return True
    
'''
AI Assistance Disclaimer:
This project incorporates concepts and suggestions generated through NotebookLM. The Gemini AI model served as a technical consultant to ensure the desired architecture, specific libraries, and general best practices.
'''