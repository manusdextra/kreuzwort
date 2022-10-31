import unittest
from ddt import ddt, data, unpack
from kreuzwort import Wordlist, Table


@ddt
class TestNodes(unittest.TestCase):
    @unpack
    @data(
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
    )
    def test_nodes(self, inputs, expected):
        self.assertEqual([word.nodes for word in Wordlist(inputs).items], expected)


@ddt
class TestNamedNodes(unittest.TestCase):
    @unpack
    @data(
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
    )
    def test_named_nodes(self, inputs, expected):
        self.assertEqual([word.named_nodes for word in Wordlist(inputs).items], expected)

@ddt
class TestRanking(unittest.TestCase):
    @unpack
    @data(
        (
            ["chair", "cardboard", "speaker", "bottle"],
            ["cardboard"],
        ),
        (
            ["pen", "eraser", "schedule", "phone"],
            ["schedule"],
        ),
        (
            [
                "book",
                "tissue",
                "water",
            ],
            ["tissue"],
        ),
        (
            [
                "dictionary",
                "maths",
                "tablet",
            ],
            ["tablet"],
        ),
        (
            [
                "rucksack",
                "vocabulary",
                "medicine",
            ],
            ["rucksack"],
        ),
    )
    def test_ranking(self, inputs, expected):
        self.assertEqual([Table(inputs).placed[0].letters], expected)


@ddt
class TestCombinations(unittest.TestCase):
    @unpack
    @data(
        (
            ["chair", "cardboard"],
            [(0, 0), (1, 2), (2, 4), (6, 2), (7, 4)],
        ),
    )
    def test_combinations(self, inputs, expected):
        table = Table(inputs)
        (current, next) = table.unplaced
        self.assertEqual(table.find_possibilities(current, next), expected)
