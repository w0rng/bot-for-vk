from flask import Flask, request, abort
import db
import api
from config import START_MESSAGE, SECRET
import logging


app = Flask(__name__)
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', 
                    filename = 'log')

# Главное тело бота
def bot(json: dict) -> None:
    peer_id = api.get_user_id(json)
    # Если написал администратор
    if db.is_admin(peer_id):
        logging.critical(f'Написал {peer_id}')
        # Отмечаем сообщение как отвеченное
        api.mark_message_answer(peer_id)
        # Отмечаем сообщение как прочитанное
        api.mark_message_read(peer_id)
        # Рассылаем сообщение всем и считаем количество отправленных писем
        count_messages_sent = api.send_message_in_all_group(json)
        # Если хоть кому-то отправили
        if count_messages_sent:
            # Уведомляем администратора
            api.send_message(f'Разослал в {count_messages_sent} бесед', peer_id, [])
        else:
            # Иначе говорим, что все плохо
            api.send_message(f'Нет зарегистрированных групп :c', peer_id, [])
    # Если бота добавили в новую конфу, регаем его
    elif peer_id > 2000000000 and db.check_group(peer_id):
        logging.critical(f'Добавили в беседу {peer_id}')
        # Отправляем приветственное сообщение
        api.send_message(START_MESSAGE, peer_id, [])


@app.route('/', methods=['GET', 'POST'])
def main():
    # Если пришел нужный запрос и серветный ключ верный
    if request.json and request.json['secret'] == SECRET:
        # Запускаем итерацию бота
        bot(request.json)
        return 'ok'
    else:
        # Иначе шлем скрипткиди нахуй
        abort(405)


if __name__ == '__main__':
    # Запуск сервера
    app.run(host='0.0.0.0', port=80)
