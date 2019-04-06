from typing import List, Dict

import kingsburg

def state_to_input(s: kingsburg.State) -> List[int]:
    """
    Transform a game state into a list of integers that can be
    fed into a neural net as inputs.
    """
    input: List[int] = []

    input.append(s.year)
    input.append(s.phase)

    for p in [p for p in s.playerList() if p.name == "fred"]:
        for val in player_to_input(p, s.turn_order, s.taken_advisors):
            input.append(val)

    for p in [p for p in s.playerList() if p.name != "fred"]:
        for val in player_to_input(p, s.turn_order, s.taken_advisors):
            input.append(val)

    return input

def player_to_input(p: kingsburg.PlayerState, turn_order: List[str], taken_advisors: Dict[kingsburg.AdvisorScore, List[str]]) -> List[int]:
    input: List[int] = []

    for i in range(len(turn_order)):
        if turn_order[i] == p.name:
            input.append(i)
            break

    input.append(int(p.has_kings_favor_bonus_die))
    input.append(int(p.has_kings_envoy))
    input.append(p.plustwo_tokens)
    input.append(int(p.used_plustwo_token))
    input.append(int(p.used_market))
    input.append(len(p.buildings))

    for row in kingsburg.PROVINCE_SHEET:
        for b in row:
            input.append(int(b in p.buildings))

    for r in kingsburg.RESOURCES:
        input.append(p.resources[r])

    for d in range(3):
        if len(p.dice.player_dice) > d:
            input.append(p.dice.player_dice[d])
        else:
            input.append(0)

    for d in range(2):
        if len(p.dice.bonus_dice) > d:
            input.append(p.dice.bonus_dice[d])
        else:
            input.append(0)

    input.append(p.victory_points)
    input.append(p.soldiers)

    for score in kingsburg.ADVISORS:
        if score in taken_advisors and p.name in taken_advisors[score]:
            input.append(1)
        else:
            input.append(0)

    return input
