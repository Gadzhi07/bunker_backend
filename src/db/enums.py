from enum import StrEnum, auto


class GameStatus(StrEnum):
    wait = auto()
    round_1 = "1"
    round_2 = "2"
    round_3 = "3"
    round_4 = "4"
    round_5 = "5"
    advanced = auto()
    finished = auto()


class TeamSide(StrEnum):
    kicked = auto()
    not_kicked = auto()


class GameMode(StrEnum):
    Basic = auto()
    Advanced = auto()


class BunkerCardType(StrEnum):
    BunkerCard = auto()
    DangerCard = auto()

