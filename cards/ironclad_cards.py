from cards.cards import Card, CardType, CardRarity, CardCategory
from actions import Damage, Condition, Block
from characters.character import ConditionType


"""
NOTE
* do we need to specify where the source of damage or block comes from?
    probably? 

"""


class Defend(Card):
    def __init__(self):
        super().__init__(
            name="DEFEND",
            description="Gain 5 Block.",
            cost=1,
            type=CardType.SKILL,
            rarity=CardRarity.BASIC,
            category=CardCategory.IRONCLAD,
            targeted=False,
        )

    def play_card(self, target, round_state):
        return [
            Block(
                block=5,
                source=round_state.player,
            )
        ]


class Strike(Card):
    def __init__(self):
        super().__init__(
            name="STRIKE",
            description="Deal 6 damage.",
            cost=1,
            type=CardType.ATTACK,
            rarity=CardRarity.BASIC,
            category=CardCategory.IRONCLAD,
            targeted=True,
        )

    def play_card(self, target, round_state):
        return [
            Damage(
                damage=6,
                source=round_state.player,
                target=target,
            ),
        ]


class Bash(Card):
    def __init__(self):
        super().__init__(
            name="BASH",
            description="Deal 8 damage. Apply 2 Vulnerable.",
            cost=2,
            type=CardType.ATTACK,
            rarity=CardRarity.BASIC,
            category=CardCategory.IRONCLAD,
            targeted=True,
        )

    def play_card(self, target, round_state):
        return [
            Damage(
                damage=8,
                source=round_state.player,
                target=target,
            ),
            Condition(
                condition={
                    ConditionType.VULNERABLE: 2,
                },
                target=target,
            ),
        ]


class Whirlwind(Card):
    def __init__(self):
        self.damage = 5
        super().__init__(
            name="WHIRLWIND",
            description="Deal 5 damage to ALL enemies X times.",
            cost=0,
            type=CardType.ATTACK,
            rarity=CardRarity.UNCOMMON,
            category=CardCategory.IRONCLAD,
            targeted=False,
        )

    def play_card(self, target, round_state):
        return [
            Damage(
                damage=self.damage,
                source=round_state.player,
                target=enemy,
            )
            for enemy in round_state.enemies
        ] * round_state.player.energy
