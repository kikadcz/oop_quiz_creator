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
        pygame.mixer.quit()  # Ensure mixer is stopped
        pygame.mixer.init(44100, -16, 2, 2048)  # Initialize with proper parameters

        music_files = ["bg_music.ogg", "bg_music.mp3"]
        loaded = False

        for music_file in music_files:
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)
                print(Fore.GREEN + f"Successfully loaded background music from {music_file}")
                loaded = True
                break
            except Exception as e:
                print(Fore.YELLOW + f"Warning: Could not load {music_file}: {str(e)}")

        try:
            self.bong_sound = pygame.mixer.Sound("bong.wav")
            self.bong_sound.set_volume(0.5)  # Set reasonable volume
        except Exception as e:
            print(Fore.YELLOW + f"Warning: Could not load bong sound: {str(e)}")

    def cleanup(self):
        """Clean up resources when program exits"""
        if hasattr(self, 'bong_sound'):
            del self.bong_sound
        pygame.mixer.quit()

    def get_question_and_choices(self):
        print("Type 'exit' to quit.")
        question = input(Fore.GREEN + "Enter your quiz question: ")
        if question.lower() == 'exit':
            return None

