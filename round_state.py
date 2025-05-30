from __future__ import annotations
from enum import Enum, auto
from cards.cards import Card, CardType
from collections import defaultdict, deque
from typing import Callable, List, Dict
from actions import Action, ActionType
from characters.players import Player
from characters.enemies import Enemy
from relics.relics import FrozenEye
import random
from abstract_player import AbstractPlayer
from potions import Potion

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
* Add abstract communication layer (e.g. stdin/stdout, socket?).
* Add round end detection system.
    * Reset default player state at the end of round.
* Akabeko shit.
* Update intentions whenever it gets hit or something...
* Add ability to update player deck (e.g. Parasite for Writhing Mass).
* Display rewards if round ends with no smoke bomb.
* Add a hook to recalculate enemy intent upon Condition update, e.g. if player now has Vulnerable.
* For an enemy like Writhing Mass, their intent updates with each damage taken. Should the enemy just register a callback on ENEMY_DAMAGE_TAKEN?

"""


class EncounterType(Enum):
    BOSS = auto()
    ELITE = auto()
    HALLWAY = auto()


class RoundState:
    """Represents the round state of a battle."""

    def __init__(
        self,
        player_interface: AbstractPlayer,
        player: Player,
        enemies: List[Enemy],
        encounter_type: EncounterType,
    ):
        self.player = player
        self.enemies = enemies
        self.encounter_type = encounter_type
        self.player_interface = player_interface
        self.action_queue = deque(
            [
                Action(ActionType.START_ROUND),
            ]
        )  # processed left to right
        self.event_callbacks = {action_type: [] for action_type in ActionType}
        self.draw_amount = 5
        self.round = 1

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
            print(action.type)
            for callback in self.event_callbacks[action.type]:
                callback(self)
            match action.type:
                case ActionType.START_ROUND:
                    self._start_round()
                case ActionType.START_TURN:
                    self._start_turn()
                case ActionType.DRAW_HAND:
                    for i in range(self.draw_amount):
                        
                case ActionType.DISPLAY_TURN_STATE:
                    self.display_turn_state_and_choices()

    def target_enemy(self):
        return self.player_interface.make_choice(
            [(Action, enemy.get_state_string) for enemy in self.enemies]
            + [(Action, "GO BACK")]
        )

    def _play_card(self, card: Card):
        enemy_index = None
        if card.targeted:
            enemy_index = self.target_enemy()
            if enemy_index == len(self.enemies):
                return

        card.play_card(self.enemies[enemy_index], self)
        self.action_queue.append(Action(ActionType.PLAY_CARD))

        if card.type == CardType.ATTACK:
            pass
        elif card.type == CardType.SKILL:
            pass
        elif card.type == CardType.POWER:
            pass

    def _play_attack(self, card, target):
        # single enemy target, random enemy target, all enemies
        # fixed cost, x cost
        pass

    def _play_skill(self, card):
        pass

    def _play_power(self, card):
        pass

    def _start_round(self):
        for callback in self.event_callbacks[ActionType.START_ROUND]:
            callback(self)

        # queue START_TURN
        self.action_queue.append(Action(ActionType.START_TURN))

    def _round_end(self):
        # update player deck with curses (Writhing Mass)
        # display rewards if no smoke bomb
        pass

    def _start_turn(self):
        self.action_queue.append(Action(ActionType.DRAW_HAND))
        for enemy in self.enemies:
            enemy.get_move()
        self.action_queue.append(Action(ActionType.DISPLAY_TURN_STATE))

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
            if len(self.hand) < 10:
                self._draw_card()
        else:
            self._shuffle_discard_pile()

            if len(self.draw_pile) > 0:
                if len(self.hand) < 10:
                    self._draw_card()

    def _shuffle_discard_pile(self):
        # shuffle discard pile callbacks
        pass

        for callback in self.event_callbacks[ActionType.SHUFFLE_DISCARD_PILE]:
            callback(self)

        random.shuffle(self.discard_pile)
        self.draw_pile = self.discard_pile
        self.discard_pile = []

    def _get_enemy_moves(self):
        # get enemy move
        for enemy in self.enemies:
            enemy.get_move()

    # displays turn state and invokes selected choice
    def display_turn_state_and_choices(self):
        while True:
            self.turn_state = self.player_interface.display_turn_state(self)
            choices = self._get_turn_choices()
            choice = self.player_interface.make_choice(choices)

            match choices[choice][0].type:
                case ActionType.PLAY_CARD:
                    self._play_card(choices[choice][2])
                case ActionType.PLAY_POTION:
                    pass
                case ActionType.VIEW_DRAW_PILE:
                    self._view_pile(self.draw_pile)
                case ActionType.VIEW_DISCARD_PILE:
                    self._view_pile(self.discard_pile)
                case ActionType.VIEW_EXHAUST_PILE:
                    self._view_pile(self.exhaust_pile)
                case ActionType.VIEW_DECK:
                    self._view_pile(self.player.deck)

    def _get_turn_choices(self):
        choices = []
        for card in self.hand:
            if self.player.energy >= card.cost:
                choices.append(
                    (
                        Action(ActionType.PLAY_CARD),
                        "PLAY CARD: {} ({})".format(card.name, card.description),
                        card,
                    )
                )

        for potion in self.player.potions:
            choices.append(
                (
                    Action(ActionType.PLAY_POTION),
                    "PLAY POTION: {} ({})".format(potion.name, potion.description),
                    potion,
                )
            )

        choices.append((Action(ActionType.VIEW_DRAW_PILE), "VIEW DRAW PILE"))
        choices.append((Action(ActionType.VIEW_DISCARD_PILE), "VIEW DISCARD PILE"))
        choices.append((Action(ActionType.VIEW_EXHAUST_PILE), "VIEW EXHAUST PILE"))
        choices.append((Action(ActionType.VIEW_DECK), "VIEW DECK"))
        choices.append((Action(ActionType.END_TURN), "END TURN"))

        return choices

    def _view_pile(self, pile: List[Card]):
        for card in pile:
            print(card.get_card_info_string())

    def _turn_end(self):
        # end turn callbacks
        pass

        # enemy attacks
        for enemy in self.enemies:
            enemy.move_method(self)

        # enqueue turn start
        self.action_queue.append(Action(ActionType.START_TURN))
