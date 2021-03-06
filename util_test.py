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
        [],
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
        [],
        [1],
        [1, 1],
        [1, 1, 1]
    ]
    got = util.unique_combinations(roll)
    assert got == expected

def test_unique_list_pairs__withduplicate():
    player_roll = [1, 1, 1]
    bonus_roll = [1]
    expected = [
        [1, 1]
    ]
    got = util.unique_list_pairs(
        player_roll,
        bonus_roll,
    )

    assert got == expected

def test_unique_list_pairs__onebonus():
    player_roll = [1, 2, 3]
    bonus_roll = [4]
    expected = [
        [[], []],
        [[], [4]],
        [[1], []],
        [[1], [4]],
        [[2], []],
        [[2], [4]],
        [[3], []],
        [[3], [4]],
        [[1, 2], []],
        [[1, 2], [4]],
        [[1, 3], []],
        [[1, 3], [4]],
        [[2, 3], []],
        [[2, 3], [4]],
        [[1, 2, 3], []],
        [[1, 2, 3], [4]],
    ]
    got = util.unique_list_pairs(
        util.unique_combinations(player_roll),
        util.unique_combinations(bonus_roll)
    )

    assert got == expected

def test_unique_list_pairs__twobonus():
    player_roll = [1, 2, 3]
    bonus_roll = [4, 5]
    expected = [
        [[], []],
        [[], [4]],
        [[], [5]],
        [[], [4, 5]],
        [[1], []],
        [[1], [4]],
        [[1], [5]],
        [[1], [4, 5]],
        [[2], []],
        [[2], [4]],
        [[2], [5]],
        [[2], [4, 5]],
        [[3], []],
        [[3], [4]],
        [[3], [5]],
        [[3], [4, 5]],
        [[1, 2], []],
        [[1, 2], [4]],
        [[1, 2], [5]],
        [[1, 2], [4, 5]],
        [[1, 3], []],
        [[1, 3], [4]],
        [[1, 3], [5]],
        [[1, 3], [4, 5]],
        [[2, 3], []],
        [[2, 3], [4]],
        [[2, 3], [5]],
        [[2, 3], [4, 5]],
        [[1, 2, 3], []],
        [[1, 2, 3], [4]],
        [[1, 2, 3], [5]],
        [[1, 2, 3], [4, 5]],
    ]
    got = util.unique_list_pairs(
        util.unique_combinations(player_roll),
        util.unique_combinations(bonus_roll)
    )

    assert got == expected

def test_unique_list_pairs__onebonusandplustwo():
    player_roll = [1, 2, 3]
    bonus_roll = [4]
    plus_two = [1]
    expected = [
        [[[], []], []],
        [[[], []], [1]],
        [[[], [4]], []],
        [[[], [4]], [1]],
        [[[1], []], []],
        [[[1], []], [1]],
        [[[1], [4]], []],
        [[[1], [4]], [1]],
        [[[2], []], []],
        [[[2], []], [1]],
        [[[2], [4]], []],
        [[[2], [4]], [1]],
        [[[3], []], []],
        [[[3], []], [1]],
        [[[3], [4]], []],
        [[[3], [4]], [1]],
        [[[1, 2], []], []],
        [[[1, 2], []], [1]],
        [[[1, 2], [4]], []],
        [[[1, 2], [4]], [1]],
        [[[1, 3], []], []],
        [[[1, 3], []], [1]],
        [[[1, 3], [4]], []],
        [[[1, 3], [4]], [1]],
        [[[2, 3], []], []],
        [[[2, 3], []], [1]],
        [[[2, 3], [4]], []],
        [[[2, 3], [4]], [1]],
        [[[1, 2, 3], []], []],
        [[[1, 2, 3], []], [1]],
        [[[1, 2, 3], [4]], []],
        [[[1, 2, 3], [4]], [1]],
    ]
    got = util.unique_list_pairs(
        util.unique_list_pairs(
            util.unique_combinations(player_roll),
            util.unique_combinations(bonus_roll)
        ),
        util.unique_combinations(plus_two)
    )

    assert got == expected

