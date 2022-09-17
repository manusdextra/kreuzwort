import unittest
from ddt import ddt, data, unpack
from kreuzwort import find_nodes

@ddt
class TestNodes(unittest.TestCase):

    @unpack
    @data(
        (
            [ "book", "tissue", "water", ],
            [
                [],
                [0,5],
                [2,3],
            ]
        ),
        (   
            [ "dictionary", "maths", "tablet", ],
            [
                [3,7],
                [1,2],
                [0,1,5],
            ]
        ),
        (
            [ "rucksack", "vocabulary", "medicine", ],
            [
                [0,1,2,5,6],
                [2,3,5,7,8],
                [4],
            ]
        ),
    )
    def test_nodes(self, inputs, expected):
        self.assertEqual(find_nodes(inputs), expected)
