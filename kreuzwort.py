"""
Generate an arrowword puzzle from an unordered list of words (and definitions).
"""

from typing import Iterator, List, Literal
from enum import Enum


class Orientation(Enum):
    """this will be useful as a cursor of sorts,
    as well as enabling the growth of a grid by multiplying
    with the length of a word or some other number.

    The tuples can be accessed with Orientation.value

    TODO: should this be subclassed for a cursor so it can be used
    with negative values (which you need to grow the grid for example)?
    """

    # NB the tuple values are (row, column)
    ACROSS = (0, 1)
    DOWN = (1, 0)


class Word:

    """class for dictionary items and their necessary properties"""

    def __init__(self, letters) -> None:
        """gather information that will help in analysing the dictionary"""
        self.letters: str = letters
        self.hint: Literal[""] = ""  # definition to be added
        self.named_nodes: dict[int, str] = {}
        self.orientation: Orientation
        self.position: tuple[int, int]  # will need to be updated

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

    @property
    def nodes(self):
        """
        this is done for convenience, I don't know if
        it actually will be useful in the future
        """
        return list(self.named_nodes.keys())

    def find_intersections(self, candidate) -> list[tuple[int, int]]:
        """
        list all possible connections between two words
        """
        intersections: list[tuple[int, int]] = []
        for index, letter in self.named_nodes.items():
            matches: list = [
                i
                for i in candidate.named_nodes.keys()
                if candidate.named_nodes[i] == letter
            ]
            for match in matches:
                intersections.append((index, match))
        return intersections


