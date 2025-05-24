from enum import Enum


class CardType(Enum):
    ATTACK = "ATTACK"
    SKILL = "SKILL"
    POWER = "POWER"
    STATUS = "STATUS"
    CURSE = "CURSE"


class CardTarget(Enum):
    ALL = "ALL"
    SINGLE = "SINGLE"
    RANDOM = "RANDOM"


class Card:
    def __init__(self, name, card_type, cost, description, rarity):
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.description = description
        self.rarity = rarity
        self.target = target

    def play(self):
        raise NotImplementedError(f"Play method not implemented for {self.name}")

    def __str__(self):
        return f"{self.name} ({self.card_type}) - Cost: {self.cost}\n{self.description}"
