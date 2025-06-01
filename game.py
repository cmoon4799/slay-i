from room.battle import RoundState, BattleType
from characters.players import Ironclad
from characters.enemies import JawWorm
from abstract_player import ConsolePlayer
from enum import Enum, auto
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
keys
"""


class GameState(Enum):
    PLAYER_TYPE = auto()
    FLOOR = auto()
    ACT = auto()
    POTIONS = auto()
    POTION_SLOT_SIZE = auto()
    GOLD = auto()
    RELICS = auto()
    DECK = auto()
    HEALTH = auto()
    MAX_HEALTH = auto()

    # SHOP
    SHOP_CARDS = auto()
    SHOP_RELICS = auto()


class Game:
    def __init__(self, player, player_interface, starting_room):
        # generate map (enemies for each room, etc)
        pass

        self.act = 1
        self.floor = 1
        self.player = player
        self.player_interface = player_interface
        self.room = starting_room

    def get_game_state(self):
        state = {
            GameState.PLAYER_TYPE: self.player.type,
            GameState.FLOOR: self.floor,
            GameState.ACT: self.act,
            GameState.POTIONS: self.player.potions,
            GameState.POTION_SLOT_SIZE: len(self.player.potions),
            GameState.GOLD: self.player.gold,
            GameState.RELICS: self.player.relics,
            GameState.DECK: self.player.deck,
            GameState.HEALTH: self.player.health,
            GameState.MAX_HEALTH: self.player.max_health,
        }

        state.update(self.room.get_room_state())
        return state

    def run_room_loop(self):
        while not self.room.is_over():
            self.room.process_action_queue()

            self.player_interface.render_state(
                self.room.type,
                self.room.get_state(),
            )
            self.player_interface.prompt_choice(self.room.get_choices())


# create character
player = Ironclad()
enemies = [JawWorm()]
battle = RoundState(
    player_interface=ConsolePlayer(),
    player=player,
    enemies=enemies,
    encounter_type=BattleType.HALLWAY,
)

battle.process_action_queue()

# starter relic
# filter relics_by_rarity based on player class
