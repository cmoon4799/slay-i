from enum import Enum, auto
from cards.cards import Card, CardType
from collections import defaultdict, deque
from typing import Callable, List
from actions import Event, EventType
from characters.players import Player
from characters.enemies import Enemy

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
    
action queue
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
    """Represents the round state of a battle.

    action_queue: A double ended queue of a sequence of actions to process. Some actions are considered Events which can trigger Event callbacks. For example, the relic Orichalcum may register a callback on EventType.TURN_END to add block to the player.
    """

    def __init__(self, player: Player, enemies: List[Enemy]):
        self.action_queue = deque(
            [
                Event(EventType.ROUND_START),
                Event(EventType.TURN_START),
            ]
        )  # processed left to right
        self.event_callbacks = default_event_callbacks
        self.card_draw = 5
        self.round = 1
        self.player = player
        self.enemies = enemies

    def process_action_queue(self):
        while self.action_queue:
            event = self.action_queue.popleft()
            match event.event_type:
                case EventType.ROUND_START:
                    pass
                case EventType.TURN_START:
                    pass

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


def draw_card(round_state: RoundState):
    pass


default_event_callbacks = {
    EventType.TURN_START: [draw_card],
}

round_state = RoundState(None, [])
print(round_state.event_callbacks)
