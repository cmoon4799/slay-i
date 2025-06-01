
from __future__ import annotations
from enum import Enum, auto
from math import floor
from cards.cards import Card, CardType, build_card_table
from collections import defaultdict, deque
from typing import Callable, List, Dict
from actions import Action, ActionType, Damage
from characters.character import Character, ConditionType, ConditionModifierType
from characters.players import Player
from characters.enemies import Enemy
from relics.relics import FrozenEye
import random
from abstract_player import AbstractPlayer, ConsolePlayer


class RoomType:
    BATTLE = auto()
    SHOP = auto()


class Room:
    def __init__(
        self,
        player: Player,
        player_interface: AbstractPlayer,
    ):
        self.player = player
        self.player_interface = player_interface
        self.action_queue = deque(
            [
                Action(ActionType.START_ROUND),
            ]
        )  # processed left to right
        self.action_callbacks = {action_type: [] for action_type in ActionType}

        # iterate through relics, register callbacks
        pass

    def process_action_queue(self):
        raise NotImplementedError()

    def _start_round(self):
        for callback in self.action_callbacks[ActionType.START_ROUND]:
            callback(self)

        # queue START_TURN
        self.action_queue.append(Action(ActionType.START_TURN))

    def _round_end(self):
        # update player deck with curses (Writhing Mass)
        # display rewards if no smoke bomb
        pass

    def _start_turn(self):
        self.player.energy = self.player.base_energy
        self.action_queue.append(Action(ActionType.DRAW_HAND))
        for enemy in self.enemies:
            enemy.get_move()

    # get state representation based on abstract player interface
    def _get_state(self):
        raise NotImplementedError

    # displays turn state and invokes selected choice
    def display_turn_state_and_choices(self):
        pass

    def _view_pile(self, title, cards):
        for line in build_card_table(title, cards):
            print(line)

    def _get_turn_choices(self):
        raise NotImplementedError
