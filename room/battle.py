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
from room.room import Room

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
* Fairy in the bottle
* Ascension's bane
* Intangible
* Update intentions whenever it gets hit or something...
* Add ability to update player deck (e.g. Parasite for Writhing Mass).
* Display rewards if round ends with no smoke bomb.
* Add a hook to recalculate enemy intent upon Condition update, e.g. if player now has Vulnerable.
* For an enemy like Writhing Mass, their intent updates with each damage taken. Should the enemy just register a callback on ENEMY_DAMAGE_TAKEN?

* Need to consider unblocked damage for Fossilized Helix and Torii

"""


class BattleType(Enum):
    BOSS = auto()
    ELITE = auto()
    HALLWAY = auto()


class BattleState(Enum):
    ENEMIES = auto()
    HAND = auto()
    DRAW_PILE = auto()
    DISCARD_PILE = auto()
    EXHAUST_PILE = auto()
    TURN = auto()


class Battle(Room):
    def __init__(
        self,
        player: Player,
        enemies: List[Enemy],
        battle_type: BattleType,
        player_interface: AbstractPlayer,
    ):
        self.player = player
        self.enemies = enemies
        self.battle_type = battle_type
        self.player_interface = player_interface
        self.action_queue = deque(
            [
                Action(ActionType.START_ROUND),
            ]
        )  # processed left to right
        self.action_callbacks = {action_type: [] for action_type in ActionType}
        self.draw_amount = 5
        self.turn = 1

        self.player_turn = True

        # piles
        self.hand = []
        self.draw_pile = player.deck.copy()
        self.discard_pile = []
        self.exhaust_pile = []

        # iterate through relics, register callbacks
        pass

    def process_action_queue(self):
        while self.action_queue:
            action = self.action_queue.popleft()
            print("action: ", action)
            for callback in self.action_callbacks[action.type]:
                callback(self)
            match action.type:
                case ActionType.START_ROUND:
                    self._start_round()
                case ActionType.START_TURN:
                    self._start_turn()
                case ActionType.DRAW_HAND:
                    for _ in range(self.draw_amount):
                        self._attempt_draw()
                case ActionType.DAMAGE:
                    action.target.receive_damage(action, self)
                case ActionType.BLOCK:
                    action.target.receive_block(action, self)
                case ActionType.CONDITION:
                    action.target.receive_condition(action, self)

    def target_enemy(self):
        enemy_index = self.player_interface.prompt_choice(
            [
                (Action, f"{enemy.name} {enemy.get_state_string()}")
                for enemy in self.enemies
            ]
            + [(Action, "GO BACK")]
        )

        if enemy_index < len(self.enemies):
            return self.enemies[enemy_index]
        else:
            return None

    def _play_card(self, card: Card):
        target = None
        if card.targeted:
            target = self.target_enemy()
            if not target:
                return

        self.action_queue.extend(card.play_card(target, self))
        self.player.energy -= card.cost
        self.action_queue.append(Action(ActionType.PLAY_CARD))

        if card.type == CardType.ATTACK:
            pass
        elif card.type == CardType.SKILL:
            pass
        elif card.type == CardType.POWER:
            pass

    def _start_round(self):
        for callback in self.action_callbacks[ActionType.START_ROUND]:
            callback(self)

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
            if len(self.draw_pile) > 0 and len(self.hand) < 10:
                self._draw_card()

    def _shuffle_discard_pile(self):
        # shuffle discard pile callbacks
        pass

        for callback in self.action_callbacks[ActionType.SHUFFLE_DISCARD_PILE]:
            callback(self)

        random.shuffle(self.discard_pile)
        self.draw_pile = self.discard_pile
        self.discard_pile = []

    def _get_enemy_moves(self):
        # get enemy move
        for enemy in self.enemies:
            enemy.get_move()

    # get state representation based on abstract player interface
    def _get_state(self):
        state = super().get_state()

    # displays turn state and invokes selected choice

    def display_turn_state_and_choices(self):
        self.turn_state = self.player_interface.render_state(self)
        choices = self._get_turn_choices()
        choice = self.player_interface.prompt_choice(choices)

        match choices[choice][0].type:
            case ActionType.PLAY_CARD:
                self._play_card(choices[choice][2])
            case ActionType.PLAY_POTION:
                pass
            case ActionType.VIEW_DRAW_PILE:
                self._view_pile("DRAW PILE", self.draw_pile)
            case ActionType.VIEW_DISCARD_PILE:
                self._view_pile("DISCARD PILE", self.discard_pile)
            case ActionType.VIEW_EXHAUST_PILE:
                self._view_pile("EXHAUST PILE", self.exhaust_pile)
            case ActionType.VIEW_DECK:
                self._view_pile("VIEW DECK", self.player.deck)
            case ActionType.END_TURN:
                self._end_turn()

    def _view_pile(self, title, cards):
        for line in build_card_table(title, cards):
            print(line)

    def _get_turn_choices(self):
        choices = []
        for card in self.hand:
            if self.player.energy >= card.cost:
                choices.append(
                    (
                        Action(ActionType.PLAY_CARD),
                        "PLAY CARD: {} ({})".format(
                            card.name, card.description),
                        card,
                    )
                )

        for potion in self.player.potions:
            choices.append(
                (
                    Action(ActionType.PLAY_POTION),
                    "PLAY POTION: {} ({})".format(
                        potion.name, potion.description),
                    potion,
                )
            )

        choices.append((Action(ActionType.VIEW_DRAW_PILE), "VIEW DRAW PILE"))
        choices.append(
            (Action(ActionType.VIEW_DISCARD_PILE), "VIEW DISCARD PILE"))
        choices.append(
            (Action(ActionType.VIEW_EXHAUST_PILE), "VIEW EXHAUST PILE"))
        choices.append((Action(ActionType.VIEW_DECK), "VIEW DECK"))
        choices.append((Action(ActionType.END_TURN), "END TURN"))

        return choices

    def _end_turn(self):
        # end turn callbacks
        pass

        # discard cards
        self.discard_pile.extend(self.hand)
        self.hand = []

        # enemy attacks
        for enemy in self.enemies:
            enemy.play_move(self)

        self.turn += 1
        # enqueue turn start
        self.action_queue.append(Action(ActionType.START_TURN))
        print(self.action_queue)
