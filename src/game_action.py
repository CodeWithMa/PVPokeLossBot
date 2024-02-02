from enum import Enum
from attrs import define


class GameActions(Enum):
    no_action = 1
    tap_position = 2
    exit_program = 3


@define(frozen=True)
class GameAction:
    action: GameActions = GameActions.no_action
    position: tuple[int,int] = (0, 0)
    is_ingame: bool = False
