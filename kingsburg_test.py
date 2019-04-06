from typing import List

import kingsburg

##############################################
# Advisors
##############################################

def test_choices_rewards():
    advisor = kingsburg.ADVISOR[kingsburg.ADVISOR_JESTER]
    expected = [
        kingsburg.Reward(victory_points=1)
    ]
    got = advisor.choices__rewards({})
    assert got == expected

    advisor = kingsburg.ADVISOR[kingsburg.ADVISOR_MERCHANT]
    expected = [
        kingsburg.Reward(resources={kingsburg.RESOURCE_WOOD: 1}),
        kingsburg.Reward(resources={kingsburg.RESOURCE_GOLD: 1}),
    ]
    got = advisor.choices__rewards({})
    assert got == expected

    # Can't get rewards from alchemist if you have no resources.
    advisor = kingsburg.ADVISOR[kingsburg.ADVISOR_ALCHEMIST]
    expected = []
    got = advisor.choices__rewards({})
    assert got == expected

    # If you have two resources you should have two possible rewards.
    advisor = kingsburg.ADVISOR[kingsburg.ADVISOR_ALCHEMIST]
    expected = [
        kingsburg.Reward(resources={kingsburg.RESOURCE_WOOD: -1, kingsburg.RESOURCE_GOLD: 1, kingsburg.RESOURCE_STONE: 1}),
        kingsburg.Reward(resources={kingsburg.RESOURCE_GOLD: -1, kingsburg.RESOURCE_WOOD: 1, kingsburg.RESOURCE_STONE: 1}),
    ]
    got = advisor.choices__rewards({kingsburg.RESOURCE_GOLD: 1, kingsburg.RESOURCE_WOOD: 1})
    assert got == expected

    advisor = kingsburg.ADVISOR[kingsburg.ADVISOR_DUCHESS]
    expected = [
        kingsburg.Reward(resources={kingsburg.RESOURCE_GOLD: 2}, plustwos=1),
        kingsburg.Reward(resources={kingsburg.RESOURCE_STONE: 2}, plustwos=1),
        kingsburg.Reward(resources={kingsburg.RESOURCE_WOOD: 2}, plustwos=1),
        kingsburg.Reward(resources={kingsburg.RESOURCE_GOLD: 1, kingsburg.RESOURCE_WOOD: 1}, plustwos=1),
        kingsburg.Reward(resources={kingsburg.RESOURCE_GOLD: 1, kingsburg.RESOURCE_STONE: 1}, plustwos=1),
        kingsburg.Reward(resources={kingsburg.RESOURCE_STONE: 1, kingsburg.RESOURCE_WOOD: 1}, plustwos=1),
    ]
    got = advisor.choices__rewards({})
    assert got == expected

##############################################
# Die
##############################################

def test_productive_season_roll_total():
    roll = kingsburg.ProductiveSeasonRoll([1, 2, 3], [4])
    assert roll.totalValue() == 10

def test_advisor_influence_score():
    influence = kingsburg.AdvisorInfluence(
        [1, 2, 3],
        [4],
        plus_two=True,
        market_modifier=-1
    )
    assert influence.advisorScore() == 11

##############################################
# State
##############################################

def test_set_players():
    state = kingsburg.State().setPlayers(["fred", "george"])
    assert len(state.players) == 2

def test_next_year():
    state = kingsburg.State()
    assert state.year == 1
    state = state.nextYear()
    assert state.year == 2

    state.year = kingsburg.MAX_YEAR
    state = state.nextYear()
    assert state.over

def test_next_phase():
    state = kingsburg.State().nextPhase()
    assert state.year == 1
    assert state.phase == 1

    state.phase = kingsburg.MAX_PHASE
    state = state.nextPhase()
    assert state.year == 2
    assert state.phase == 0

    state.year = kingsburg.MAX_YEAR
    state.phase = kingsburg.MAX_PHASE
    state = state.nextPhase()
    assert state.year == kingsburg.MAX_YEAR
    assert state.phase == kingsburg.MAX_PHASE
    assert state.over

def test_take_free_resource():
    state = kingsburg \
        .State() \
        .setPlayers(["fred", "george"]) \
        .takeFreeResource("fred", kingsburg.RESOURCE_GOLD)
    assert state.players["fred"].resources[kingsburg.RESOURCE_GOLD] == 1

