from enum import Enum
from cards import Card, CardType, CardTarget
from collections import defaultdict

"""
INPUT:

enemy
character
  deck
  health



round start
draw cards
play card



"""


class EventTypes(Enum):
    PLAYER_DAMAGE = "PLAYER_DAMAGE"
    ENEMY_DAMAGE = "ENEMY_DAMAGE"
    DRAW_CARD = "DRAW_CARD"
    TURN_START = "TURN_START"

class EventCallbacks:
  self.callbacks = defaultdict(list)

  def register_callback(event_type):
    pass

class RoundState:
    self.event_queue = []
    self.player = None

    def __init__():
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

    def start_turn(self):
        # turn N specific callbacks, e.g. Captain's Wheel


    def end_turn(self):
        # call end turn callbacks
