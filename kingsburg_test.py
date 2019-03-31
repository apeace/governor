import kingsburg

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
        .giveBuilding("fred", kingsburg.BUILDING_STATUE)
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
    player = kingsburg.PlayerState("fred").addBuilding(kingsburg.BUILDING_STATUE)
    assert len(player.buildings) == 1

    player = player.addBuilding(kingsburg.BUILDING_CHAPEL)
    assert len(player.buildings) == 2
    assert player.buildings[0] == kingsburg.BUILDING_STATUE
    assert player.buildings[1] == kingsburg.BUILDING_CHAPEL

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

    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie().addBuilding(kingsburg.BUILDING_FARMS)
    assert player.getNumBonusDice(kingsburg.PHASE_SPRING) == 2

def test_roll():
    roll = kingsburg.ProductiveSeasonRoll([1, 2, 3], [4])
    player = kingsburg.PlayerState("fred").addKingsFavorBonusDie().roll(roll)
    assert player.dice.player_dice == [1, 2, 3]
    assert player.dice.bonus_dice == [4]
    assert not player.has_kings_favor_bonus_die
