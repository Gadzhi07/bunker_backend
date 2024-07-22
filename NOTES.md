1. Старт
2. Кнопки
	- Настройки (пока без них, не готово)
	- Профиль:
		1. GET /api/game/{game_id}/users_info
3. В чате /game :

### /game:
- POST /api/game
- Сообщение с t.me/bot?start=game_id и регаем создателя

### ?start=game_id
- POST /api/game/{game_id}
- регаем чела в игру

### /cancel (лс)
- выйти из игры
### /start (чат)
- GET /api/game/{game_id}/start
- выдаем в лс фул инфу и соо с кнопкой “Использовать ОУ” закрепляем
- в чат кидаем фото катастрофы (можно закрепить это соо и после игры открепить)
- **Исследование Бункера**
- GET /api/game/{game_id}/open_bunker_card
- кидаем в чат карту бункера
- кидаем в чат соо НАЧАТЬ ОТКРЫТИЕ КАРТ
### Круг открытия карт. после нажатия от current_in_queue / НАЧАТЬ ОТКРЫТИЕ КАРТ:
- GET /api/game/{game_id}/current_in_queue
- GET /api/game/{game_id}/{user_id}/list_of_cards
- отправляется сообщение выбора что открывать в лс с лимитом в time_to_open_card сек
- POST /api/game/{game_id}/{user_id}/open_card
- инлайн кнопка, которая меняется каждые 10 сек
- После выбора и speak_after_open_card секунд меняется текст на display_name следующего
- GET /api/game/{game_id}/next_in_queue (450 - игроки закончились)

#### Когда список игроков закончен
- GET /api/game/{game_id}/users_info
- Сообщение с открытыми характеристиками игроков
- /api/game/{game_id}/start_new_voting - получили voting_id

#### голосование (если есть)
##### общее обсуждение
- инлайн кнопка меняется каждые 10 сек
- speak_under_vote секунд на общее обсуждение
- После speak_under_vote секунд отправляется сообщение с никами (инлайн выбор) людей в лс
- GET /api/vote/{voting_id}/who_can_vote
- GET /api/vote/{voting_id}/{user_id}/possible_for_voting
- POST /api/vote/{voting_id}/{user_id}/vote
##### голосование
- в чат отправляется сообщение “Для того, чтобы проголосовать перейдите в бота” + инлайн кнопка перейти в бота + кнопка с таймером на voting_time_limit
- итоги в чат
- GET /api/vote/{voting_id}/vote_results
- отправляется сообщение “Прокомментируйте свое решение” и инлайн кнопка “Закончить обсуждение”
###### если кого-то кикнули (статус код 200):
- идем в след раунд
- GET /api/game/{game_id}/start_new_round
###### если ничья (статус код 210 и сохраняем новый voting_id):
- дается speak_if_equal_vote секунд каждому на аргументацию
- GET /api/vote/{voting_id}/who_can_vote
- GET /api/vote/{voting_id}/{user_id}/possible_for_voting
- POST /api/vote/{voting_id}/{user_id}/vote
- GET /api/vote/{voting_id}/vote_results

##### Пытаемся начать второе голосование
- GET /api/game/{game_id}/start_new_voting
- 451 - начинаем новый раунд — GET /api/game/{game_id}/start_new_round
- 200 - сохраняем voting_id и повторяем этап голосования

##### когда 5 раундов прошли ( получили 451 от /api/game/{game_id}/start_new_round )
- GET /game/{game_id}/finish
- 200 - выводим победителей
	1. GET /api/game/{game_id}/users_info
	2. показываем все не открытые карты
- 451 - начинаем advanced режим
	1. ОН ПОКА НЕ ГОТОВ, ПОЭТОМУ СКИП
