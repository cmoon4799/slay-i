from cards.cards import Card, CardType, CardRarity, CardClass
from actions import Damage, Source, Condition, Block, CharacterTarget
from characters.character import ConditionType


"""
NOTE
* do we need to specify where the source of damage or block comes from?
    probably? 

"""


class Defend(Card):
    def __init__(self):
        self.name = "DEFEND"
        self.block_count = 1

        super().__init__(
            name=self.name,
            cost=1,
            card_type=CardType.ATTACK,
            card_rarity=CardRarity.BASIC,
            card_class=CardClass.IRONCLAD,
            targeted=False,
        )

    def _play_card(self, target, round_state):
        return [
            Block(
                block=5,
                source=round_state.player,
            )
        ]


class Strike(Card):
    def __init__(self):
        self.name = "STRIKE"

        super().__init__(
            name=self.name,
            cost=1,
            card_type=CardType.ATTACK,
            card_rarity=CardRarity.BASIC,
            card_class=CardClass.IRONCLAD,
            targeted=True,
        )

    def _play_card(self, target, round_state):
        return [
            Damage(
                damage=6,
                source=round_state.player,
                target=target,
            ),
        ]


class Bash(Card):
    def __init__(self):
        self.name = "BASH"
        super().__init__(
            name=self.name,
            cost=2,
            card_type=CardType.ATTACK,
            card_rarity=CardRarity.BASIC,
            card_class=CardClass.IRONCLAD,
        )

    def _play_card(self, target, round_state):
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
        self.name = "WHIRLWIND"
        self.damage = 5
        super().__init__(
            name=self.name,
            cost=0,
            card_type=CardType.ATTACK,
            card_rarity=CardRarity.UNCOMMON,
            card_class=CardClass.IRONCLAD,
            x_cost=True,
        )

    def _play_card(self, target, round_state):
        return [
            Damage(
                damage=self.damage,
                source=round_state.player,
                target=enemy,
            )
            for enemy in round_state.enemies
        ] * round_state.player.energy
