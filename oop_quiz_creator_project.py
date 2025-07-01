import pygame
from colorama import init, Fore
import pyfiglet
import sys
import os

init(autoreset=True)

class QuizCreator:
    def __init__(self):
        self.bong_sound = None
        self.filename = "quiz_questions.txt"
        self.init_sound()

    def print_header(self):
        try:
            ascii_art = pyfiglet.figlet_format("QUIZZATRON 3000", font="doom", justify="left", width=240)
            print(Fore.RED + "QUIZZATRON 3000")
            print(f"Error generating ASCII art: {str(e)}")

