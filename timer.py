import threading
import time
import sys
from colorama import Fore, Style

class DebateTimer(threading.Thread):
    def __init__(self, duration_seconds, texts):
        super().__init__()
        self.remaining = duration_seconds
        self.running = False
        self.time_up = False
        self.texts = texts 

    def run(self):
        self.running = True
        while self.running and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            
            # yellow default, red last 30 seconds
            color = Fore.RED if self.remaining <= 30 else Fore.YELLOW
            
            # \r sobrescribe la línea actual en la terminal
            sys.stdout.write(f"\r{self.texts['debate_time_left']} [ {color}{time_str}{Style.RESET_ALL} ]    ")
            sys.stdout.flush()
            
            time.sleep(1)
            self.remaining -= 1

        if self.remaining <= 0:
            self.time_up = True
            self.running = False
            sys.stdout.write(f"\r{self.texts['debate_time_left']} [ {Fore.RED}00:00{Style.RESET_ALL} ]    \n")
            sys.stdout.flush()

    def stop(self):
        self.running = False

'''
AI Assistance Disclaimer:
This project incorporates concepts and suggestions generated through NotebookLM. The Gemini AI model served as a technical consultant to ensure the desired architecture, specific libraries, and general best practices.
'''