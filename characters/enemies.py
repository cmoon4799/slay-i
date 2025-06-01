from enum import Enum, auto
import random

from typing import List, Callable
from characters.character import Character, ConditionType
from actions import Damage, Action, Block, Condition

"""
TODO
* Alter base stats depending on Ascension level.
* keys as names in moves when defining the map? should we make this consistent?
"""


class EnemyIntent(Enum):
    ATTACK = auto()
    DEFEND = auto()
    BUFF = auto()
    DEBUFF = auto()
    ESCAPE = auto()
    SLEEPING = auto()
    STUNNED = auto()
    UNKNOWN = auto()


class EnemyMove:
    def __init__(
        self, name, intentions: List[EnemyIntent], damage, hit_count, move_method
    ):
        self.name = name
        self.intentions = intentions
        self.damage = damage
        self.hit_count = hit_count
        self.play_move = move_method


class Enemy(Character):
    def __init__(self, name, max_health):
        super().__init__(name, max_health)
        self.intentions = None
        self.move_method = None
        self.move_order = []
        self.move: EnemyMove = None
        self.move_map = {}

    def get_state_string(self):
        out = "HEALTH: {}/{} | BLOCK: {} | INTENTIONS: {}".format(
            self.health,
            self.max_health,
            self.block,
            ", ".join(type.name for type in self.intentions),
        )
        if EnemyIntent.ATTACK in self.intentions:
            out += " | {}x{}".format(self.move.damage, self.move.hit_count)
        if any(self.conditions[condition] > 0 for condition in self.conditions):
            out += " | " + ", ".join(
                [
                    "{}: {}".format(condition.name, self.conditions[condition])
                    for condition in self.conditions
                    if self.conditions[condition] > 0
                ]
            )
        return out

    def get_move(self):
        raise NotImplementedError("Each enemy must define its move behavior.")

    def play_move(self, battle):
        battle.action_queue.extend(self.move_method(battle))
        self.move_order.append(self.move_name)

    def _set_move(self, move_name):
        enemy_move: EnemyMove = self.move_map[move_name]
        self.move = enemy_move
        self.intentions = enemy_move.intentions
        self.move_method = enemy_move.play_move
        self.move_name = move_name

    def _last_move(self, move, n):
        return len(self.move_order) >= n and all(
            m == move for m in self.move_order[-n:]
        )


class JawWorm(Enemy):
    class Moves(Enum):
        CHOMP = auto()
        THRASH = auto()
        BELLOW = auto()

    def __init__(self):
        super().__init__("JAW WORM", random.randrange(40, 45))
        self.move_map = {
            self.Moves.CHOMP: EnemyMove(
                name=self.Moves.CHOMP,
                intentions=[EnemyIntent.ATTACK],
                damage=11,
                hit_count=1,
                move_method=self._chomp,
            ),
            self.Moves.THRASH: EnemyMove(
                name=self.Moves.THRASH,
                intentions=[EnemyIntent.ATTACK, EnemyIntent.DEFEND],
                damage=7,
                hit_count=1,
                move_method=self._thrash,
            ),
            self.Moves.BELLOW: EnemyMove(
                name=self.Moves.BELLOW,
                intentions=[EnemyIntent.BUFF],
                damage=0,
                hit_count=0,
                move_method=self._bellow,
            ),
        }

    def _chomp(self, battle):
        return [
            Damage(
                damage=11,
                source=self,
                target=battle.player,
            )
        ]

    def _thrash(self, battle):
        return [
            Damage(
                damage=7,
                source=self,
                target=battle.player,
            ),
            Block(
                block=5,
                source=self,
                target=self,
            ),
        ]

    def _bellow(self, battle):
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
        if len(self.move_order) == 0:
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
