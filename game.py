from round_state import RoundState, EncounterType
from characters.players import Ironclad
from characters.enemies import JawWorm
from abstract_player import ConsolePlayer

"""
map
    question mark
    merchant
    treasure
    rest
    enemy
    elite
        super elite

later...
timer
ascension modes
"""

# generate map (enemies for each room, etc)

# create character
player = Ironclad()
enemies = [JawWorm()]
round_state = RoundState(
    player_interface=ConsolePlayer(),
    player=player,
    enemies=enemies,
    encounter_type=EncounterType.HALLWAY,
)

round_state.process_action_queue()

# starter relic
# filter relics_by_rarity based on player class
