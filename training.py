from typing import List, Dict

import kingsburg

def state_to_input(s: kingsburg.State) -> List[int]:
    """
    Transform a game state into a list of integers that can be
    fed into a neural net as inputs.
    """
    input: List[int] = []

    # There should be a 0 or 1 for every year/phase combination.
    # Only the current year/phase should be set as 1.
    # There are 5 years and 8 phases, so this should produce 40 ints.
    phases: List[int] = []
    for year in range(1, kingsburg.MAX_YEAR+1):
        # TODO this is weird.
        for phase in range(1, kingsburg.MAX_PHASE+1+1):
            if year == s.year and phase == s.phase:
                phases.append(1)
            else:
                phases.append(0)
    assert len(phases) == 40
    assert len([p for p in phases if p == 1]) == 1
    input = input + phases

    for p in [p for p in s.playerList() if p.name == "fred"]:
        input = input + player_to_input(p)

    # TODO make sure these are always ordered the same way
    for p in [p for p in s.playerList() if p.name != "fred"]:
        input = input + player_to_input(p)

    assert len(input) == 376

    return input

def player_to_input(p: kingsburg.PlayerState) -> List[int]:
    """
    Transform a player state into a list of integeres that can be
    fed into a neural net as inputs.
    """
    input: List[int] = []

    # These available benefits are simple booleans.
    input.append(int(p.has_kings_favor_bonus_die))
    input.append(int(p.has_kings_envoy))

    # Represent the number of plustwo tokens as a list of booleans.
    # Only represents up to ten plustwo tokens, because most likely
    # having more than ten is not very different from having ten.
    plustwo_tokens: List[int] = []
    for i in range(0, 10):
        if i+1 <= p.plustwo_tokens:
            plustwo_tokens.append(1)
        else:
            plustwo_tokens.append(0)
    assert len(plustwo_tokens) == 10
    input = input + plustwo_tokens

    # Represent each building as a boolean.
    buildings: List[int] = []
    for row in kingsburg.PROVINCE_SHEET:
        for b in row:
            buildings.append(int(b in p.buildings))
    assert len(buildings) == 20
    input = input + buildings

    # Represent the number of each resource as a list of booleans.
    # Only represents up to twenty of each resource, beacause most likely
    # having more than twenty of a resource is not very different from
    # having twenty.
    resources: List[int] = []
    for r in kingsburg.RESOURCES:
        for i in range(0, 20):
            if i+1 <= p.resources[r]:
                resources.append(1)
            else:
                resources.append(0)
    assert len(resources) == 60
    input = input + resources

    # Represent the number of solidiers as a list of booleans.
    # It is possible to have more than nine soldiers even though the board
    # only shows nine spaces. We only represent up to twenty soldiers,
    # because most likely having more than twenty soliders is not very
    # different from having twenty.
    soldiers: List[int] = []
    for i in range(0, 20):
        if i+1 <= p.soldiers:
            soldiers.append(1)
        else:
            soldiers.append(0)
    assert len(soldiers) == 20
    input = input + soldiers

    assert len(input) == 112

    return input

def advisor_choice_to_input(s: kingsburg.State, influence: kingsburg.AdvisorInfluence) -> List[int]:
    input: List[int] = []

    # First we'll represent the choice that was made...

    # There should be a 1 or 0 for each advisor. The chosen advisor should
    # be a 1 and all others should be 0.
    score = influence.advisorScore()
    advisors: List[int] = []
    for i in range(0, 18):
        if i+1 == score:
            advisors.append(1)
        else:
            advisors.append(0)
    assert len(advisors) == 18
    assert len([a for a in advisors if a == 1]) <= 1
    input = input + advisors

    # Whether a plustwo token was used is a boolean.
    input.append(int(influence.plus_two))

    # Market modifier is an integer from -1 to 1.
    input.append(influence.market_modifier)

    # There can be up to three player dice used. Each one is represented
    # as a list of integers.
    player_dice: List[int] = []
    for i in range(0, 3):
        if len(influence.player_dice) >= i+1:
            player_dice = player_dice + dice_to_input(influence.player_dice[i])
        else:
            player_dice = player_dice + dice_to_input(0)
    assert len(player_dice) == 18
    input = input + player_dice
    
    # There can be up to two bonus dice used. Each one is represented as
    # a list of integers.
    bonus_dice: List[int] = []
    for i in range(0, 2):
        if len(influence.bonus_dice) >= i+1:
            bonus_dice = bonus_dice + dice_to_input(influence.bonus_dice[i])
        else:
            bonus_dice = bonus_dice + dice_to_input(0)
    assert len(bonus_dice) == 12
    input = input + bonus_dice

    # Next we'll represent the dice that each player has rolled and not
    # used yet. Each player may have up to three player dice and two bonus dice.
    remaining_dice: List[int] = []

    # First the AI player.
    for p in [p for p in s.playerList() if p.name == "fred"]:
        for i in range(0, 3):
            if len(p.dice.player_dice) >= i+1:
                remaining_dice = remaining_dice + dice_to_input(p.dice.player_dice[i])
            else:
                remaining_dice = remaining_dice + dice_to_input(0)
        for i in range(0, 2):
            if len(p.dice.bonus_dice) >= i+1:
                remaining_dice = remaining_dice + dice_to_input(p.dice.bonus_dice[i])
            else:
                remaining_dice = remaining_dice + dice_to_input(0)

    # Then all the other players.
    for p in [p for p in s.playerList() if p.name != "fred"]:
        for i in range(0, 3):
            if len(p.dice.player_dice) >= i+1:
                remaining_dice = remaining_dice + dice_to_input(p.dice.player_dice[i])
            else:
                remaining_dice = remaining_dice + dice_to_input(0)
        for i in range(0, 2):
            if len(p.dice.bonus_dice) >= i+1:
                remaining_dice = remaining_dice + dice_to_input(p.dice.bonus_dice[i])
            else:
                remaining_dice = remaining_dice + dice_to_input(0)

    assert len(remaining_dice) == 90
    input = input + remaining_dice

    assert len(input) == 140

    return input

def dice_to_input(die: int) -> List[int]:
    input: List[int] = []
    for i in range(0, 6):
        if i+1 == die:
            input.append(1)
        else:
            input.append(0)
    assert len(input) == 6
    assert len([d for d in input if input == 1]) <= 1
    return input
