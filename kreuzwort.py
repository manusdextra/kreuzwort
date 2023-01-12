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
        return self.letters

    def __iter__(self) -> Iterator[str]:
        """another helper with the same function as above"""
        return iter(self.letters)

    def __eq__(self, other) -> bool:
        """this helps with testing"""
        return self.letters == other


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
        return iter([word for word in self.items])

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
        """
        this could be adapted to different strategies
        according to what determines a word's worth

        TODO: it could also return a score, which would
        make testing it easier since more than one word
        can have a particular score
        """
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
                i
                for i in candidate.named_nodes.keys()
                if candidate.named_nodes[i] == letter
            ]
            for match in matches:
                possibilities.append((index, match))
        return possibilities

    def place_words(self) -> list[Word]:
        """
        main combination loop

        TODO: design a data structure for recording placement options,
        ideally in a way that has branches for the different possibilities
        """
        placed: list[Word] = [self.unplaced.best_choices.pop(0)]
        for index, candidate in enumerate(self.unplaced.best_choices):
            current = placed[index]
            if self.find_possibilities(current, candidate):
                placed.append(candidate)
        return placed
