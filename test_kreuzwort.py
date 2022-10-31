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