class Wordlist:
    """
    a sorted list of words, ranked by their number of possible combinations
    """

    def __init__(self, words) -> None:
        """analysis methods"""
        self.items: list[Word] = [Word(item) for item in words]
        self.alphabet: dict[str, int] = self.find_all_letters()
        self.items: list[Word] = self.analyse(self.items)
        self.best_choices: list[Word] = self.rank_words()

    def __iter__(self) -> Iterator[Word]:
        """helper"""
        return iter([word for word in self.items])

    def __getitem__(self, index: int) -> Word:
        """helper"""
        return self.items[index]

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
            if current.find_intersections(candidate):
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

    @property
    def rows(self):
        return len(self.grid)

    @property
    def columns(self):
        return len(self.grid[0])

    def output(self):
        for line in self.grid:
            print(line)

    def make_space(
        self,
        spaces=0,
        orientation=Orientation.ACROSS,
        forward=True,
    ):
        """This function inserts or append rows and columns."""
        match (orientation, forward):
            # trailing columns
            case (Orientation.ACROSS, True):
                self.grid = [row + ["_" for _ in range(0, spaces)] for row in self.grid]
            # leading columns
            case (Orientation.ACROSS, False):
                self.grid = [["_" for _ in range(0, spaces)] + row for row in self.grid]
                # update position of previously placed words
                for word in self.placed_words:
                    pos_row, pos_col = word.position
                    pos_col += spaces
                    word.position = (pos_row, pos_col)
            # trailing rows
            case (Orientation.DOWN, True):
                for _ in range(0, spaces):
                    self.grid.append(["_" for _ in range(0, self.columns)])
            # leading rows
            case (Orientation.DOWN, False):
                for _ in range(0, spaces):
                    self.grid.insert(0, ["_" for _ in range(0, self.columns)])
                # update position of previously placed words
                for word in self.placed_words:
                    pos_row, pos_col = word.position
                    pos_row += spaces
                    word.position = (pos_row, pos_col)

    def find_matching_word(
        self, next_word: Word, attempt=1
    ) -> tuple[Word, list[tuple[int, int]]]:
        """ Go through the list of previously placed
        words and find one that matches, then return
        the chosen word and a list of possible
        intersections """
        # check previously placed word(s) for a match
        if attempt > len(self.placed_words):
            self.output()
            raise SystemExit(f"Can't match {next_word} with any of the others")
        prev_word = self.placed_words[-attempt]
        next_word.orientation = [
            _ for _ in Orientation if not _ == prev_word.orientation
        ][0]
        possibilities = prev_word.find_intersections(next_word)
        if not possibilities:
            return self.find_matching_word(next_word, attempt=attempt + 1)
        return prev_word, possibilities

    def place(self, next_word: Word) -> None:
        """find somewhere to put the word"""
        if not self.placed_words:
            next_word.orientation = Orientation.ACROSS
            self.make_space(
                len(next_word),
                next_word.orientation,
                forward=True,
            )
            next_word.position = (0, 0)
            self.write(next_word)
            self.placed_words.append(next_word)
            return None

        # choose a possible connection
        prev_word, possibilities = self.find_matching_word(next_word)
        # TODO: this could be a point where a choice between different
        # strategies could be made
        possibility = possibilities[0]
        node_prev_word, node_next_word = possibility

        # start with the absolute position of the next word, which may
        # be out of bounds
        row_absolute, column_absolute = prev_word.position
        row_multiplier, column_multiplier = prev_word.orientation.value
        next_word.position = (
            (row_absolute + row_multiplier * node_prev_word),
            (column_absolute + column_multiplier * node_prev_word),
        )

        # calculate & make required space
        if next_word.orientation == Orientation.ACROSS:
            leading_spaces = prev_word.position[1] - node_next_word
        else:
            leading_spaces = prev_word.position[0] - node_next_word
        if leading_spaces < 0:
            self.make_space(
                leading_spaces * -1,
                next_word.orientation,
                forward=False,
            )
        # update position of next word
        row_next, column_next = next_word.position
        if next_word.orientation == Orientation.ACROSS:
            next_word.position = (
                    row_next,
                    (prev_word.position[1] - node_next_word),
            )
        else:
            next_word.position = (
                    (prev_word.position[0] - node_next_word),
                    column_next,
            )

        trailing_spaces = len(next_word) - node_next_word - 1
        prev_row, prev_col = prev_word.position
        if next_word.orientation == Orientation.ACROSS:
            absolute_column = prev_col + node_next_word
            space_needed = absolute_column + trailing_spaces > len(self.grid[0])
        else:
            absolute_row = prev_row + node_next_word
            space_needed = absolute_row + trailing_spaces > len(self.grid)
        if space_needed:
            self.make_space(
                trailing_spaces,
                next_word.orientation,
                forward=True,
            )

        # check if the position would lead to any conflicts
        if not self.check(next_word.position, next_word):
            return None

        # commit
        self.write(next_word)
        # delete the used match from the named nodes of both words
        # to avoid future collisions
        prev_node = possibility[0]
        next_node = possibility[1]

        # NB this is a fairly blunt force approach as it doesn't take into
        # account the possibility of adjacent letters matching with the first
        # and last of two other words. Is there a way to allow for this?
        prev_word.named_nodes.pop(prev_node - 1, None)
        prev_word.named_nodes.pop(prev_node, None)
        prev_word.named_nodes.pop(prev_node + 1, None)
        next_word.named_nodes.pop(next_node - 1, None)
        next_word.named_nodes.pop(next_node, None)
        next_word.named_nodes.pop(next_node + 1, None)
        self.placed_words.append(next_word)
        self.output()

    def check(self, position, word: Word) -> bool:
        """checks the existing grid (ignoring its bounds) for conflicting
        letters and returns True if the word can be placed here"""
        checks = []
        (row, column) = position
        if word.orientation == Orientation.ACROSS:
            for space, letter in enumerate(word.letters):
                try:
                    square = self.grid[row][column + space]
                    checks.append(square == letter or square == "_")
                except IndexError:
                    checks.append(True)
        if word.orientation == Orientation.DOWN:
            for space, letter in enumerate(word.letters):
                try:
                    square = self.grid[row + space][column]
                    checks.append(square == letter or square == "_")
                except IndexError:
                    checks.append(True)
        return all(checks)

    def write(self, current_word: Word) -> None:
        """add single word to the grid"""
        (row, column) = current_word.position
        if current_word.orientation == Orientation.ACROSS:
            for space, letter in enumerate(current_word.letters):
                self.grid[row][column + space] = letter
        if current_word.orientation == Orientation.DOWN:
            for space, letter in enumerate(current_word.letters):
                self.grid[row + space][column] = letter