def test_kings_favor__tie():
    state = kingsburg.State().setPlayers(["fred", "george"])
    result = state.kingsFavor()
    assert result == kingsburg.KINGS_FAVOR_TIE

def test_kings_favor__fewest_buildings():
    state = kingsburg \
        .State() \
        .setPlayers(["fred", "george"]) \
        .giveBuilding("fred", kingsburg.BUILDING_STATUE, False)
    assert not state.players["fred"].has_kings_favor_bonus_die
    assert not state.players["george"].has_kings_favor_bonus_die

    state = state.kingsFavor()
    assert state.players["george"].has_kings_favor_bonus_die
    assert not state.players["fred"].has_kings_favor_bonus_die

def test_productive_season_rolls__no_tie():
    state = kingsburg.State().setPlayers(["fred", "george", "ron"])
    assert state.turn_order == ["fred", "george", "ron"]

    state = state.productiveSeasonRolls({
        "ron": kingsburg.ProductiveSeasonRoll([1, 1, 1], []),
        "fred": kingsburg.ProductiveSeasonRoll([2, 2, 2], []),
        "george": kingsburg.ProductiveSeasonRoll([3, 3, 3], [])
    })
    assert state.turn_order == ["ron", "fred", "george"]

def test_productive_season_rolls__tie():
    state = kingsburg.State().setPlayers(["fred", "george", "ron"])
    state.turn_order = ["ron", "fred", "george"]

    state = state.productiveSeasonRolls({
        "fred": kingsburg.ProductiveSeasonRoll([2, 2, 2], []),
        "george": kingsburg.ProductiveSeasonRoll([1, 1, 1], []),
        "ron": kingsburg.ProductiveSeasonRoll([2, 2, 2], [])
    })
    assert state.turn_order == ["george", "ron", "fred"]

def test_productive_season_rolls__tie2():
    state = kingsburg.State().setPlayers(["fred", "george", "ron"])
    state.turn_order = ["ron", "fred", "george"]

    state = state.productiveSeasonRolls({
        "fred": kingsburg.ProductiveSeasonRoll([3, 3, 3], []),
        "george": kingsburg.ProductiveSeasonRoll([2, 2, 2], []),
        "ron": kingsburg.ProductiveSeasonRoll([2, 2, 2], [])
    })
    assert state.turn_order == ["ron", "george", "fred"]

def test_productive_season_rolls__tie_bonus_die():
    state = kingsburg.State().setPlayers(["fred", "george", "ron"])
    state.turn_order = ["ron", "fred", "george"]

    state = state.productiveSeasonRolls({
        "fred": kingsburg.ProductiveSeasonRoll([2, 2, 1], [2]),
        "george": kingsburg.ProductiveSeasonRoll([1, 1, 1], []),
        "ron": kingsburg.ProductiveSeasonRoll([2, 2, 2], [1])
    })
    assert state.turn_order == ["george", "ron", "fred"]

##############################################
# PlayerState
##############################################

def test_add_resources():
    player = kingsburg.PlayerState("fred").addResources({
        kingsburg.RESOURCE_GOLD: 1,
        kingsburg.RESOURCE_WOOD: 2,
        kingsburg.RESOURCE_STONE: 3
    })
    assert player.resources[kingsburg.RESOURCE_GOLD] == 1
    assert player.resources[kingsburg.RESOURCE_WOOD] == 2
    assert player.resources[kingsburg.RESOURCE_STONE] == 3

def test_add_building():
    player = kingsburg.PlayerState("fred")\
        .addResources({kingsburg.RESOURCE_GOLD: 2, kingsburg.RESOURCE_WOOD: 1})\
        .addBuilding(kingsburg.BUILDING_STATUE, [])
    assert player.buildings == [kingsburg.BUILDING_STATUE]
    assert player.resources == {kingsburg.RESOURCE_GOLD: 0, kingsburg.RESOURCE_WOOD: 1, kingsburg.RESOURCE_STONE: 0}
    assert player.victory_points == 3

    player = player\
        .addResources({kingsburg.RESOURCE_GOLD: 3, kingsburg.RESOURCE_STONE: 1})\
        .addBuilding(kingsburg.BUILDING_CHAPEL, [])
    assert player.buildings == [kingsburg.BUILDING_STATUE, kingsburg.BUILDING_CHAPEL]
    assert player.resources == {kingsburg.RESOURCE_GOLD: 0, kingsburg.RESOURCE_WOOD: 1, kingsburg.RESOURCE_STONE: 0}
    assert player.victory_points == 8

