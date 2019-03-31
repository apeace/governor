def lowest(members):
    """
    Given a dict, returns the key with the lowest value.
    If there is a tie for lowest value, returns None.
    """
    if len(members) == 0:
        return None

    reverse_members = {}
    min = None

    for member in members:
        reverse_members[members[member]] = member
        if min is None:
            min = members[member]
            continue
        if members[member] < min:
            min = members[member]

    lowest_member = None
    for member in members:
        if members[member] == min:
            if lowest_member is not None:
                return None
            lowest_member = member

    return lowest_member

def highest(members):
    """
    Given a dict, returns the key with the highest value.
    If there is a tie for highest value, returns None.
    """
    if len(members) == 0:
        return None

    reverse_members = {}
    max = None

    for member in members:
        reverse_members[members[member]] = member
        if max is None:
            max = members[member]
            continue
        if members[member] > max:
            max = members[member]

    highest_member = None
    for member in members:
        if members[member] == max:
            if highest_member is not None:
                return None
            highest_member = member

    return highest_member
