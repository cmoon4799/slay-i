from enum import Enum, auto
from characters.character import Character
from collections import defaultdict
import cards.ironclad_cards as ironclad_cards
import copy

"""
TODO
* add typings to parameters
* Is name necessary? If not, can we remove name from Enemy as well?
"""


class PlayerType(Enum):
    IRONCLAD = auto()
    SILENT = auto()
    DEFECT = auto()
    WATCHER = auto()


class Player(Character):
    def __init__(
        self, name, max_health, type, potions, relics, deck, gold, base_energy
    ):
        super().__init__(name, max_health)
        self.type = type
        self.potions = potions
        self.relics = relics
        self.deck = deck
        self.gold = gold
        self.energy = 0
        self.base_energy = base_energy

    def get_state_string(self):
        out = "{} | HEALTH: {}/{} | ENERGY: {}/{} | CONDITIONS: {}".format(
            self.name,
            self.health,
            self.max_health,
            self.energy,
            self.base_energy,
            ", ".join(
                [
                    "{}: {}".format(condition, self.conditions[condition])
                    for condition in self.conditions
                    if self.conditions[condition] > 0
                ]
            ),
        )
        return out

    def reset(self):
        self.energy = 0

    def gain_relic(self, relic):
        pass

    def remove_relic(self, relic):
        pass


IRONCLAD_STARTING_DECK = [
    ironclad_cards.Defend() for _ in range(4)
] + [
    ironclad_cards.Strike() for _ in range(5)
] + [
    ironclad_cards.Bash()
]


class Ironclad(Player):
    def __init__(self):
        super().__init__(
            name="IRONCLAD",
            max_health=80,
            type=PlayerType.IRONCLAD,
            potions=[],
            relics=[],
            deck=copy.deepcopy(IRONCLAD_STARTING_DECK),
            gold=99,
            base_energy=3,
        )
