from kreuzwort import find_nodes

first_batch = [
    "book",
    "tissue",
    "water",
    ]

second_batch = [
    "dictionary",
    "maths",
    "tablet",
    ]

third_batch = [
    "rucksack",
    "vocabulary",
    "medicine",
    ]

def test_first_batch():
    assert find_nodes(first_batch) == [
            [],
            [0,5],
            [2,3],
    ]
