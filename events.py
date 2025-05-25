from enum import Enum, auto
from typing import Callable, Dict

from characters.character import EffectType
from characters.enemies import EnemyIntent


class EventType(Enum):
    PLAYER_DAMAGE = auto()
    ENEMY_DAMAGE = auto()
    DRAW_CARD = auto()
    ROUND_START = auto()
    ROUND_END = auto()
    TURN_START = auto()
    TURN_END = auto()
    PLAY_CARD = auto()
    PLAY_ATTACK = auto()
    PLAY_SKILL = auto()
    PLAY_POWER = auto()
    RECEIVE_ATTACK = auto()
    RECEIVE_DAMAGE = auto()


class Event:
    def __init__(self, event_type: EventType):
        self.event_type = event_type


"""
things that can be represented as Attack...
attack card
enemy attack move

should we subclass EnemyAttack?
then the target it always clear? no, because enemies can attack other enemies
i guess the only difference is intent?


targeting...
i suppose a specific enemy is always selected through the menu
what if you play a card that targets all? would you then use a list?
if you use a list then you need access to RoundState
enum doesn't really work because you need to be specific

if it's an array of indices to specify target, how do you specify a cleric using a skill on the knight?
do we assume strict ordering? [0, 1, 2] <- player, centurion, mystic
probably have to


"""


class Attack(Event):
    """Represents any source of direct damage, e.g. potions, card, enemy attack"""

    def __init__(
        self,
        name,
        base_damage,
        hit_count,
        intent: EnemyIntent,
        event_type: EventType,
        effect={},
    ):
        super().__init__(event_type)
        self.name = name
        self.base_damage = base_damage
        self.hit_count = hit_count
        self.intent = intent
        self.effect = effect


# class Skill:
#     """By definition, does not do direct damage"""

#     def __init__(
#         self,
#         name,

#     )


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
