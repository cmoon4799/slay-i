from enum import Enum, auto
from actions import Damage, Block, Condition

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

"""


class ConditionType(Enum):
    DEXTERITY = auto()
    DEXTERITY_DELTA = auto()
    STRENGTH = auto()
    STRENGTH_DELTA = auto()

    POISON = auto()
    FRAIL = auto()
    VULNERABLE = auto()
    WEAK = auto()  # rounded down

    FRAIL_MODIFIER = auto()
    VULNERABLE_MODIFIER = auto()
    WEAK_MODIFIER = auto()


class Character:
    def __init__(self):
        self.block = 0
        self._default_conditions = {
            condition_type: 0 for condition_type in ConditionType
        }
        self._default_conditions.update(
            {
                ConditionType.FRAIL_MODIFIER: 0.25,
                ConditionType.VULNERABLE_MODIFIER: 0.5,
                ConditionType.WEAK_MODIFIER: 0.25,
            }
        )
        self.conditions = self._default_conditions.copy()

    # reset block and condition
    def reset(self):
        self.block = 0
        self.conditions = self._default_conditions.copy()

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
