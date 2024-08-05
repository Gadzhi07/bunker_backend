from typing import Annotated, Any, Optional
from .enums import BunkerCardType, CharacterCardType, GameMode, GameStatus, TeamSide
from .base import Base

from sqlalchemy import VARCHAR, CheckConstraint, ForeignKey, String, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship


intpk = Annotated[int, mapped_column(primary_key=True)]
user_gamedata_id_fk_pk = Annotated[int, mapped_column(ForeignKey("user_gamedata.id"), primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    display_name: Mapped[str] = mapped_column(VARCHAR(150), nullable=False)
    count_games: Mapped[int] = mapped_column(server_default="0")
    number_of_wins: Mapped[int] = mapped_column(server_default="0")

    settings: Mapped[list["Settings"]] = relationship(back_populates="creator")


class EnabledTypeCard(Base):
    __tablename__ = "enabled_type_cards"

    id: Mapped[intpk]
    settings_id: Mapped[int] = mapped_column(ForeignKey("settings.id"))
    card_type: Mapped["CharacterCardType"] = mapped_column(
        ENUM(CharacterCardType, name="character_card_type_enum", create_type=False))


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[intpk]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    game_mode: Mapped["GameMode"] = mapped_column(ENUM(GameMode, name="game_mode_enum", create_type=False),
                                                  server_default=GameMode.Basic)
    count_sc_cards: Mapped[int]
    time_to_open_card: Mapped[int]
    speak_after_open_card: Mapped[int]
    speak_under_vote: Mapped[int] 
    voting_time_limit: Mapped[int]
    speak_if_equal_vote: Mapped[int]
    speak_after_open_card_if_without_vote: Mapped[int]

    enabled_type_cards: Mapped[list["EnabledTypeCard"]] = relationship(backref="settings") 
    creator: Mapped["User"] = relationship(back_populates="settings")

    __table_args__ = (
        CheckConstraint("count_sc_cards BETWEEN 0 AND 8", name="check_count_sc_cards"),
        CheckConstraint("""time_to_open_card >= 10 AND speak_after_open_card >= 10 AND
    speak_under_vote >= 10 AND voting_time_limit >= 10 AND
    speak_if_equal_vote >= 10 AND speak_after_open_card_if_without_vote >= 0""", name="check_time_limits")
    )

class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(Uuid, server_default=text("gen_random_uuid()"), primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int]
    settings_id: Mapped[int] = mapped_column(ForeignKey("settings.id"))
    disaster_image_url: Mapped[str] =  mapped_column(String)
    opened_bunker_cards: Mapped[list["OpenedBunkerCards"]] = relationship(backref="game")
    status: Mapped["GameStatus"] = mapped_column(ENUM(GameStatus, name="game_status_enum", create_type=False),
                                                 server_default=GameStatus.wait)
    current_queue: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_gamedata.id", use_alter=True, name="games_current_queue_fk"))

    owner: Mapped["User"] = relationship(backref="owner_of_games")
    settings: Mapped["Settings"] = relationship(backref="used_in_games")


class UserGamedata(Base):
    __tablename__ = "user_gamedata"

    id: Mapped[intpk]
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    go_out_voting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("votes_rounds.voting_id"))
    character_data: Mapped[list["CharacterData"]] = relationship(backref="user_gamedata")
    special_conditions: Mapped[list["CharacterSCCards"]] = relationship(backref="user_gamedata")

    __tableargs__ = (
        UniqueConstraint('game_id', "user_id", name="user_gamedata_uc")
    )

class CharacterData(Base):
    __tablename__ = "character_data"

    user_gamedata_id: Mapped[user_gamedata_id_fk_pk]
    card_name: Mapped[str] = mapped_column(String, primary_key=True)
    card_value: Mapped[str] = mapped_column(String)
    is_opened: Mapped[bool] = mapped_column(server_default="False")


class CharacterSCCards(Base):
    """
    special_conditions - информация о действиях карты ОУ
    """
    __tablename__ = "character_sc_cards"

    user_gamedata_id: Mapped[user_gamedata_id_fk_pk]
    image_url: Mapped[str] = mapped_column(String, primary_key=True)
    special_conditions: Mapped[dict[str, Any]]
    voting_id_when_card_was_open: Mapped[Optional[int]] = mapped_column(ForeignKey("votes_rounds.voting_id"))


class Rounds(Base):
    __tablename__ = "rounds"

    id: Mapped[intpk]
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"))
    needed_votes: Mapped[int]
    type_of_card_to_open: Mapped[Optional["CharacterCardType"]] = mapped_column(
        ENUM(CharacterCardType, name="character_card_type_enum", create_type=False))


class VotesRounds(Base):
    """
    voting_id - чем больше, тем позднее было голосование
    """
    __tablename__ = "votes_rounds"

    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id"), primary_key=True)
    voting_id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    permited_to_revote: Mapped[bool] = mapped_column(server_default="True")
    is_this_revote_voting: Mapped[bool] = mapped_column(server_default="False")


class Votes(Base):
    __tablename__ = "votes"

    vote_id: Mapped[intpk]
    voting_id: Mapped[int] = mapped_column(ForeignKey("votes_rounds.voting_id"))
    who_voted: Mapped[int] = mapped_column(ForeignKey("users.id"))
    selected_user: Mapped[int] = mapped_column(ForeignKey("users.id"))


class OpenedBunkerCards(Base):
    __tablename__ = "opened_bunker_cards"

    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), primary_key=True)
    card_image_url: Mapped[str] = mapped_column(String, primary_key=True)
    team_side: Mapped['TeamSide'] = mapped_column(
        ENUM(TeamSide, name="team_side_enum", create_type=False), server_default=TeamSide.not_kicked)
    bunker_card_type: Mapped['BunkerCardType'] = mapped_column(
        ENUM(BunkerCardType, name="bunker_card_type_enum", create_type=False))