def test_add_building__stable():
    player = kingsburg.PlayerState("fred") \
        .addBuilding(kingsburg.BUILDING_STABLE, [kingsburg.ADVISOR_GENERAL])
    assert player.soldiers == 1

def test_add_bonus_die():
    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie()
    assert player.has_kings_favor_bonus_die

def test_get_num_player_dice():
    player = kingsburg.PlayerState("fred")
    assert player.getNumPlayerDice(kingsburg.PHASE_SPRING) == 3

    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie()
    assert player.getNumPlayerDice(kingsburg.PHASE_SUMMER) == 3
    assert player.getNumPlayerDice(kingsburg.PHASE_SPRING) == 3

def test_get_num_bonus_dice():
    player = kingsburg.PlayerState("fred")
    assert player.getNumBonusDice(kingsburg.PHASE_SPRING) == 0

    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie()
    assert player.getNumBonusDice(kingsburg.PHASE_SPRING) == 1

    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie().addBuilding(kingsburg.BUILDING_FARMS, [])
    assert player.getNumBonusDice(kingsburg.PHASE_SPRING) == 2

def test_roll():
    roll = kingsburg.ProductiveSeasonRoll([1, 2, 3], [4])
    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie().roll(roll)
    assert player.dice.player_dice == [1, 2, 3]
    assert player.dice.bonus_dice == [4]
    assert not player.has_kings_favor_bonus_die

def test_choices_advisor_influence__simple():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
        ),
    ]
    assert player.choices_advisorInfluence(kingsburg.ADVISORS) == expected

def test_choices_advisor_influence__simple_with_taken():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
    ]
    assert player.choices_advisorInfluence([kingsburg.ADVISOR_JESTER]) == expected

def test_choices_advisor_influence__simple2():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 2, 3],
        bonus_dice=[],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[2],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[3],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 2],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 3],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[2, 3],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 2, 3],
            bonus_dice=[],
        ),
    ]
    assert player.choices_advisorInfluence(kingsburg.ADVISORS) == expected

def test_choices_advisor_influence__simple2_with_taken():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 2, 3],
        bonus_dice=[],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[3],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 2],
            bonus_dice=[],
        ),
    ]
    assert player.choices_advisorInfluence([kingsburg.ADVISOR_JESTER, kingsburg.ADVISOR_ARCHITECT]) == expected

def test_choices_advisor_influence__withbonus():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[1],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
        ),
    ]
    assert player.choices_advisorInfluence(kingsburg.ADVISORS) == expected
    
def test_choices_advisor_influence__insanebonus():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[6, 6, 6],
        bonus_dice=[6],
    ))
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[6],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[6],
            bonus_dice=[6],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[6, 6],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[6, 6],
            bonus_dice=[6],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[6, 6, 6],
            bonus_dice=[],
        ),
    ]
    assert player.choices_advisorInfluence(kingsburg.ADVISORS) == expected

def test_choices_advisor_influence__withbonus_withplustwo():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[1],
    ))
    player.plustwo_tokens = 1
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True
        ),
    ]
    assert player.choices_advisorInfluence(kingsburg.ADVISORS) == expected

def test_choices_advisor_influence__withbonus_withplustwo_withmarket():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[1],
    )).addBuilding(kingsburg.BUILDING_MARKET, [])
    player.plustwo_tokens = 1
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),
    ]

    got = player.choices_advisorInfluence(kingsburg.ADVISORS)

    assert got == expected

def test_choices_advisor_influence__withbonus_withplustwo_withmarket_excluded():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[1],
    )).addBuilding(kingsburg.BUILDING_MARKET, [])
    player.plustwo_tokens = 1
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            market_modifier=0
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=0
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=0
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=-1
        ),
    ]

    got = player.choices_advisorInfluence([kingsburg.ADVISOR_JESTER, kingsburg.ADVISOR_ARCHITECT])

    assert got == expected

