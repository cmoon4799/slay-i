import textwrap
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from actions import ActionType
from characters.character import Character
from cards.cards import build_card_table


class AbstractPlayer(ABC):
    @abstractmethod
    def display_turn_state(self, round_state):
        pass

    @abstractmethod
    def make_choice(self, prompt: str, choices: List[Tuple[int, str]]) -> int:
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
    padded_boxes = [b + [" " * len(b[0])] * (max_lines - len(b)) for b in boxes]
    return ["   ".join(line_group) for line_group in zip(*padded_boxes)]


class ConsolePlayer(AbstractPlayer):
    def display_turn_state(self, round_state):
        def box(title, lines):
            return format_box(title, lines)

        # Inventory Box
        inventory_box = box(
            "INVENTORY",
            [
                "Potions: "
                + (", ".join(p.name for p in round_state.player.potions) or "None"),
                "Relics: "
                + (", ".join(r.name for r in round_state.player.relics) or "None"),
                f"Gold: {round_state.player.gold}",
            ],
        )

        # Player Box
        player_box = box(
            round_state.player.name, round_state.player.get_state_string().split("\n")
        )

        # Enemy Boxes
        enemy_boxes = [
            box(enemy.name, enemy.get_state_string().split("\n"))
            for i, enemy in enumerate(round_state.enemies)
        ]

        # Pile Summary
        pile_box = box(
            "PILES",
            [
                f"Draw: {len(round_state.draw_pile)}",
                f"Discard: {len(round_state.discard_pile)}",
                f"Exhaust: {len(round_state.exhaust_pile)}",
                f"Deck: {len(round_state.player.deck)}",
            ],
        )

        # Round Info
        info_box = box(
            "ROUND INFO",
            [
                f"Turn: {round_state.turn}",
            ],
        )

        # Display vertically stacked
        for line in combine_boxes_horizontally([inventory_box, pile_box, info_box]):
            print(line)

        print()  # Spacer

        for line in combine_boxes_horizontally([player_box] + enemy_boxes):
            print(line)

        print()  # Spacer

        for line in build_card_table("HAND", round_state.hand):
            print(line)

    def make_choice(self, choices: List) -> int:
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
