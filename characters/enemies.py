from enum import Enum, auto
import random

from typing import List
from characters.character import Character
from actions import Damage, Action, Block, Condition
from round_state import RoundState


class EnemyIntent(Enum):
    ATTACK = auto()
    DEFEND = auto()
    BUFF = auto()
    DEBUFF = auto()
    ESCAPE = auto()
    SLEEPING = auto()
    STUNNED = auto()
    UNKNOWN = auto()


class EnemyType(Enum):
    BOSS = auto()
    ELITE = auto()
    HALLWAY = auto()


class EnemyMove:
    def __init__(self, name, intentions: List[EnemyIntent], damage, hit_count):
        self.name = name
        self.intentions = intentions
        self.damage = damage
        self.hit_count = hit_count


class Enemy(Character):
    def __init__(self, type: EnemyType, round_state: RoundState):
        self.type = type
        self.round_state = round_state
        self.move_order = []

    def get_move(self):
        raise NotImplementedError("Each enemy must define its move behavior.")


class JawWorm(Enemy):
    class Moves(Enum):
        CHOMP = auto()
        THRASH = auto()

    def __init__(self, type):
        super().__init__(type)
        self.move_order = []
        self.moves = {
            self.Moves.CHOMP: EnemyMove(
                name="CHOMP",
                intentions=[EnemyIntent.ATTACK],
                damage=11,
                hit_count=1,
            ),
            JawWorm.Moves.THRASH: EnemyMove(
                name="THRASH",
                intent=[EnemyIntent.ATTACK, EnemyIntent.DEFEND],
                actions=[
                    Damage(
                        damage=7,
                        source=self,

                    ),
                    Block(
                        target=[
                            self.position,
                        ]
                    ),
                ]
            )
        }

    def _chomp(self):

    def last_move(self, move):
        return self.move_order and self.move_order[-1] == move

    def last_two_moves(self, move):
        return len(self.move_order) >= 2 and all(
            m == move for m in self.move_order[-2:]
        )

    def get_move(self):
        num = random.random()
        if len(self.first_move) == 0:
            self.first_move = False
            chosen = self.Moves.CHOMP
            intent = EnemyIntent.ATTACK
            dmg = self.damage[0]

        elif num < 0.25:
            if self.last_move(self.Moves.CHOMP):
                if random.random() < 0.5625:
                    chosen = self.Moves.BELLOW
                    intent = EnemyIntent.DEFEND_BUFF
                    dmg = None
                else:
                    chosen = self.Moves.THRASH
                    intent = EnemyIntent.ATTACK_DEFEND
                    dmg = self.damage[1]
            else:
                chosen = self.Moves.CHOMP
                intent = EnemyIntent.ATTACK
                dmg = self.damage[0]

        elif num < 0.55:
            if self.last_two_moves(self.Moves.THRASH):
                if random.random() < 0.357:
                    chosen = self.Moves.CHOMP
                    intent = EnemyIntent.ATTACK
                    dmg = self.damage[0]
                else:
                    chosen = self.Moves.BELLOW
                    intent = EnemyIntent.DEFEND_BUFF
                    dmg = None
            else:
                chosen = self.Moves.THRASH
                intent = EnemyIntent.ATTACK_DEFEND
                dmg = self.damage[1]

        else:
            if self.last_move(self.Moves.BELLOW):
                if random.random() < 0.416:
                    chosen = self.Moves.CHOMP
                    intent = EnemyIntent.ATTACK
                    dmg = self.damage[0]
                else:
                    chosen = self.Moves.THRASH
                    intent = EnemyIntent.ATTACK_DEFEND
                    dmg = self.damage[1]
            else:
                chosen = self.Moves.BELLOW
                intent = EnemyIntent.DEFEND_BUFF
                dmg = None

        self.move_order.append(chosen)
        return Damage(
            name=chosen.name,
            base_damage=(dmg.base_damage if dmg else 0),
            hit_count=(dmg.hit_count if dmg else 0),
            intent=intent,
        )
