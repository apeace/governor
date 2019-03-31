import game

# TODO add Pycharm type annotations
# TODO propagate messages from gamestate
# convert non-methods to this_case
# rename bonusDie to has_bonus_die
# TODO engine take free resource
# TODO randomengine

##############################################
# State
##############################################

def test_set_players():
    state = game.State().setPlayers(["fred", "george"])
    assert len(state.players) == 2

def test_next_year():
    state = game.State()
    assert state.year == 1
    state = state.nextYear()
    assert state.year == 2

    state.year = game.MAX_YEAR
    state = state.nextYear()
    assert state.over

def test_next_phase():
    state = game.State().nextPhase()
    assert state.year == 1
    assert state.phase == 1

    state.phase = game.MAX_PHASE
    state = state.nextPhase()
    assert state.year == 2
    assert state.phase == 0

    state.year = game.MAX_YEAR
    state.phase = game.MAX_PHASE
    state = state.nextPhase()
    assert state.year == game.MAX_YEAR
    assert state.phase == game.MAX_PHASE
    assert state.over

def test_take_free_resource():
    state = game\
        .State()\
        .setPlayers(["fred", "george"])\
        .takeFreeResource("fred", game.RESOURCE_GOLD)
    assert state.players["fred"].resources[game.RESOURCE_GOLD] == 1

def test_kings_favor__tie():
    state = game.State().setPlayers(["fred", "george"])
    result = state.kingsFavor()
    assert result == game.KINGS_FAVOR_TIE

def test_kings_favor__fewest_buildings():
    state = game\
        .State()\
        .setPlayers(["fred", "george"])\
        .giveBuilding("fred", game.BUILDING_STATUE)
    assert not state.players["fred"].bonusDie
    assert not state.players["george"].bonusDie

    state = state.kingsFavor()
    assert state.players["george"].bonusDie
    assert not state.players["fred"].bonusDie

##############################################
# PlayerState
##############################################

def test_add_resources():
    player = game.PlayerState("fred").addResources({
        game.RESOURCE_GOLD: 1,
        game.RESOURCE_WOOD: 2,
        game.RESOURCE_STONE: 3
    })
    assert player.resources[game.RESOURCE_GOLD] == 1
    assert player.resources[game.RESOURCE_WOOD] == 2
    assert player.resources[game.RESOURCE_STONE] == 3

def test_add_building():
    player = game.PlayerState("fred").addBuilding(game.BUILDING_STATUE)
    assert len(player.buildings) == 1

    player = player.addBuilding(game.BUILDING_CHAPEL)
    assert len(player.buildings) == 2
    assert player.buildings[0] == game.BUILDING_STATUE
    assert player.buildings[1] == game.BUILDING_CHAPEL

def test_add_bonus_die():
    player = game.PlayerState("fred").addBonusDie()
    assert player.bonusDie