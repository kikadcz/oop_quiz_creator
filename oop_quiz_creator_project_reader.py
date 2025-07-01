import random
import pygame
from colorama import init, Fore
import re
from typing import List, Dict, Optional

init(autoreset=True)


class QuizPlayer:
    def __init__(self, filename: str = "quiz_questions.txt"):
        self.filename = filename
        self.correct_sound = None
        self.wrong_sound = None
        self.questions = []

        pygame.mixer.init(44100, -16, 2, 2048)
        self._load_sounds()
        self._parse_quiz()

    def _load_sounds(self):
        try:
            self.correct_sound = pygame.mixer.Sound("correct.wav")
            self.wrong_sound = pygame.mixer.Sound("wrong.wav")

            self.correct_sound.set_volume(0.5)
            self.wrong_sound.set_volume(0.5)

        except Exception as error:
            print(f"{Fore.RED}Sound Error: {error}")
            self.correct_sound = None
            self.wrong_sound = None

    def play_sound(self, sound_type: str):

        if sound_type == "correct":
            if self.correct_sound:
                try:
                    self.correct_sound.play()
                except pygame.error as e:
                    print(f"{Fore.YELLOW}Error playing correct sound: {e}")
        elif sound_type == "wrong":
            if self.wrong_sound:
                try:
                    self.wrong_sound.play()
                except pygame.error as e:
                    print(f"{Fore.YELLOW}Error playing wrong sound: {e}")

