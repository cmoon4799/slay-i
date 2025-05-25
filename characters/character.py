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

buffs...
    artifact
        artifact order? e.g. if an attack applies both weak and frail
        which one gets countered first?
    

intensity debuffs...
    dexterity down: reduce dex by N every turn
    dexterity negative: decreases block gained from cards
        - dexterity only works for cards that directly give buff
        does not work for powers and other buff-based cards
        - changes to dexterity are either for one turn or the entire round
        e.g. speed potion vs wraith form
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


class EffectType(Enum):
    DEXTERITY = auto()
    DEXTERITY_DELTA = auto()
    STRENGTH = auto()
    STRENGTH_DELTA = auto()

    POISON = auto()
    FRAIL = auto()
    VULNERABLE = auto()
    WEAK = auto()

    FRAIL_MODIFIER = auto()
    VULNERABLE_MODIFIER = auto()
    WEAK_MODIFIER = auto()


class Character:
    # intensity effects
    dexterity = 0
    dexterity_delta = 0
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

    block = 0

    def __init__(self):
        pass

    # receive attack from opponent
    def receive_attack():
        pass

    # receive effect from opponent
    def receive_effect():
        pass


class Attack:
    def __init__(
        self,
        name,
        base_damage,
        hit_count,
        intent,
        effects,  # buffs, debuffs
    ):
        self.name = name
        self.base_damage = base_damage
        self.hit_count = hit_count
        self.intent = intent
        self.effects = effects


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


class EnemyType(Enum):
    BOSS = auto()
    ELITE = auto()


class Enemy(Character):
    move_order = []

    def __init__(self, type):
        self.type = type

    def get_move(self):
        raise NotImplementedError("Each enemy must define its move behavior.")
