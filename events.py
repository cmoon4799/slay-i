from enum import Enum, auto
from typing import Callable, Dict

from characters.character import EffectType


class EventType(Enum):
    PLAYER_DAMAGE = auto()
    ENEMY_DAMAGE = auto()
    DRAW_CARD = auto()
    ROUND_START = auto()
    ROUND_END = auto()
    TURN_START = auto()
    TURN_END = auto()


class Event:
    def __init__(self, event_type: EventType):
        self.event_type = event_type


class Intent(Enum):
    ATTACK = auto()
    ATTACK_DEFEND = auto()
    DEFEND_BUFF = auto()


class Attack:
    def __init__(
        self,
        name,
        base_damage,
        hit_count,
        intent: Intent,  # for enemy attack
    ):
        self.name = name
        self.base_damage = base_damage
        self.hit_count = hit_count
        self.intent = intent


class Target(Enum):
    ALL = auto()
    SINGLE = auto()
    NONE = auto()


class Effect:
    default_effects = {
        effect_type: 0 for effect_type in EffectType
    }
    default_effects.update({
        EffectType.FRAIL_MODIFIER: .25,
        EffectType.VULNERABLE_MODIFIER: .5,
        EffectType.WEAK_MODIFIER: .25,
    })
    # represents both the state of a character's effects and a move that applies effects

    def __init__(self, name, effect: Dict[EffectType, int], target: Target):
        self.name = name
        self.effect = Effect.default_effects.copy()
        self.effect.update(effect)
        self.target = target
        pass
