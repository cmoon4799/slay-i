from enum import Enum, auto
import random

from typing import List
from characters.character import Character, ConditionType
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
    def __init__(
        self, name, intentions: List[EnemyIntent], damage, hit_count, play_move
    ):
        self.name = name
        self.intentions = intentions
        self.damage = damage
        self.hit_count = hit_count
        self.play_move = play_move


class Enemy(Character):
    def __init__(self, type: EnemyType, round_state: RoundState):
        self.type = type
        self.round_state = round_state
        self.intentions = None
        self.play_move = None
        self.move_order = []

    def get_move(self):
        raise NotImplementedError("Each enemy must define its move behavior.")

    def _set_move(self, move: EnemyMove):
        self.intentions = move.intentions
        self.play_move = move.play_move

    def _last_move(self, move, n):
        return len(self.move_roder) >= n and all(
            m == move for m in self.move_order[-n:]
        )


class JawWorm(Enemy):
    class Moves(Enum):
        CHOMP = auto()
        THRASH = auto()
        BELLOW = auto()

    def __init__(self, type, round_state):
        super().__init__(type, round_state)
        self.Moves.CHOMP = EnemyMove(
            name="CHOMP",
            intentions=[EnemyIntent.ATTACK],
            damage=11,
            hit_count=1,
            play_move=self._chomp,
        )
        self.Moves.THRASH = EnemyMove(
            name="THRASH",
            intentions=[EnemyIntent.ATTACK, EnemyIntent.DEFEND],
            damage=7,
            hit_count=1,
            play_move=self._thrash,
        )
        self.Moves.BELLOW = EnemyMove(
            name="BELLOW",
            intentions=[EnemyIntent.BUFF],
            damage=0,
            hit_count=0,
            play_move=self._bellow,
        )

    def _chomp(self, round_state):
        return [
            Damage(
                damage=11,
                source=self,
                target=round_state.player,
            )
        ]

    def _thrash(self, round_state):
        return [
            Damage(
                damage=7,
                source=self,
                target=round_state.player,
            ),
            Block(
                block=5,
                source=self,
            ),
        ]

    def _bellow(self, round_state):
        return [
            Condition(
                condition={
                    ConditionType.STRENGTH: 3,
                },
                source=self,
                target=self,
            )
        ]

    def get_move(self):
        num = random.random()
        if len(self.first_move) == 0:
            self._set_move(self.Moves.CHOMP)

        elif num < 0.25:
            if self._last_move(self.Moves.CHOMP, 1):
                if random.random() < 0.5625:
                    self._set_move(self.Moves.BELLOW)
                else:
                    self._set_move(self.Moves.THRASH)
            else:
                self._set_move(self.Moves.CHOMP)

        elif num < 0.55:
            if self._last_move(self.Moves.THRASH, 2):
                if random.random() < 0.357:
                    self._set_move(self.Moves.CHOMP)
                else:
                    self._set_move(self.Moves.BELLOW)
            else:
                self._set_move(self.Moves.THRASH)

        else:
            if self._last_move(self.Moves.BELLOW, 1):
                if random.random() < 0.416:
                    self._set_move(self.Moves.CHOMP)
                else:
                    self._set_move(self.Moves.THRASH)
            else:
                self._set_move(self.Moves.BELLOW)
