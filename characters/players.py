from enum import Enum, auto
from characters.character import Character
from collections import defaultdict

"""
TODO
add typings to parameters

"""


class Player(Character):
    def __init__(self, type, potions, relics, deck, gold, base_energy):
        self.type = type
        self.potions = potions
        self.relics = relics
        self.deck = deck
        self.gold = gold
        self.energy = 0
        self.base_energy = base_energy

    def reset(self):
        self.energy = 0

    def gain_relic(self, relic):
        pass

    def remove_relic(self, relic):
        pass


class Ironclad(Player):
    pass
