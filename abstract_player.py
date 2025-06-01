import textwrap
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from actions import ActionType
from characters.character import Character
from cards.cards import build_card_table
from room.battle import BattleState
from room.room import RoomType
from game import GameState


class AbstractPlayer(ABC):
    @abstractmethod
    def render_state(self, room_type, state):
        pass

    @abstractmethod
    def prompt_choice(self, prompt: str, choices: List[Tuple[int, str]]) -> int:
        pass

    # @abstractmethod
    # def display_message(self, message: str):
    #     pass


BOX_WIDTH = 50
PADDING = 1
MAX_ROWS = 5


def wrap_line(line, width):
    return textwrap.wrap(line, width)


def format_box(title, lines, width=BOX_WIDTH):
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(wrap_line(line, width - 2 * PADDING - 2))

    # Pad all lines to width
    padded_lines = [
        f"|{' ' * PADDING}{line.ljust(width - 2 * PADDING - 2)}{' ' * PADDING}|"
        for line in wrapped_lines
    ]

    top = f"+{'-' * (width - 2)}+"
    title_bar = f"| {title.center(width - 4)} |"
    separator = f"+{'=' * (width - 2)}+"
    bottom = f"+{'-' * (width - 2)}+"

    return [top, title_bar, separator] + padded_lines + [bottom]


def combine_boxes_horizontally(boxes):
    max_lines = max(len(b) for b in boxes)
    padded_boxes = [b + [" " * len(b[0])] *
                    (max_lines - len(b)) for b in boxes]
    return ["   ".join(line_group) for line_group in zip(*padded_boxes)]


class ConsolePlayer(AbstractPlayer):
    def render_state(self, room_type, state):
        # render default game information
        if room_type == RoomType.BATTLE:
            self._render_battle_state()

    def _render_game_state(state):
        print(format_box(
            "GENERAL",
            [
                state[GameState.PLAYER_TYPE],
                "{}/{}".format(state[GameState.HEALTH],
                               state[GameState.MAX_HEALTH]),
                "GOLD: {}".format(state[GameState.GOLD]),
                "ACT: {}".format(state[GameState.ACT]),
                "FLOOR: {}".format(state[GameState.FLOOR]),
            ]
        ))

        print()

        print(format_box(
            "POTIONS",
            [
                p.name if p else "-" for p in state.potions
            ],
        ))

        print()

        print(format_box(
            "RELICS",
            [
                relic.name for relic in state.relics
            ],
        ))

        # floor, act

    def _render_battle_state(state):
        # Player Box
        player_box = format_box(
            state[GameState.PLAYER_TYPE].name, state.player.get_state_string().split(
                "\n")
        )

        # Enemy Boxes
        enemy_boxes = [
            format_box(enemy.name, enemy.get_state_string().split("\n"))
            for i, enemy in enumerate(state.enemies)
        ]

        # Pile Summary
        pile_box = format_box(
            "PILES",
            [
                f"Draw: {len(state.draw_pile)}",
                f"Discard: {len(state.discard_pile)}",
                f"Exhaust: {len(state.exhaust_pile)}",
                f"Deck: {len(state.player.deck)}",
            ],
        )

        # Round Info
        info_box = format_box(
            "ROUND INFO",
            [
                f"Turn: {state.turn}",
            ],
        )

        # Display vertically stacked
        for line in combine_boxes_horizontally([pile_box, info_box]):
            print(line)

        print()  # Spacer

        for line in combine_boxes_horizontally([player_box] + enemy_boxes):
            print(line)

        print()  # Spacer

        for line in build_card_table("HAND", state.hand):
            print(line)

    def prompt_choice(self, choices: List) -> int:
        print("\n== CHOICES ==\n")
        for i in range(len(choices)):
            print("({}) {}".format(i, choices[i][1]))

        print()
        while True:
            try:
                user_input = input("Choice: ").strip()
                choice = int(user_input)
                if choice < len(choices):
                    return choice
                else:
                    print("Invalid choice. Please enter one of the numbers listed.")
            except ValueError:
                print("Invalid input. Please enter a number.")
