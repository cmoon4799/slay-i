from enum import Enum, auto
from typing import Callable, Dict, List

from characters.character import ConditionType


class EventType(Enum):
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
    RECEIVE_DAMAGE = auto()  # necessary?


class Event:
    def __init__(self, event_type: EventType):
        self.event_type = event_type


class Source(Enum):
    CARD = auto()
    POTION = auto()
    CONDITION = auto()


class Target(Enum):
    ALL = auto()
    SINGLE = auto()
    NONE = auto()


class Damage:
    """Any source of direct damage, e.g. potions, card, enemy attack"""

    def __init__(
        self,
        name,
        damage,
        hit_count,
        source,
        target: List[int],
    ):
        self.name = name
        self.damage = damage
        self.hit_count = hit_count
        self.source = source
        self.target = target


class Block:
    def __init__(
        self,
        name,
        block,
        block_count,
        source,
        target: List[int],
    ):
        self.name = name
        self.block = block
        self.block_count = block_count
        self.source = source
        self.target = target


class Condition:
    def __init__(
        self,
        name,
        condition: Dict[ConditionType, int],
        source,
        target: List[int],
    ):
        self.name = name
        self.condition = {condition_type: 0 for condition_type in ConditionType}
        self.condition.update(
            {
                ConditionType.FRAIL_MODIFIER: 0.25,
                ConditionType.VULNERABLE_MODIFIER: 0.5,
                ConditionType.WEAK_MODIFIER: 0.25,
            }
        )
        self.condition.update(condition)
        self.source = source
        self.target = target


condition = Condition("blach", {}, 1, [1])

print(condition, type(condition))
