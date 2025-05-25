from character import Enemy, Attack, Effect
from enum import Enum, auto
import random


class Intent(Enum):
    ATTACK = auto()
    ATTACK_DEFEND = auto()
    DEFEND_BUFF = auto()


class JawWorm(Enemy):
    class Moves(Enum):
        CHOMP = [
            Attack(
                name="CHOMP",
                base_damage=11,
                hit_count=1,
                intent=Intent.ATTACK
            )
        ]
        THRASH = [
            Attack(
                name="THRASH",
                base_damage=7,
                hit_count=1,
                intent=Intent.ATTACK_DEFEND
            ),
            Effect(
                name="",
                base_damage=)
        ]
        BELLOW = auto()

    def __init__(self):
        super().__init__()
        self.move_order = []
        self.damage = [
            Attack(name="CHOMP", base_damage=11,
                   hit_count=1, intent=Intent.ATTACK),
            Attack(name="THRASH", base_damage=7,
                   hit_count=2, intent=Intent.ATTACK_DEFEND)
        ]

    def last_move(self, move):
        return self.move_order and self.move_order[-1] == move

    def last_two_moves(self, move):
        return len(self.move_order) >= 2 and all(m == move for m in self.move_order[-2:])

    def get_move(self):
        num = random.random()
        if len(self.first_move) == 0:
            self.first_move = False
            chosen = self.Moves.CHOMP
            intent = Intent.ATTACK
            dmg = self.damage[0]

        elif num < .25:
            if self.last_move(self.Moves.CHOMP):
                if random.random() < 0.5625:
                    chosen = self.Moves.BELLOW
                    intent = Intent.DEFEND_BUFF
                    dmg = None
                else:
                    chosen = self.Moves.THRASH
                    intent = Intent.ATTACK_DEFEND
                    dmg = self.damage[1]
            else:
                chosen = self.Moves.CHOMP
                intent = Intent.ATTACK
                dmg = self.damage[0]

        elif num < .55:
            if self.last_two_moves(self.Moves.THRASH):
                if random.random() < 0.357:
                    chosen = self.Moves.CHOMP
                    intent = Intent.ATTACK
                    dmg = self.damage[0]
                else:
                    chosen = self.Moves.BELLOW
                    intent = Intent.DEFEND_BUFF
                    dmg = None
            else:
                chosen = self.Moves.THRASH
                intent = Intent.ATTACK_DEFEND
                dmg = self.damage[1]

        else:
            if self.last_move(self.Moves.BELLOW):
                if random.random() < 0.416:
                    chosen = self.Moves.CHOMP
                    intent = Intent.ATTACK
                    dmg = self.damage[0]
                else:
                    chosen = self.Moves.THRASH
                    intent = Intent.ATTACK_DEFEND
                    dmg = self.damage[1]
            else:
                chosen = self.Moves.BELLOW
                intent = Intent.DEFEND_BUFF
                dmg = None

        self.move_order.append(chosen)
        return Attack(
            name=chosen.name,
            base_damage=(dmg.base_damage if dmg else 0),
            hit_count=(dmg.hit_count if dmg else 0),
            intent=intent
        )
