from enum import Enum, auto


class CardType(Enum):
    ATTACK = auto()
    SKILL = auto()
    POWER = auto()
    STATUS = auto()
    CURSE = auto()


class CardRarity(Enum):
    BASIC = auto()
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    SPECIAL = auto()


class CardTarget(Enum):
    ALL = auto()
    SINGLE = auto()
    NONE = auto()


class Card:
    def __init__(self, name, cost, card_type: CardType, rarity: CardRarity, target: CardTarget, damage, vulnerable, weak):
        self.name = name
        self.cost = cost
        self.type = card_type
        self.rarity = rarity
        self.target = target

        self.damage = damage
        self.vulnerable = vulnerable
        self.weak = weak

        '''
        anger - add a copy of this card
        armaments - upgrade a card in your hand
        body slam - deal damage equal to your block
        clash - can only be played if every card in your hand is an attack
        sword boomerang - deal 3 damage to a random enemy 3 times
        wild strike - deal 12 damage, shuffle a wound into your draw pile
        blood for blood - costs 1 less for each time you lose hp
        searing blow - can be upgraded any number of times
        sever soul - exhaust all non-attack cards in your hand
        feed - if fatal, raise your max hp by 3
        '''

        self.upgraded = False
        self.description = ""
        self.exhaust = False
        self.retain = False
        self.ethereal = False

    def play(self, character, round_state, target):
        """Execute the effect of the card."""
        raise NotImplementedError("Each card must define its play behavior.")

    def upgrade(self):
        """Upgrade the card's effects or stats."""
        self.upgraded = True
        # Implement upgrade logic in subclass or override this

    def make_copy(self):
        """Return a new instance of the same card (e.g., for cloning)."""
        return self.__class__()  # Assuming each card can be initialized without args or has its own override

    def is_playable(self, player):
        """Check if the card can be played (enough energy, etc)."""
        return player.energy >= self.cost

    def __str__(self):
        return f"{self.name} ({self.type.name}) - Cost: {self.cost}"
