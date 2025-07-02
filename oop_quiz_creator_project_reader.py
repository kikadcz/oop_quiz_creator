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

    def _parse_quiz(self):
        try:
            with open(self.filename, encoding="utf-8") as quiz_file:
                question_blocks = quiz_file.read().strip().split('-' * 30)

                for block_index, question_block in enumerate(question_blocks):
                    if not question_block.strip():
                        continue

                    lines_in_block = question_block.strip().split('\n')
                    question_text = None
                    answer_choices = {}

                    for line_index, line_text in enumerate(lines_in_block):
                        if line_text.strip().lower().startswith("question:"):
                            if line_index + 1 < len(lines_in_block):
                                question_text = lines_in_block[line_index + 1].strip()
                            break

                    if not question_text:
                        print(f"{Fore.YELLOW}Warning: Missing question text in block {block_index}")
                        continue

                    for line_text in lines_in_block:
                        option_match = re.match(r'\(([a-dA-D])\)\s+(.+)', line_text.strip())
                        if option_match:
                            option_letter = option_match.group(1).upper()
                            option_content = option_match.group(2).strip()
                            answer_choices[option_letter] = option_content

                    for expected_letter in 'ABCD':
                        if expected_letter not in answer_choices:
                            print(f"{Fore.YELLOW}Warning: Missing option {expected_letter} in question block {block_index}")
                            answer_choices[expected_letter] = ""

                    correct_answer_match = re.search(r'Answer:\s*([a-dA-D])', question_block)
                    if not correct_answer_match:
                        print(f"{Fore.YELLOW}Warning: Missing correct answer in question block {block_index}")
                        continue

                    correct_answer = correct_answer_match.group(1).upper()

                    self.questions.append({
                        'text': question_text,
                        'options': answer_choices,
                        'correct': correct_answer
                    })

                print(f"{Fore.CYAN}Loaded {len(self.questions)} question(s) from '{self.filename}'")

        except FileNotFoundError:
            print(f"{Fore.RED}Error: Quiz file '{self.filename}' not found")
        except Exception as error:
            print(f"{Fore.RED}Error parsing quiz file: {error}")

    def play_sound(self, sound_type: str):
        if sound_type == "correct" and self.correct_sound:
            try:
                self.correct_sound.play()
            except pygame.error as play_error:
                print(f"{Fore.YELLOW}Error playing correct sound: {play_error}")
        elif sound_type == "wrong" and self.wrong_sound:
            try:
                self.wrong_sound.play()
            except pygame.error as play_error:
                print(f"{Fore.YELLOW}Error playing wrong sound: {play_error}")

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
        user_score = 0

        try:
            for question_number, quiz_question in enumerate(self.questions, 1):
                print(f"\n{Fore.YELLOW}Question {question_number}: {quiz_question['text']}")
                for option_key, option_value in quiz_question['options'].items():
                    print(f"({option_key}) {option_value}")

                while True:
                    user_answer = input("Your answer (A/B/C/D): ").strip().upper()
                    if user_answer in 'ABCD':
                        break
                    print(f"{Fore.RED}Invalid option! Try again")

                if user_answer == quiz_question['correct']:
                    print(f"{Fore.GREEN}Correct!")
                    self.play_sound("correct")
                    user_score += 1
                else:
                    print(f"{Fore.RED}Wrong! The correct answer was {quiz_question['correct']}")
                    self.play_sound("wrong")

            print(f"{Fore.MAGENTA}\nQuiz Finished! Final Score: {user_score}/{len(self.questions)} ")

        finally:
            self.cleanup()


if __name__ == "__main__":
    print(f"{Fore.LIGHTBLUE_EX}\nWelcome to Quizzatron 3000: Game Saga")
    quiz_game = QuizPlayer()
    try:
        quiz_game.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTRED_EX}Game interrupted by user! Rage quit detected")
    finally:
        quiz_game.cleanup()
