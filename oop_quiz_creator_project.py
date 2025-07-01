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

    def init_sound(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("bg_music.mp3")
            pygame.mixer.music.play(-1)
            self.bong_sound = pygame.mixer.Sound("bong.wav")
        except Exception as audio_error:
            print(Fore.RED + f"\nWarning: Sound initialization failed ({str(audio_error)}). "
                             "Continuing without sound effects.")