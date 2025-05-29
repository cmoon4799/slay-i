from enum import Enum, auto
from actions import Damage, Block, Condition
from __future__ import annotations
from math import floor

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

NOTES
* Weak and Vulnerable are rounded down
* Strength is added to calculation first before other modifiers (Vulnerable, Weak, Wrath, Divinity)

"""


class ConditionType(Enum):
    # buffs
    ARTIFACT = auto()
    BARRICADE = auto()
    BUFFER = auto()
    METALLICIZE = auto()
    THORNS = auto()
    PLATED_ARMOR = auto()

    DEXTERITY = auto()
    DEXTERITY_DELTA = auto()
    STRENGTH = auto()
    STRENGTH_DELTA = auto()  # Ritual, Demon Form, ...

    POISON = auto()

    FRAIL = auto()
    VULNERABLE = auto()
    WEAK = auto()  # rounded down


class ConditionModifierType(Enum):
    FRAIL_MODIFIER = auto()
    VULNERABLE_MODIFIER = auto()
    WEAK_MODIFIER = auto()


class Character:
    def __init__(self, name, max_health):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.block = 0
        self._default_conditions = {
            condition_type: 0 for condition_type in ConditionType
        }
        self._default_condition_modifiers = {
            ConditionModifierType.FRAIL_MODIFIER: 0.25,
            ConditionModifierType.VULNERABLE_MODIFIER: 0.5,
            ConditionModifierType.WEAK_MODIFIER: 0.25,
        }
        self.conditions = self._default_conditions.copy()
        self.condition_modifiers = self._default_condition_modifiers.copy()

    def get_state_string(self):
        out = """
        {} | HEALTH: {}/{} | CONDITIONS: {}
        """.format(
            self.name,
            self.health,
            self.max_health,
            ", ".join(
                [
                    "{}: {}".format(condition, self.conditions[condition])
                    for condition in self.conditions
                    if self.conditions[condition] > 0
                ]
            ),
        )
        return out

    # reset block and condition at round start or round end
    def reset(self):
        self.block = 0
        self.conditions = self._default_conditions.copy()
        self.condition_modifiers = self._default_condition_modifiers.copy()

    # Damage, Block, Condition
    def receive_targeted_action(self, action):
        if isinstance(action, Damage):
            self.receive_damage(action)
        elif isinstance(action, Block):
            self.receive_block(action)
        elif isinstance(action, Condition):
            self.receive_condition(action)

    # receive attack from opponent
    def receive_damage(self, damage):
        pass

    # receive effect from opponent
    def receive_condition():
        pass

    def calculate_damage(self, target: Character, base_damage: int) -> int:
        strength = self.conditions[ConditionType.STRENGTH]
        damage = base_damage + strength

        if ConditionType.WEAK in self.conditions:
            damage = floor(
                damage
                * (1 - self.condition_modifiers[ConditionModifierType.WEAK_MODIFIER])
            )

        if target.conditions[ConditionType.VULNERABLE] > 1:
            damage = floor(
                damage
                * (
                    1
                    + target.condition_modifiers[
                        ConditionModifierType.VULNERABLE_MODIFIER
                    ]
                )
            )

        return max(0, damage)
