from enum import Enum, auto
from characters.character import Character
import cards.ironclad_cards as ironclad_cards
import copy
from actions import Damage

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
        out = "HEALTH: {}/{} | BLOCK: {} | ENERGY: {}/{}".format(
            self.health,
            self.max_health,
            self.block,
            self.energy,
            self.base_energy,
        )
        if any(self.conditions[condition] > 0 for condition in self.conditions):
            out += " | CONDITIONS: " + ", ".join(
                [
                    "{}: {}".format(condition, self.conditions[condition])
                    for condition in self.conditions
                    if self.conditions[condition] > 0
                ]
            )
        return out

    def reset(self):
        self.energy = 0

    def gain_relic(self, relic):
        pass

    def remove_relic(self, relic):
        pass

    def receive_damage(self, damage: Damage, battle):
        damage = self.calculate_damage(damage)

        block, damage = max(self.block - damage,
                            0), max(damage - self.block, 0)
        self.block = block

        if damage > 0:
            # hook in torii and tungsten rod
            pass

        self.health -= damage


IRONCLAD_STARTING_DECK = {
    ironclad_cards.Defend: 4,
    ironclad_cards.Strike: 5,
    ironclad_cards.Bash: 1,
}


class Ironclad(Player):
    def __init__(self):
        super().__init__(
            name="IRONCLAD",
            max_health=80,
            type=PlayerType.IRONCLAD,
            potions=[],
            relics=[],
            deck=[
                card_class()
                for card_class, count in IRONCLAD_STARTING_DECK.items()
                for _ in range(count)
            ],
            gold=99,
            base_energy=3,
        )
