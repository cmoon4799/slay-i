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
        self.block = 5
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
                block=self.block,
                source=round_state.player,
            )
        ]


class Strike(Card):
    def __init__(self):
        self.name = "STRIKE"
        self.damage = 6

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
                damage=self.damage,
                source=round_state.player,
                target=target,
            ),
        ]


class Bash(Card):
    def __init__(self):
        self.name = "BASH"
        self.damage = 8
        self.condition = {
            ConditionType.VULNERABLE: 2,
        }
        super().__init__(
            name=self.name,
            cost=2,
            card_type=CardType.ATTACK,
            card_rarity=CardRarity.BASIC,
            card_class=CardClass.IRONCLAD,
        )

    def play_card(self, source, target, energy):
        return [
            Damage(
                name=self.name,
                damage=self.damage,
                source=source,
                target=target,
            ),
            Condition(
                name=self.name,
                condition=self.condition,
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

    def play_card(self, source, target, round_state, energy):
        return [
            Damage(
                name=self.name, damage=self.damage, source=source, target=i,
            )
            for i in range(1, len(round_state.enemies) + 1)
        ] * round_state.player.energy
