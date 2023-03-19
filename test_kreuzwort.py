"""tests for kreuzwort.py"""

import pytest
from kreuzwort import Wordlist


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
    assert expected == current.find_possibilities(candidate)


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
            ["chair", "cardboard", "speaker", "bottle"],
            ["cardboard", "speaker", "chair"],
        ),
        (
            ["book", "tissue", "water"],
            ["tissue", "water"],
        ),
    ],
)
def test_unplaceables(inputs, expected) -> None:
    """
    given a list of words, this should eliminate those words which cannot be combined
    with any others in the list
    """
    assert expected == Wordlist(inputs).place_words()
