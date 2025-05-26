from cards.cards import Card, CardType, CardRarity, CardClass
from actions import Damage, Source, Condition, Block
from characters.character import ConditionType


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
        )

    def play_card(self, current_position, target, round_state):
        return [
            Damage(
                name=self.name,
                damage=self.damage,
                hit_count=1,
                source=Source.CARD,
                target=target,
            ),
        ]


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
        )

    def play_card(self, current_position, target, round_state):
        return [
            Block(
                name=self.name,
                block=self.block,
                block_count=self.block_count,
                source=Source.CARD,
                target=[current_position],  # self
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

    def play_card(self, current_position, target, round_state):
        return [
            Damage(
                name=self.name,
                damage=self.damage,
                hit_count=1,
                source=Source.CARD,
                target=target,
            ),
            Condition(
                name=self.name,
                condition=self.condition,
            ),
        ]
