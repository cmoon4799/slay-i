from enum import Enum, auto
from characters.character import Character


class PlayerType(Enum):
    IRONCLAD = auto()


class Player(Character):
    potions = []
    relics = []
    deck = []
    gold = 0

    def __init__(self, type, potions, relics, deck, gold):
        self.type = type
        self.potions = potions
        self.relics = relics
        self.deck = deck
        self.gold = gold
