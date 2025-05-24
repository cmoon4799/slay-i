from cards import Card, CardType, CardRarity, CardTarget


class Bash(Card):
    def __init__(self):
        super().__init__(
            name="Bash",
            cost=2,
            card_type=CardType.ATTACK,
            rarity=CardRarity.BASIC,
            target=CardTarget.SINGLE,
            damage=8,
            vulnerable=2,
            weak=0,
        )

    def play(self, character, round_state, target):
        pass