def test_choices_advisor_influence__withbonus_withplustwo_withmarket_excluded_withkingsenvoy():
    player = kingsburg.PlayerState("fred").roll(kingsburg.ProductiveSeasonRoll(
        player_dice=[1, 1, 1],
        bonus_dice=[1],
    )).addBuilding(kingsburg.BUILDING_MARKET, [])
    player.plustwo_tokens = 1
    player.has_kings_envoy = True
    expected: List[kingsburg.AdvisorInfluence] = [
        kingsburg.ADVISOR_INFLUENCE_PASS,
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[],
            plus_two=True,
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            market_modifier=1
        ),

        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=0
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=-1
        ),
        kingsburg.AdvisorInfluence(
            player_dice=[1, 1, 1],
            bonus_dice=[1],
            plus_two=True,
            market_modifier=1
        ),
    ]

    got = player.choices_advisorInfluence([kingsburg.ADVISOR_JESTER, kingsburg.ADVISOR_ARCHITECT])

    assert got == expected

def test_spenddice():
    player = kingsburg.PlayerState("fred")\
        .roll(kingsburg.ProductiveSeasonRoll(
            player_dice=[1, 2, 3],
            bonus_dice=[4],
        ))\
        .addBuilding(kingsburg.BUILDING_MARKET, [])
    player.plustwo_tokens = 1

    influence = kingsburg.AdvisorInfluence(
        player_dice=[1],
        bonus_dice=[4],
        plus_two=True,
        market_modifier=-1
    )
    player = player.spendDice(influence)

    assert player.dice.player_dice == [2, 3]
    assert player.dice.bonus_dice == []
    assert player.plustwo_tokens == 0

def test_applyreward():
    player = kingsburg.PlayerState("fred").applyReward(kingsburg.Reward(
        victory_points=2,
        resources={kingsburg.RESOURCE_STONE: 1},
        soldiers=2,
        plustwos=2,
    ))

    assert player.victory_points == 2
    assert player.resources == {
        kingsburg.RESOURCE_STONE: 1,
        kingsburg.RESOURCE_WOOD: 0,
        kingsburg.RESOURCE_GOLD: 0
    }
    assert player.soldiers == 2
    assert player.plustwo_tokens == 2

    player = player.applyReward(kingsburg.Reward(
        victory_points=-1,
        resources={kingsburg.RESOURCE_STONE: -1, kingsburg.RESOURCE_WOOD: 1},
        soldiers=-1,
        plustwos=-1,
    ))

    assert player.victory_points == 1
    assert player.resources == {
        kingsburg.RESOURCE_STONE: 0,
        kingsburg.RESOURCE_WOOD: 1,
        kingsburg.RESOURCE_GOLD: 0
    }
    assert player.soldiers == 1
    assert player.plustwo_tokens == 1

def test_choices_buildings__rich():
    player = kingsburg.PlayerState("fred")\
        .addResources({kingsburg.RESOURCE_GOLD: 100, kingsburg.RESOURCE_WOOD: 100, kingsburg.RESOURCE_STONE: 100})\
        .addBuilding(kingsburg.BUILDING_BARRICADE, [])\
        .addBuilding(kingsburg.BUILDING_CRANE, [])
    choices = player.choices__buildings()

    expected = [
        kingsburg.BUILDING_STATUE,
        kingsburg.BUILDING_INN,
        kingsburg.BUILDING_GUARD_TOWER,
        kingsburg.BUILDING_PALISADE,
        kingsburg.BUILDING_TOWN_HALL,
        kingsburg.BUILD_PASS,
    ]
    assert choices == expected

def test_choices_buildings__broke():
    player = kingsburg.PlayerState("fred")
    choices = player.choices__buildings()

    assert choices == [kingsburg.BUILD_PASS]

def test_choices_buildings__limited():
    player = kingsburg.PlayerState("fred") \
        .addResources({kingsburg.RESOURCE_GOLD: 1, kingsburg.RESOURCE_WOOD: 4, kingsburg.RESOURCE_STONE: 1}) \
        .addBuilding(kingsburg.BUILDING_BARRICADE, []) \
        .addBuilding(kingsburg.BUILDING_CRANE, [])
    choices = player.choices__buildings()

    expected = [
        kingsburg.BUILDING_INN,
        kingsburg.BUILDING_PALISADE,
        kingsburg.BUILD_PASS,
    ]
    assert choices == expected
