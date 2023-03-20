"""Generate an arrowword puzzle from an unordered list of words (and definitions)."""

from typing import Iterator, List, Literal
from enum import Enum
import random


class Orientation(Enum):
    """this will be useful as a cursor of sorts,
    as well as enabling the growth of a grid by multiplying
    with the length of a word or some other number.

    The tuples can be accessed with Orientation.value

    TODO: should this be subclassed for a cursor so it can be used
    with negative values (which you need to grow the grid for example)?
    """

    ACROSS = (1, 0)
    DOWN = (0, 1)


class Word:

    """class for dictionary items and their necessary properties"""

    def __init__(self, letters) -> None:
        """gather information that will help in analysing the dictionary"""
        self.letters: str = letters
        self.hint: Literal[""] = ""  # definition to be added
        self.named_nodes: dict[int, str] = {}
        self.nodes: list[int] = []
        self.orientation: Orientation

    def __repr__(self) -> str:
        """use the word itself to represent this class"""
        return self.letters

    def __iter__(self) -> Iterator[str]:
        """another helper with the same function as above"""
        return iter(self.letters)

    def __eq__(self, other) -> bool:
        """this helps with testing"""
        return self.letters == other

    def __len__(self) -> int:
        return len(self.letters)

    def find_possibilities(self, candidate) -> list[tuple[int, int]]:
        """
        list all possible connections between two words,
        represented as a tuple of index and letter
        """
        possibilities: list[tuple[int, int]] = []
        for index, letter in enumerate(self.letters):
            matches: list = [
                i
                for i in candidate.named_nodes.keys()
                if candidate.named_nodes[i] == letter
            ]
            for match in matches:
                possibilities.append((index, match))
        return possibilities


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

    def __eq__(self, other) -> bool:
        """this helps with testing"""
        return self.items == other.items

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

    def place_words(self) -> list[Word]:
        """
        main combination loop

        TODO: design a data structure for recording placement options,
        ideally in a way that has branches for the different possibilities
        """
        placed: list[Word] = [self.best_choices.pop(0)]
        for index, candidate in enumerate(self.best_choices):
            current = placed[index]
            if current.find_possibilities(candidate):
                placed.append(candidate)
        return placed


class Layout:
    """here, the words are joined up and eventually, a completed
    puzzle will be printed / output"""

    def __init__(
        self,
        grid: list[list[str]] = [[]],
    ) -> None:
        """set up dimensions of grid, track history"""
        self.placed_words: List[Word] = []
        self.grid: list[list[str]] = grid

    def make_space(
        self,
        spaces=0,
        orientation=Orientation.ACROSS,
        forward=True,
    ):
        length = len(self.grid[0])
        match (orientation, forward):
            case (Orientation.ACROSS, True):
                for row in self.grid:
                    row += ["_" for _ in range(0, spaces)]
            case (Orientation.ACROSS, False):
                for row in self.grid:
                    row = ["_" for _ in range(0, spaces)] + row
            case (Orientation.DOWN, True):
                for _ in range(0, spaces):
                    self.grid.append(["_" for _ in range(0, length)])
            case (Orientation.DOWN, False):
                for _ in range(0, spaces):
                    self.grid.insert(0, ["_" for _ in range(0, length)])

    def start(self, first: Word) -> None:
        """place first word"""
        first.orientation = Orientation.ACROSS
        self.make_space(len(first), first.orientation)
        if first.orientation == Orientation.ACROSS:
            for space, letter in enumerate(first.letters):
                self.grid[0][space] = letter
        if first.orientation == Orientation.DOWN:
            for space, letter in enumerate(first.letters):
                self.grid[space][0] = letter
        self.placed_words.append(first)

    def place(self, next_word: Word) -> None:
        """add single word to the grid"""
        if not self.placed_words:
            self.start(next_word)
        else:
            pass
