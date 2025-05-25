from enum import Enum, auto
from cards import Card, CardType, CardTarget
from collections import defaultdict, deque
from typing import Callable

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
    turn start
    shuffle cards
    draw cards

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
    
event queue
    [
        Attack(
            name = "Bash",
            base_damage = 8,
            hit_count = 1,
            intent = None,
        ),
        Effect(
            name = "Bash"
            effect = {
                VULNERABLE = 2
            }
        )
    ]

"""


class RoundState:
    event_queue = deque()
    card_draw = 5
    round = 1

    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies

    def play_card(self, card):
        if card.type == CardType.ATTACK:
            self.play_attack(card)
        if card.type == CardType.SKILL:
            self.play_skill(card)

    def _play_attack(self, card):
        pass

    def _play_skill(self, card):
        pass

    def round_start(self):
        # TD: display choices for electronics, library card, etc
        # iterate through relics, register callbacks
        pass

    def start_turn(self):
        # start turn callbacks, including turn N specific callbacks (Captain's Wheel)
        # display choices: potions, play a card, end turn
        pass

    def end_turn(self):
        # call end turn callbacks
        # enemy attacks
        pass


class EventTypes(Enum):
    PLAYER_DAMAGE = auto()
    ENEMY_DAMAGE = auto()
    DRAW_CARD = auto()
    ROUND_START = auto()
    ROUND_END = auto()
    TURN_START = auto()
    TURN_END = auto()


class EventCallbacks:
    callbacks = {event: [] for event in EventTypes}

    def __init__(self):
        self.callbacks[EventTypes.TURN_START].append()

    def register_callback(event_type, callback: Callable[[RoundState], None]):
        pass

    # TURN_START default callbacks
    def _remove_player_armor(round_state):
        round_state.player.block = 0
