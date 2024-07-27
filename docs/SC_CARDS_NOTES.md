POST /game/{game_id}/{user_id}/open_special_conditions_card
BODY image_url, selected_user (optional), action_with_card_type (optional), bunker_card_url (optional)
RETURN 200 | 20X + list of [](DB.md#User_games) | 20X + list of [](DB.md#all_card_types) | 20X [](DB.md#Opened_bunker_cards) | 400

Структура:
```json
{ // позволяет забрать себе чужую карту багажа, пострадавший берет +1 ОУ
	"can_play": "always", // kicked / in_vote / in_your_turn
	"dependencies": ["selected_user all anyway"],
	"actions": [
"update baggage user_id from selected_user",
"delete baggage selected_user",
"insert special_conditions selected_user"]
}

{ // поменяйся открытыми картами багажа с игроком слева/справа
	"can_play": "always", // kicked / in_vote / in_your_turn
	"dependencies": ["selected_user left_right if_opened"],
	"if_opened_card_type": "baggage",
	"actions": ["swap baggage user_id selected_user"]
}

{ // если изгнан игрок слева, то в след раз голосуй против себя
	"can_play": "always", // kicked / in_vote / in_your_turn
	"dependencies": [],
	"actions": [],
	"vote_against_yourself_if": "left_player_is_kicked"
}
```

- позволяют выбрать объекта действия:
	1. ВАРИАНТ с выбором чела: all / left_right
	2. ВАРИАНТ с выбором карты (если есть): anyway / if_opened
	3. меняем статус код на 20Х
	4. возвращаем список user_id: display_name
	5. после выбора ждем обратного запроса с selected_user

- позволяют выбрать карту бункера:
	1. меняем статус код на 20Х
	2. возвращаем список round_id: Opened_bunker_cards.bunker_card_url
	3. после выбора ждем обратного запроса с bunker_card_url

- позволяют выбрать тип карты игрока:
	1. меняем статус код на 20Х
	2. возвращаем список Game.Settings.enabled_type_cards.name
	3. после выбора ждем обратного запроса с action_with_card_type

- возможность разыграть:
	1. Всегда
	2. изгнан: User_games.go_out_vote_id not NULL
	3. Во время голосования: COUNT(Votes_rounds) для текущего раунда > 0
	4. В свою очередь: current_queue == user_id

#### Изменения в бд:
#### При подведении итогов голосования:

##### Твой голос удваивается в этом голосовании
Скопировать cur_vote_id WHERE who_voted = user_id

##### Голос выбранного не учитывается
Удалить cur_vote_id WHERE Votes.who_voted == selected_user

##### Голоса против выбранного удваиваются, но сам не голосуешь
Удалить cur_vote_id WHERE who_voted = user_id
ПОЛУЧИТЬ И ОТПРАВИТЬ ВСЕ:
cur_vote_id WHERE selected_user = selected_user

##### Переголосовать всем, выбирая другого
- Rounds.needed_votes += 1
- Создаем Votes_rounds с permited_to_revote = False
- Возвращаем 20X с vote_id созданного голосования

