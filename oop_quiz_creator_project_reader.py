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

    def cleanup(self):
        if hasattr(self, 'correct_sound'):
            del self.correct_sound
        if hasattr(self, 'wrong_sound'):
            del self.wrong_sound
        pygame.mixer.quit()

    def run(self):
        if not self.questions:
            print(f"{Fore.YELLOW}No questions available!")
            return

        random.shuffle(self.questions)
        score = 0

        try:
            for question_number, question in enumerate(self.questions, 1):
                print(f"\n{Fore.YELLOW}Question {question_number}: {question['text']}")
                for option_letter, option_text in question['options'].items():
                    print(f"({option_letter}) {option_text}")

                while True:
                    answer = input("Your answer (A/B/C/D): ").upper()
                    if answer in 'ABCD':
                        break
                    print(f"{Fore.RED}Invalid option!")

                if answer == question['correct']:
                    print(f"{Fore.GREEN}Correct!")
                    self.play_sound("correct")
                    score += 1
                else:
                    print(f"{Fore.RED}Wrong! The correct answer was {question['correct']}")
                    self.play_sound("wrong")

            print(f"{Fore.MAGENTA}\nQuiz Finished! Final Score: {score}/{len(self.questions)}")

        finally:
            self.cleanup()

