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
