from typing import List
import util

def test_lowest():
    members = {}
    assert util.lowest(members) is None

    members = {
        "fred": 1,
        "george": 2,
        "ron": 3,
    }
    assert util.lowest(members) == "fred"

    members = {
        "fred": 1,
        "george": 1,
        "ron": 3,
    }
    assert util.lowest(members) is None

    members = {
        "fred": 1,
        "george": 1,
        "ron": 1,
    }
    assert util.lowest(members) is None

def test_highest():
    members = {}
    assert util.highest(members) is None

    members = {
        "fred": 1,
        "george": 2,
        "ron": 3,
    }
    assert util.highest(members) == "ron"

    members = {
        "fred": 1,
        "george": 3,
        "ron": 3,
    }
    assert util.highest(members) is None

    members = {
        "fred": 1,
        "george": 1,
        "ron": 1,
    }
    assert util.highest(members) is None

def test_unique_combinations():
    roll = [1, 2, 3]
    expected: List[List[int]] = [
        [1],
        [2],
        [3],
        [1, 2],
        [1, 3],
        [2, 3],
        [1, 2, 3]
    ]
    got = util.unique_combinations(roll)
    assert got == expected

def test_unique_combinations__allones():
    roll = [1, 1, 1]
    expected: List[List[int]] = [
        [1],
        [1, 1],
        [1, 1, 1]
    ]
    got = util.unique_combinations(roll)
    assert got == expected
