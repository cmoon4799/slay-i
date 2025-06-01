from __future__ import annotations
from enum import Enum, auto
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
        out = "{} | HEALTH: {}/{} | CONDITIONS: {}".format(
            self.name,
            self.health,
            self.max_health,
            ", ".join(
                [
                    "{}: {}".format(condition.name, self.conditions[condition])
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

    # receive attack from opponent
    def receive_damage(self, damage):
        pass

    # receive effect from opponent
    def receive_condition():
        pass

    def calculate_block(self, block) -> int:
        dexterity = self.conditions[ConditionType.DEXTERITY]
        base_block = block.block + dexterity

        if self.conditions[ConditionType.FRAIL] > 0:
            base_block = floor(
                base_block
                * (1 - self.condition_modifiers[ConditionModifierType.FRAIL_MODIFIER])
            )

        return max(0, base_block)

    def receive_block(self, block, battle):
        self.block += self.calculate_block(block)

    def calculate_damage(self, damage) -> int:
        strength = self.conditions[ConditionType.STRENGTH]
        base_damage = damage.damage + strength

        if self.conditions[ConditionType.WEAK] > 0:
            base_damage = floor(
                base_damage
                * (1 - self.condition_modifiers[ConditionModifierType.WEAK_MODIFIER])
            )

        print("vulnerable: ",
              damage.target.conditions[ConditionType.VULNERABLE])
        if damage.target.conditions[ConditionType.VULNERABLE] > 0:
            base_damage = floor(
                base_damage
                * (
                    1
                    + damage.target.condition_modifiers[
                        ConditionModifierType.VULNERABLE_MODIFIER
                    ]
                )
            )

        return max(0, base_damage)

    def receive_damage(self, damage, battle):
        damage = self.calculate_damage(damage)

        block, damage = max(self.block - damage,
                            0), max(damage - self.block, 0)
        self.block = block

        if damage > 0:
            # hook in torii and tungsten rod
            pass

        self.health -= damage

    def receive_condition(self, condition, battle):
        for condition_type, amount in condition.condition.items():
            self.conditions[condition_type] += amount
