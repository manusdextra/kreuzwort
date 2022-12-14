"""Generate an arrowword puzzle from an unordered list of words (and definitions)."""

from typing import Iterator, Literal


class Word:
    """class for dictionary items and their necessary properties"""

    def __init__(self, letters) -> None:
        """gather information that will help in analysing the dictionary"""
        self.letters: str = letters
        self.hint: Literal[""] = ""  # definition to be added
        self.named_nodes: dict[int, str] = {}
        self.nodes: list[int] = []

    def __repr__(self) -> str:
        """use the word itself to represent this class"""
        return f"'{self.letters}'"

    def __iter__(self) -> Iterator[str]:
        """another helper with the same function as above"""
        return iter(self.letters)


class Wordlist:
    """a sorted list of words, ranked by their number of possible combinations"""

    def __init__(self, words) -> None:
        """analysis methods"""
        self.items: list[Word] = [Word(item) for item in words]
        self.alphabet: dict[str, int] = self.find_all_letters()
        self.items: list[Word] = self.analyse(self.items)
        self.best_choices: list[Word] = self.rank_words()

    def __iter__(self) -> Iterator[Word]:
        """helper"""
        return iter(self.items)

    def find_all_letters(self) -> dict[str, int]:
        """starting point for analysis"""
        alphabet: dict[str, int] = {}
        for item in self.items:
            for letter in item.letters:
                if letter in alphabet:
                    alphabet[letter] += 1
                else:
                    alphabet[letter] = 1
        return alphabet

    def analyse(self, items) -> list[Word]:
        """find common letters"""
        for item in items:
            for index, letter in enumerate(item.letters):
                if letter not in self.alphabet:
                    continue
                if self.alphabet[letter] == 1:
                    continue
                item.named_nodes[index] = letter

        # throw out letters that only occur in the same word
        for item in items:
            for index, letter in item.named_nodes.items():
                if self.alphabet[letter] == item.letters.count(letter):
                    item.named_nodes[index] = 0

            # this seems to be necessary because
            # you can't delete entries while looping over a dict
            item.named_nodes = {
                key: val for key, val in item.named_nodes.items() if val != 0
            }

            # this is done for convenience, I don't know if
            # it actually will be useful in the future
            item.nodes = list(item.named_nodes.keys())
        return items

    def rank_words(self) -> list[Word]:
        """this could be adapted to different strategies
        according to what determines a word's worth"""
        return sorted(self.items, key=lambda x: len(x.nodes), reverse=True)


class Table:
    """here, the words are joined up and eventually, a completed
    puzzle will be printed / output"""

    def __init__(self, words) -> None:
        """maintain separate lists"""
        self.unplaced: Wordlist = Wordlist(words)
        self.placed: list[Word] = self.place_words()

    def find_possibilities(self, current, candidate) -> list[tuple[int, int]]:
        """
        list all possible connections between two words,
        represented as a tuple of index and letter
        """
        possibilities: list[tuple[int, int]] = []
        for index, letter in enumerate(current.letters):
            matches: list = [
                i for i in candidate.named_nodes.keys() if candidate.named_nodes[i] == letter
            ]
            for match in matches:
                possibilities.append((index, match))
        return possibilities

    def place_words(self) -> list[Word]:
        """main combination loop"""
        placed: list[Word] = []
        while self.unplaced.best_choices:
            print(placed)
            current = self.unplaced.best_choices.pop(0)
            # automatically place first word
            if not placed:
                placed.append(current)
            for candidate in self.unplaced.best_choices:
                if self.find_possibilities(current, candidate):
                    placed.append(candidate)
                    break
        return placed
