from typing import Dict, Optional

def lowest(members: Dict[str, int]):
    """
    Given a dict, returns the key with the lowest value.
    If there is a tie for lowest value, returns None.
    """
    if len(members) == 0:
        return None

    reverse_members: Dict[int, str] = {}
    min: Optional[int] = None

    for member in members:
        reverse_members[members[member]] = member
        if min is None:
            min = members[member]
            continue
        if members[member] < min:
            min = members[member]

    lowest_member: Optional[str] = None
    for member in members:
        if members[member] == min:
            if lowest_member is not None:
                return None
            lowest_member = member

    return lowest_member

def highest(members: Dict[str, int]):
    """
    Given a dict, returns the key with the highest value.
    If there is a tie for highest value, returns None.
    """
    if len(members) == 0:
        return None

    reverse_members: Dict[int, str] = {}
    max: Optional[int] = None

    for member in members:
        reverse_members[members[member]] = member
        if max is None:
            max = members[member]
            continue
        if members[member] > max:
            max = members[member]

    highest_member: Optional[str] = None
    for member in members:
        if members[member] == max:
            if highest_member is not None:
                return None
            highest_member = member

    return highest_member
