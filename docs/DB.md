Удобная PDF схема базы данных: [bunker_db](bunker_db.pdf)

Онлайн диаграмма: https://dbdiagram.io/d/bunker-669cd5b68b4bb5230ee8aea6

##### User:
- user_id: int primary key
- display_name: str
- count_games: int, default = 0
- number_of_wins: int, default = 0

##### User_games:
- Game.game_id
- User.user_id
- go_out_vote_id: int NULLABLE
- queue: AUTOINCREMENT внутри Game.game_id = 0
- character_data_id:  AUTOINCREMENT Character_data.id
- special_conditions_id:  AUTOINCREMENT Character_special_conditions.id

##### Character_data:
- id
- card_name
- card_value
- is_opened: bool = False

##### Character_special_conditions
- id
- image_url
- special_conditions
- vote_id_when_card_was_open: int = NULL

##### Votes_rounds:
- game_id
- round_id
- vote_id autoincrement (чем больше, тем позднее было голосование)
- permited_to_revote: bool default = True
- is_this_revote_voting: bool default = False

##### Votes:
- id
- vote_id: int
- who_voted: User.user_id
- selected_user: User.user_id

##### Rounds:
- game_id
- round_id: int 1 ≤ x ≤ 5
- needed_votes: int ≥ 0
- type_of_card_to_open: NULLABLE (profession для round_id = 1)
##### Opened_bunker_cards
- game_id
- card_image_url
- team_side: kicked/not_kicked
- card_type: BunkerCard/DangerCard

##### Game:
- game_id: uuid v4 primary key ( gen_random_uuid() )
- owner_id: User.user_id
- chat_id: int
- settings_id: int
- disaster_image_url: str NULLABLE
- status: wait/round_id//finished
- current_queue: Users_games.queue

##### Settings:
- id: int primary key
- game_mode: Enum Basic/Advanced
- enabled_cards_id: enabled_type_cards.id
- count_special_conditions_cards: int 0 ≤ x ≤ 8
- time_to_open_card: int ≥ 10
- speak_after_open_card: int ≥ 10
- speak_under_vote: int ≥ 10
- voting_time_limit: int ≥ 10
- speak_if_equal_vote: int ≥ 10
- speak_after_open_card_if_without_vote: int ≥ 0

##### enabled_type_cards:
- id
- name

##### all_card_types:
- profession
- biology
- health
- hobby
- baggage
- facts
- special_conditions (dont use in enabled_type_cards)
- phobia (optional)
- character_trait (optional)
