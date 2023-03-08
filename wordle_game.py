from colorama import init as cinit, deinit, Fore, Back
from colorama.ansi import clear_screen as cls, CSI
from random import choice


class Wordle():
    _filename = '/Users/andrejsemin/PycharmProjects/WordleGame/Wordle-Game/wordle_game/summary.txt'
    _alpha = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    def __init__(self, debug_mode=False):
        with open(self._filename, 'r', encoding='utf8') as f:
            self._words = f.readlines()
            self._running = False
            self._debug = debug_mode

    def start(self):
        cinit(autoreset=True)
        self._word = choice(self._words).strip().upper()
        self._running = True
        self._available = set(self._alpha)
        self._selected = set()
        self._required = set(self._word)
        self._attempts = 6
        self._winning = False
        self._latest = ''

    def finish(self):
        self.clear()
        if self._winning:
            self.out(1, 1, f'{Back.YELLOW}{Fore.BLACK}Вы выиграли!')
        else:
            self.out(1, 1, f'{Back.YELLOW}{Fore.BLACK}Вы проиграли.')
            self.out(2, 1, f'Было загадано слово: {Back.YELLOW}{Fore.BLACK}{self._word}')
        deinit()

    @property
    def running(self):
        return self._running

    def clear(self):
        print(cls())

    def out(self, x, y, text):
        print(f'{CSI}{x};{y}H' + text, end='')

    def update_screen(self):
        self.clear()
        self.print_word()
        self.print_selected()
        self.print_attempts()
        if self._debug: self.debug()

    def print_word(self):
        self.out(1, 1, 'СЛОВО: ')
        for idx, letter in enumerate(self._word):
            if letter in self._required:
                pattern = f'{Back.WHITE}{Fore.BLACK}_'
            elif letter == self._latest:
                pattern = f'{Back.YELLOW}{Fore.BLACK}{letter}'
            else:
                pattern = f'{Back.WHITE}{Fore.BLACK}{letter}'
            self.out(1, 10 + idx * 2, pattern)

    def print_selected(self):
        self.out(2, 1, 'Буквы: ')
        for idx, letter in enumerate(self._alpha):
            if not letter in self._selected:
                pattern = f'{Back.BLACK}{Fore.WHITE}'
            elif letter in self._word:
                pattern = f'{Back.YELLOW}{Fore.BLACK}'
            else:
                pattern = f'{Back.WHITE}{Fore.BLACK}'
            self.out(2, 10 + idx * 2, pattern + letter)

    def print_attempts(self):
        self.out(3, 1, f'{Fore.WHITE}Осталось {Fore.RED}{self._attempts} {Fore.WHITE}попыток')

    def read_letter(self):
        self.out(4, 1, f'Выберите букву: ')
        letter = input().strip().upper()
        if letter in self._available:
            self._available.discard(letter)
            self._required.discard(letter)
            self._selected.add(letter)
            self._attempts -= 1
            self._latest = letter

    def decide(self):
        self._winning = len(self._required) == 0
        self._running = self._attempts > 0 and not self._winning

    def debug(self):
        self.out(20, 20, f'{Fore.MAGENTA}{Back.WHITE}{self._word}')


if __name__ == "__main__":
    game = Wordle()
    game.start()
    while game.running:
        game.update_screen()
        game.read_letter()
        game.decide()

    game.finish()