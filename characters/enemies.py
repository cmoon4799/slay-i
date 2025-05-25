from character import Enemy, Attack
from enum import Enum, auto


class JawWorm(Enemy):
    class Moves(Enum):
        CHOMP = auto()
        THRASH = auto()
        BELLOW = auto()

    def __init__(self):
        self.move_

    def get_move(self):
        # use chomp as first move
        if len(self.move_order) == 0:

		// Use chomp as the first move
		if (firstMove) {
			firstMove = false;
			setMove(CHOMP, Intent.ATTACK, damage.get(0).base);
			return ;
		}

		// 25 % Chance to Chomp
		if (num < 25) {
			if (lastMove(CHOMP)) {
				if (AbstractDungeon.aiRng.randomBoolean(0.5625f)) {
					setMove(MOVES[0], BELLOW, Intent.DEFEND_BUFF);
				} else {
					setMove(THRASH, Intent.ATTACK_DEFEND, damage.get(1).base);
				}
			} else {
				setMove(CHOMP, Intent.ATTACK, damage.get(0).base);
			}

			// 35 % chance to use Thrash
		} else if (num < 55) {
			if (lastTwoMoves(THRASH)) {
				if (AbstractDungeon.aiRng.randomBoolean(0.357f)) {
					setMove(CHOMP, Intent.ATTACK, damage.get(0).base);
				} else {
					setMove(MOVES[0], BELLOW, Intent.DEFEND_BUFF);
				}
			} else {
				setMove(THRASH, Intent.ATTACK_DEFEND, damage.get(1).base);
			}

			// 45 % chance to use BELLOW
		} else {
			if (lastMove(BELLOW)) {
				if (AbstractDungeon.aiRng.randomBoolean(0.416f)) {
					setMove(CHOMP, Intent.ATTACK, damage.get(0).base);
				} else {
					setMove(THRASH, Intent.ATTACK_DEFEND, damage.get(1).base);
				}
			} else {
				setMove(MOVES[0], BELLOW, Intent.DEFEND_BUFF);
			}
		}
	}