def test_unique_list_pairs__onebonusandplustwoandmarket():
    player_roll = [1, 2, 3]
    bonus_roll = [4]
    plus_two = [1]
    market = [-1, 1]
    expected = [
        [[[[], []], []], []],
        [[[[], []], []], [-1]],
        [[[[], []], []], [1]],

        [[[[], []], [1]], []],
        [[[[], []], [1]], [-1]],
        [[[[], []], [1]], [1]],

        [[[[], [4]], []], []],
        [[[[], [4]], []], [-1]],
        [[[[], [4]], []], [1]],

        [[[[], [4]], [1]], []],
        [[[[], [4]], [1]], [-1]],
        [[[[], [4]], [1]], [1]],

        [[[[1], []], []], []],
        [[[[1], []], []], [-1]],
        [[[[1], []], []], [1]],

        [[[[1], []], [1]], []],
        [[[[1], []], [1]], [-1]],
        [[[[1], []], [1]], [1]],

        [[[[1], [4]], []], []],
        [[[[1], [4]], []], [-1]],
        [[[[1], [4]], []], [1]],

        [[[[1], [4]], [1]], []],
        [[[[1], [4]], [1]], [-1]],
        [[[[1], [4]], [1]], [1]],

        [[[[2], []], []], []],
        [[[[2], []], []], [-1]],
        [[[[2], []], []], [1]],

        [[[[2], []], [1]], []],
        [[[[2], []], [1]], [-1]],
        [[[[2], []], [1]], [1]],

        [[[[2], [4]], []], []],
        [[[[2], [4]], []], [-1]],
        [[[[2], [4]], []], [1]],

        [[[[2], [4]], [1]], []],
        [[[[2], [4]], [1]], [-1]],
        [[[[2], [4]], [1]], [1]],

        [[[[3], []], []], []],
        [[[[3], []], []], [-1]],
        [[[[3], []], []], [1]],

        [[[[3], []], [1]], []],
        [[[[3], []], [1]], [-1]],
        [[[[3], []], [1]], [1]],

        [[[[3], [4]], []], []],
        [[[[3], [4]], []], [-1]],
        [[[[3], [4]], []], [1]],

        [[[[3], [4]], [1]], []],
        [[[[3], [4]], [1]], [-1]],
        [[[[3], [4]], [1]], [1]],

        [[[[1, 2], []], []], []],
        [[[[1, 2], []], []], [-1]],
        [[[[1, 2], []], []], [1]],

        [[[[1, 2], []], [1]], []],
        [[[[1, 2], []], [1]], [-1]],
        [[[[1, 2], []], [1]], [1]],

        [[[[1, 2], [4]], []], []],
        [[[[1, 2], [4]], []], [-1]],
        [[[[1, 2], [4]], []], [1]],

        [[[[1, 2], [4]], [1]], []],
        [[[[1, 2], [4]], [1]], [-1]],
        [[[[1, 2], [4]], [1]], [1]],

        [[[[1, 3], []], []], []],
        [[[[1, 3], []], []], [-1]],
        [[[[1, 3], []], []], [1]],

        [[[[1, 3], []], [1]], []],
        [[[[1, 3], []], [1]], [-1]],
        [[[[1, 3], []], [1]], [1]],

        [[[[1, 3], [4]], []], []],
        [[[[1, 3], [4]], []], [-1]],
        [[[[1, 3], [4]], []], [1]],

        [[[[1, 3], [4]], [1]], []],
        [[[[1, 3], [4]], [1]], [-1]],
        [[[[1, 3], [4]], [1]], [1]],

        [[[[2, 3], []], []], []],
        [[[[2, 3], []], []], [-1]],
        [[[[2, 3], []], []], [1]],

        [[[[2, 3], []], [1]], []],
        [[[[2, 3], []], [1]], [-1]],
        [[[[2, 3], []], [1]], [1]],

        [[[[2, 3], [4]], []], []],
        [[[[2, 3], [4]], []], [-1]],
        [[[[2, 3], [4]], []], [1]],

        [[[[2, 3], [4]], [1]], []],
        [[[[2, 3], [4]], [1]], [-1]],
        [[[[2, 3], [4]], [1]], [1]],

        [[[[1, 2, 3], []], []], []],
        [[[[1, 2, 3], []], []], [-1]],
        [[[[1, 2, 3], []], []], [1]],

        [[[[1, 2, 3], []], [1]], []],
        [[[[1, 2, 3], []], [1]], [-1]],
        [[[[1, 2, 3], []], [1]], [1]],

        [[[[1, 2, 3], [4]], []], []],
        [[[[1, 2, 3], [4]], []], [-1]],
        [[[[1, 2, 3], [4]], []], [1]],

        [[[[1, 2, 3], [4]], [1]], []],
        [[[[1, 2, 3], [4]], [1]], [-1]],
        [[[[1, 2, 3], [4]], [1]], [1]],
    ]
    got = util.unique_list_pairs(
        util.unique_list_pairs(
            util.unique_list_pairs(
                util.unique_combinations(player_roll),
                util.unique_combinations(bonus_roll)
            ),
            util.unique_combinations(plus_two)
        ),
        util.unique_combinations(market, 1)
    )

    assert got == expected

def test_list_minus():
    list1 = [1, 1, 1]
    list2 = [1]
    assert util.list_minus(list1, list2) == [1, 1]

    list1 = [1, 2, 3]
    list2 = [2, 3]
    assert util.list_minus(list1, list2) == [1]

    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    assert util.list_minus(list1, list2) == []

def test_pick_best():
    input = [(10, "fred"), (5, "george"), (3, "ron")]
    got = util.pick_best(input)
    assert got == (10, "fred")

    input = [(1, "fred"), (5, "george"), (3, "ron")]
    got = util.pick_best(input)
    assert got == (5, "george")

    input = [(-1, "fred"), (-5, "george"), (-3, "ron")]
    got = util.pick_best(input)
    assert got == (-1, "fred")
