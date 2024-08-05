from enum import StrEnum, auto


class GameStatus(StrEnum):
    wait = auto()
    rounds = auto()
    advanced = auto()
    finished = auto()


class TeamSide(StrEnum):
    kicked = auto()
    not_kicked = auto()


class GameMode(StrEnum):
    Basic = "Basic"
    Advanced = "Advanced"


class BunkerCardType(StrEnum):
    BunkerCard = "BunkerCard"
    DangerCard = "DangerCard"


class CharacterCardType(StrEnum):
    profession = auto()
    biology = auto()
    health = auto()
    hobby = auto()
    baggage = auto()
    facts = auto()
    phobia = auto()
    character_trait = auto()

