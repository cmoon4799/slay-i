from enum import Enum, auto
from cards.cards import Card, CardType
from collections import defaultdict, deque
from typing import Callable, List, Dict
from actions import Action, ActionType
from characters.players import Player
from characters.enemies import Enemy
from relics import FrozenEye
import random

"""
INPUT:

enemy
character
  deck
  health

piles...
    exhaust
    draw
    discard
    deck

order...
    round start
        calculate player energy
    turn start
    draw cards
        shuffle discard pile into draw pile

    display...
        enemy intent
        player inventory...
            relics, gold, etc
        map info...
            floor level
        choices...
            use potions
                can display more choices (e.g. elixir)
            play a card from the hand (consider energy and debuffs)
            end turn
                go to turn start
    
    end round

round start -> turn start -> 

TODO
* Add a hook to recalculate enemy intent upon Condition update, e.g. if player now has Vulnerable.
* For an enemy like Writhing Mass, their intent updates with each damage taken. Should the enemy just register a callback on ENEMY_DAMAGE_TAKEN?

"""


class RoundState:
    """Represents the round state of a battle."""

    def __init__(self, player: Player, enemies: List[Enemy]):
        self.action_queue = deque(
            [
                Action(ActionType.ROUND_START),
            ]
        )  # processed left to right
        self.event_callbacks = {
            ActionType.ROUND_START: [],
            ActionType.ROUND_END: [],
            ActionType.TURN_START: [],
            ActionType.DRAW_CARD: [],
            ActionType.SHUFFLE_DISCARD_PILE: [],
            ActionType.EXHAUST_CARD: [],
            ActionType.PLAY_CARD: [],
            ActionType.PLAY_ATTACK: [],
            ActionType.PLAY_SKILL: [],
            ActionType.PLAY_POWER: [],
            ActionType.PLAY_CURSE: [],
            ActionType.PLAY_STATUS: [],
            ActionType.PLAY_POTION: [],
            ActionType.TURN_END: [],
            ActionType.RECEIVE_ATTACK: [],
        }
        self.draw_amount = 5
        self.round = 1
        self.player = player
        self.enemies = enemies

        # piles
        self.draw_pile = player.deck.copy()
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []

        # iterate through relics, register callbacks
        pass

    def process_action_queue(self):
        while self.action_queue:
            action = self.action_queue.popleft()
            match action.type:
                case ActionType.ROUND_START:
                    self._round_start()
                case ActionType.TURN_START:
                    self._turn_start()

    def _play_card(self, card):
        if card.type == CardType.ATTACK:
            self.play_attack(card)
        elif card.type == CardType.SKILL:
            self.play_skill(card)
        elif card.type == CardType.POWER:
            self.play_power(card)

    def _play_attack(self, card, target):
        # single enemy target, random enemy target, all enemies

        # fixed cost, x cost

        pass

    def _play_skill(self, card):
        pass

    def _play_power(self, card):
        pass

    def _round_start(self):
        for callback in self.event_callbacks[ActionType.ROUND_START]:
            callback(self)

        # queue TURN_START
        self.action_queue.append(Action(ActionType.TURN_START))

    def _round_end(self):
        # update player deck with curses (Writhin Mass)
        pass

    def _draw_card(self):
        assert len(self.draw_pile) > 0 and len(self.hand) < 10
        if any(isinstance(relic, FrozenEye) for relic in self.player.relics):
            card = self.draw_pile.pop()
        else:
            card = self.draw_pile.pop(random.randrange(len(self.draw_pile)))

        self.hand.append(card)
        self.action_queue.appendleft(Action(ActionType.DRAW_CARD))

    def _attempt_draw(self):
        if len(self.draw_pile) > 0:
            if len(self.hand < 10):
                self._draw_card()
        else:
            self._shuffle_discard_pile()

            if len(self.draw_pile) > 0:
                if len(self.hand < 10):
                    self._draw_card()

    def _shuffle_discard_pile(self):
        # shuffle discard pile callbacks
        for callback in self.event_callbacks[ActionType.SHUFFLE_DISCARD_PILE]:
            callback(self)

        random.shuffle(self.discard_pile)
        self.draw_pile = self.discard_pile
        self.discard_pile = []

    def _turn_start(self):
        # start turn callbacks, including turn N specific callbacks (Captain's Wheel)
        pass

        # draw hand
        for i in range(self.draw_amount):
            self._attempt_draw()

        # get enemy move
        for enemy in round_state.enemies:
            enemy.get_move()

        # display choices
        self._display()

    # display the state of the round
    # inventory:
    # player state: conditions, hp, max hp
    # enemy states: conditions, hp, max hp
    # hand
    # pile sizes
    def _display(self):
        pass

    def _display_choices(self):
        pass

    def _turn_end(self):
        # call end turn callbacks
        # enemy attacks
        # enqueue turn start

        pass


round_state = RoundState(None, [])
print(round_state.event_callbacks)
