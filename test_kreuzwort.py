"""tests for kreuzwort.py"""

import pytest
from kreuzwort import Layout, Orientation, Word, Wordlist


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["chair", "cardboard", "speaker", "bottle"],
            [
                [0, 2, 4],
                [0, 1, 2, 4, 5, 6, 7],
                [2, 3, 5, 6],
                [0, 1, 5],
            ],
        ),
        (
            ["pen", "eraser", "schedule", "phone"],
            [
                [0, 1, 2],
                [0, 3, 4],
                [0, 2, 3, 7],
                [0, 1, 3, 4],
            ],
        ),
        (
            [
                "book",
                "tissue",
                "water",
            ],
            [
                [],
                [0, 5],
                [2, 3],
            ],
        ),
        (
            [
                "dictionary",
                "maths",
                "tablet",
            ],
            [
                [3, 7],
                [1, 2],
                [0, 1, 5],
            ],
        ),
        (
            [
                "rucksack",
                "vocabulary",
                "medicine",
            ],
            [
                [0, 1, 2, 5, 6],
                [2, 3, 5, 7, 8],
                [4],
            ],
        ),
        (
            [
                "armchair",
                "variety",
                "uncle",
                "country",
                "special",
            ],
            [
                [0, 1, 3, 5, 6, 7],
                [1, 2, 3, 4, 5, 6],
                [0, 1, 2, 3, 4],
                [0, 2, 3, 4, 5, 6],
                [2, 3, 4, 5, 6],
            ],
        ),
    ],
)
def test_nodes(inputs, expected):
    """
    Given a combination of words, this function should return
    a list of lists with the indexes of letters where a combination
    with other words is possible
    """
    assert expected == [word.nodes for word in Wordlist(inputs).items]


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["chair", "cardboard", "speaker", "bottle"],
            [
                {0: "c", 2: "a", 4: "r"},
                {0: "c", 1: "a", 2: "r", 4: "b", 5: "o", 6: "a", 7: "r"},
                {2: "e", 3: "a", 5: "e", 6: "r"},
                {0: "b", 1: "o", 5: "e"},
            ],
        ),
        (
            [
                "book",
                "tissue",
                "water",
            ],
            [
                {},
                {0: "t", 5: "e"},
                {2: "t", 3: "e"},
            ],
        ),
        (
            [
                "dictionary",
                "maths",
                "tablet",
            ],
            [
                {3: "t", 7: "a"},
                {1: "a", 2: "t"},
                {0: "t", 1: "a", 5: "t"},
            ],
        ),
    ],
)
def test_named_nodes(inputs, expected):
    """
    Given a list of words, this function should return a dict for each word
    containing the indexes of possible matches and the letter at that index
    """
    assert expected == [word.named_nodes for word in Wordlist(inputs).items]


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["cardboard", "chair"],
            [(0, 0), (1, 2), (2, 4), (6, 2), (7, 4)],
        ),
        (
            ["rucksack", "maths"],
            [(4, 4), (5, 1)],
        ),
        (
            ["tablet", "dictionary"],
            [(0, 3), (1, 7), (5, 3)],
        ),
        (
            ["medicine", "rucksack"],
            [(4, 2), (4, 6)],
        ),
        (
            ["abc", "xyz"],
            [],
        ),
    ],
)
def test_combinations(inputs, expected):
    """
    Given two words, this should return a list of tuples containing the indexes
    of common letters in the first and second word
    """
    (current, candidate) = Wordlist(inputs).items
    assert expected == current.find_intersections(candidate)


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["pen", "eraser", "schedule", "phone"],
            ["schedule", "phone", "pen", "eraser"],
        ),
        (
            [
                "uncle",
                "armchair",
                "variety",
                "country",
                "special",
            ],
            [
                "armchair",
                "variety",
                "country",
                "uncle",
                "special",
            ],
        ),
        (
            [
                "dictionary",
                "maths",
                "tablet",
            ],
            [
                "tablet",
                "dictionary",
                "maths",
            ],
        ),
        (
            [
                "rucksack",
                "vocabulary",
                "medicine",
            ],
            [
                "rucksack",
                "vocabulary",
                "medicine",
            ],
        ),
    ],
)
def test_placeables(inputs, expected) -> None:
    """
    given a list of words, this should sort them in order of how easy
    they are to place
    """
    assert expected == Wordlist(inputs).best_choices


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["chair", "card", "bet"],
            ["bet"],
        ),
        (
            ["drawing", "fairy", "harp", "bottle"],
            ["bottle"],
        ),
        (
            ["book", "tissue", "water"],
            ["book"],
        ),
    ],
)
def test_unplaceables(inputs, expected) -> None:
    """given a list of words, this should eliminate those words which
    cannot be combined with any others in the list"""
    assert expected == Wordlist(inputs).unplaceables


def test_initial_word() -> None:
    """
    given a simple word, this should make a grid with the same dimensions and place it
    """
    layout = Layout([[]])
    layout.place(Word("hello"))
    assert layout.grid == [["h", "e", "l", "l", "o"]]


