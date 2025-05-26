from enum import Enum, auto
from characters.character import Character


class Player(Character):
    def __init__(self, type, potions, relics, deck, gold, starting_energy):
        self.type = type
        self.potions = potions
        self.relics = relics
        self.deck = deck
        self.gold = gold
        self.starting_energy = starting_energy


class Ironclad(Player):
    pass
