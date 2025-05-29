from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from actions import ActionType
from characters.character import Character
from round_state import RoundState


class AbstractPlayer(ABC):
    @abstractmethod
    def display_turn_state(self, round_state):
        pass

    @abstractmethod
    def make_choice(self, prompt: str, choices: List[Tuple[int, str]]) -> int:
        pass

    @abstractmethod
    def display_message(self, message: str):
        pass


class ConsolePlayer(AbstractPlayer):
    def display_turn_state(self, round_state: RoundState):
        print("\n\n== INVENTORY =\n\n")
        print(
            "POTIONS: "
            + ", ".join([potion.name for potion in round_state.player.potions])
        )
        print(
            "RELICS: "
            + ", ".join([potion.name for potion in round_state.player.potions])
        )
        print("GOLD: " + round_state.player.gold)

        print("\n\n== PLAYER =\n\n")
        print(round_state.player.get_state_string())

        print("\n\n== ENEMIES ==\n\n")
        for i in range(len(round_state.enemies)):
            print("ENEMY {}".format(i))
            print(round_state.enemies[i].get_state_string())

    def make_choice(self, choices: List) -> int:
        print("\n\n== CHOICES ==\n\n")
        for i in range(len(choices)):
            print("({}) {}".format(i, choices[i][1]))

        while True:
            try:
                user_input = input("Choice: ").strip()
                choice = int(user_input)
                if len(choice) < len(choices):
                    return choice
                else:
                    print("Invalid choice. Please enter one of the numbers listed.")
            except ValueError:
                print("Invalid input. Please enter a number.")
