from enum import Enum, auto
from round_state import RoundState

"""
mechanics to consider...
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
forethought - put a card from your hand to the bottom of your draw pile, costs 0 until player

NOTES:
* AOE damage is stil considered sequential in the action queue, i.e. if there are 3 enemies, 3 Damage actions will be enqueued. Important if each enemy has thorns, so each tick of damage must be separate.
* 
"""


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


class CardClass(Enum):
    IRONCLAD = auto()
    SILENT = auto()
    DEFECT = auto()
    WATCHER = auto()
    COLORLESS = auto()


class Card:
    def __init__(
        self,
        name,
        description,
        cost,  # -1 if cost is X cost
        card_type: CardType,
        card_rarity: CardRarity,
        card_class: CardClass,
        targeted: bool,  # used to prompt the user to select target
    ):
        self.name = name
        self.description = description
        self.cost = cost
        self.type = card_type
        self.card_rarity = card_rarity
        self.card_class = card_class
        self.targeted = targeted

        self.upgraded = False
        self.description = ""
        self.exhaust = False
        self.retain = False
        self.ethereal = False

    def get_card_info_string(self):
        return "{} ({}) | Cost: {} | Type: {} | Rarity: {}"

    def play_card(self, target, round_state):
        raise NotImplementedError("Each card must define its play behavior.")

    def upgrade(self):
        """Upgrade the card's effects or stats."""
        self.upgraded = True
        # Implement upgrade logic in subclass or override this

    def make_copy(self):
        """Return a new instance of the same card (e.g., for cloning)."""
        return (
            self.__class__()
        )  # Assuming each card can be initialized without args or has its own override

    def is_playable(self, round_state: RoundState):
        """Check if the card can be played (enough energy, etc)."""
        return round_state.player.energy >= self.cost

    def __str__(self):
        return f"{self.name} ({self.type.name}) - Cost: {self.cost}"
