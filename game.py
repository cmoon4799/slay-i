from round_state import RoundState
from characters.character import Player, PlayerType

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


round_state = RoundState()


# generate map (enemies for each room, etc)

# create character
player = Player(
    PlayerType.IRONCLAD,
    [],  # potions
    [],  # relics
    [],  # deck
    0,  # gold
)

# starter relic
# filter relics_by_rarity based on player class