@pytest.mark.parametrize(
    "spaces,orientation,forward,expected",
    [
        (
            1,
            Orientation.ACROSS,
            True,
            [
                ["_", "_", "_", "_"],
                ["_", "x", "_", "_"],
                ["_", "_", "_", "_"],
            ],
        ),
        (
            2,
            Orientation.DOWN,
            True,
            [
                ["_", "_", "_"],
                ["_", "x", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"],
            ],
        ),
        (
            3,
            Orientation.DOWN,
            True,
            [
                ["_", "_", "_"],
                ["_", "x", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"],
            ],
        ),
        (
            1,
            Orientation.DOWN,
            False,
            [
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "x", "_"],
                ["_", "_", "_"],
            ],
        ),
    ],
)
def test_make_space(spaces, orientation, forward, expected) -> None:
    """
    given an initial nested list, a direction and a number to grow it by, this should
    append the list (or the lists nested therein) to grow the size of the grid
    """
    initial = [
        ["_", "_", "_"],
        ["_", "x", "_"],
        ["_", "_", "_"],
    ]
    initial = Layout(initial)
    initial.make_space(spaces, orientation, forward)
    assert initial.grid == expected


@pytest.mark.parametrize(
    "spaces,orientation,forward,expected",
    [
        (1, Orientation.DOWN, False, (1, 0)),
        (3, Orientation.ACROSS, True, (0, 0)),
        (2, Orientation.DOWN, False, (2, 0)),
    ],
)
def test_shifted_words(spaces, orientation, forward, expected) -> None:
    """
    given an inital table and a dimension to expand that table, are the placed word's
    positions shifted accurately?
    """
    words = Wordlist(["hello"])
    table = Layout([[]])
    table.place(words[0])
    table.make_space(spaces, orientation, forward)
    assert table.placed_words[0].position == expected


def test_write() -> None:
    table = Layout(
        [
            ["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"],
        ]
    )
    word = Wordlist(["abc"])[0]
    word.position = (1, 0)
    word.orientation = Orientation.ACROSS
    table.write(word)
    assert table.grid == [
        ["_", "_", "_"],
        ["a", "b", "c"],
        ["_", "_", "_"],
    ]


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            [
                "hello",
                "bye",
            ],
            [
                ["_", "b", "_", "_", "_"],
                ["_", "y", "_", "_", "_"],
                ["h", "e", "l", "l", "o"],
            ],
        ),
        (
            [
                "chair",
                "cardboard",
            ],
            [
                ["c", "a", "r", "d", "b", "o", "a", "r", "d"],
                ["h", "_", "_", "_", "_", "_", "_", "_", "_"],
                ["a", "_", "_", "_", "_", "_", "_", "_", "_"],
                ["i", "_", "_", "_", "_", "_", "_", "_", "_"],
                ["r", "_", "_", "_", "_", "_", "_", "_", "_"],
            ],
        ),
        (
            [
                "speaker",
                "chair",
            ],
            [
                ["_", "_", "_", "c", "_", "_", "_"],
                ["_", "_", "_", "h", "_", "_", "_"],
                ["s", "p", "e", "a", "k", "e", "r"],
                ["_", "_", "_", "i", "_", "_", "_"],
                ["_", "_", "_", "r", "_", "_", "_"],
            ],
        ),
        (
            [
                "cardboard",
                "chair",
                "speaker",
            ],
            [
                ["_", "_", "_", "c", "a", "r", "d", "b", "o", "a", "r", "d"],
                ["_", "_", "_", "h", "_", "_", "_", "_", "_", "_", "_", "_"],
                ["s", "p", "e", "a", "k", "e", "r", "_", "_", "_", "_", "_"],
                ["_", "_", "_", "i", "_", "_", "_", "_", "_", "_", "_", "_"],
                ["_", "_", "_", "r", "_", "_", "_", "_", "_", "_", "_", "_"],
            ],
        ),
    ],
)
def test_words(inputs, expected) -> None:
    table = Layout([[]])
    words = Wordlist(inputs)
    for word in words.best_choices:
        table.place(word)
    assert table.grid == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            [
                "double",
                "card",
                "armour",
            ],
            [
                ["c", "_", "_", "d", "_", "_"],
                ["a", "r", "m", "o", "u", "r"],
                ["r", "_", "_", "u", "_", "_"],
                ["d", "_", "_", "b", "_", "_"],
                ["_", "_", "_", "l", "_", "_"],
                ["_", "_", "_", "e", "_", "_"],
            ],
        ),
        (
            [
                "chair",
                "speaker",
                "bottle",
            ],
            [
                ["_", "_", "_", "_", "_", "b", "_"],
                ["_", "_", "_", "_", "_", "o", "_"],
                ["_", "_", "_", "_", "_", "t", "_"],
                ["_", "_", "_", "c", "_", "t", "_"],
                ["_", "_", "_", "h", "_", "l", "_"],
                ["s", "p", "e", "a", "k", "e", "r"],
                ["_", "_", "_", "i", "_", "_", "_"],
                ["_", "_", "_", "r", "_", "_", "_"],
            ],
        ),
    ],
)
def test_collision_detection(inputs, expected) -> None:
    table = Layout([[]])
    words = Wordlist(inputs)
    for word in words.best_choices:
        table.place(word)
    assert table.grid == expected


def test_fresh_start() -> None:
    """
    after other tests, calling the constructor with an empty matrix should
    yield a clean grid
    """
    layout = Layout([[]])
    assert layout.grid == [[]]
