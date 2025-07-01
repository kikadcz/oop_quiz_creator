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
            print(Fore.RED + ascii_art)
        except Exception as e:
            print(Fore.RED + f"Error generating ASCII art: {str(e)}")

    def init_sound(self):
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 2048)

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
            self.bong_sound.set_volume(0.5)
        except Exception as e:
            print(Fore.YELLOW + f"Warning: Could not load bong sound: {str(e)}")

    def cleanup(self):
        if hasattr(self, 'bong_sound'):
            del self.bong_sound
        pygame.mixer.quit()

    def get_question_and_choices(self):
        print("Type 'exit' to quit.")
        question = input(Fore.GREEN + "Enter your quiz question: ")
        if question.lower() == 'exit':
            return None

        choices = {}
        for letter in ['a', 'b', 'c', 'd']:
            choices[letter] = input(f"{Fore.CYAN}Choice {letter}: ")

        while True:
            correct_answer = input(Fore.LIGHTMAGENTA_EX + "Correct answer: ").lower()
            if correct_answer in ['a', 'b', 'c', 'd']:
                break
            print(Fore.RED + "Please enter a, b, c, or d.")

        return {
            'question': question,
            'choices': choices,
            'correct_answer': correct_answer
        }

    def save_to_file(self, data):
        try:
            with open(self.filename, "a", encoding='utf-8') as file:
                file.write(f"\nQuestion:\n{data['question']}\n")
                for letter, choice in data['choices'].items():
                    file.write(f"({letter}) {choice}\n")
                file.write(f"\nAnswer: {data['correct_answer']}\n{'-' * 30}\n")

            if self.bong_sound:
                self.bong_sound.play()

        except IOError as e:
            print(Fore.RED + f"Error saving to file: {str(e)}")

    def run(self):
        self.print_header()

        try:
            while True:
                data = self.get_question_and_choices()
                if data is None:
                    print(Fore.YELLOW + "Thanks for using Quizzatron 3000!")
                    break

                self.save_to_file(data)
                print(Fore.GREEN + "Question saved successfully.")
        finally:
            self.cleanup()


if __name__ == "__main__":
    creator = QuizCreator()
    creator.run()