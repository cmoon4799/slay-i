from enum import Enum, auto
from typing import Callable, Dict, List

from characters.character import ConditionType, Character

# some actions should be processed with no callbacks
# events such as "end turn" should be processed with callbacks


class ActionType(Enum):
    # EVENTS
    ROUND_START = auto()
    ROUND_END = auto()
    TURN_START = auto()
    DRAW_CARD = auto()
    SHUFFLE_DISCARD_PILE = auto()
    EXHAUST_CARD = auto()
    PLAY_CARD = auto()
    PLAY_ATTACK = auto()
    PLAY_SKILL = auto()
    PLAY_POWER = auto()
    PLAY_POTION = auto()
    TURN_END = auto()
    RECEIVE_ATTACK = auto()

    DISPLAY_CHOICES = auto()

    # TARGETED ACTIONS
    DAMAGE = auto()
    BLOCK = auto()
    CONDITION = auto()


class Action:
    def __init__(self, type: ActionType):
        self.type = type


class CharacterTarget(Enum):
    ALL_ENEMIES = auto()
    PLAYER = auto()
    SINGLE = auto()
    SELF = auto()


class TargetedMove(Action):
    """
        A Move can encapsulate anything from a card to a potion. The difference between a Move and a TargetedMove is that:

        1) A TargetedMove has its targets resolved to instances of Character(s). A Move's source and taret is intentionally defined generically. For example, the card Whirlwind does AOE damage to all enemies; its Move target is defined as GenericTarget.ENEMIES_ALL but its TargetedMove records the Character instance of source and target.
        2) While a card like Whirlwind is defined to target all enemies, an AOE attack can be considered as a succession of single target attacks. That is, a Move target is defined as GenericTarget.ENEMIES_ALL but when played against 3 enemies, it is resolved to 3 instances of TargetedMoves, each with a single instance of an Enemy target.
    """

    def __init__(self, source: Character, target: Character):
        self.source = source
        self.target = target


class Damage(TargetedMove):
    """
        Any source of direct damage, e.g. potions, card, enemy attack
    """

    def __init__(
        self,
        damage,
        source,
        target,
    ):
        super().__init__(source, target)
        self.damage = damage


class Block(TargetedMove):
    def __init__(
        self,
        block,
        source,
    ):
        super().__init__(source, source)  # block is always(?) self targeted
        self.block = block


class Condition(TargetedMove):
    def __init__(
        self,
        condition: Dict[ConditionType, int],
        source,
        target,
    ):
        super().__init__(source, target)
        self.condition = condition
