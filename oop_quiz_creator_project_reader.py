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