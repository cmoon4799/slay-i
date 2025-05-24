from enum import Enum, auto

"""
enemies operate similarly to players, base class can be the same

player inventory
    potions
        does fairy in the bottle work for non-combat rooms?
    relics
    deck
    gold
    keys (for later)

intensity debuffs...
    dexterity down: reduce dex by N every turn
    dexterity negative: decreases block gained from cards
    strength down
    strength negative
    poison
    shackled
        does not remove artifact stack
        exception with the heart?
    slow
        only applies to giant head atm
    hex: whenever you play a non-attack card, add X dazed to your draw pile

duration debuffs...
    frail: block gained from cards is reduced by 25%
    vulnerable
    weak

no stacks...
    no draw
        bullet time, battle trance
    entangled: no attack
        from red slaver
        

"""


class Combatant:
    # intensity debuffs
    dexterity_down = 0
    dexterity_negative = 0
    strength_down = 0
    strength_negative = 0
    poison = 0

    # duration debuffs
    frail = 0
    vulnerable = 0
    weak = 0

    # duration debuff constants
    FRAIL_MODIFIER = .25
    VULNERABLE_MODIFIER = .5
    WEAK_MODIFIER = .25

    def __init__(self):
        pass


class CharacterType(Enum):
    IRONCLAD = auto()


class Character(Combatant):
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


class EnemyType(Enum):
    pass


class Enemy(Combatant):
    def __init__(self, type):
        self.type = type
