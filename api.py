import requests
import config
import db 
from random import random
import logging


# Помечает сообщение как прочитанное
def mark_message_read(peer_id: int):
    data = {
        'access_token': config.TOKEN,
        'peer_id': peer_id,
        'v': 5.103
    }
    requests.post(config.URL_API + 'messages.markAsRead', data=data).text

# Помечает сообщение как решенное
def mark_message_answer(peer_id: int):
    data = {
        'access_token': config.TOKEN,
        'peer_id': peer_id,
        'v': 5.103
    }
    requests.post(config.URL_API + 'messages.markAsAnsweredConversation', 
                    data=data).text

# Отправка сообщений во все беседы
def send_message_in_all_group(message: dict) -> int:
    # Счетчик отправленных писем
    count = 0
    # Получаем текст сообщения
    text = __get_text_message(message)
    # Генерируем список вложений
    attachments = __create_list_attachments(message)
    # Пробегаемся по всем группам
    for peer_id in db.get_all_groups():
        # Отправляем сообщение в группу, прикрпеив файлы
        result = send_message(text, peer_id, attachments)
        # Если есть ошибки
        if 'error' in result:
            # Если в описании ошибки говорится, что бота кикнули
            if 'kicked' in __get_error(result):
                # Удаляем беседу из базы данных
                db.remove_groups(peer_id)
                logging.critical(f'Удалили из беседы {peer_id}')
        else:
            # Если ошибок нет, увеличиваем счетчик
            count += 1
    return count

# Отправка сообщения
def send_message(text: str, peer_id: int, attachments: str):
    data = {
        'access_token': config.TOKEN,
        'random_id': int(random() * 100000000),
        'peer_id': peer_id,
        'message': text,
        'attachment': attachments,
        'v': 5.103
    }
    return requests.post(config.URL_API + 'messages.send', data=data).json()

# Получение id пользователя из его сообщения
def get_user_id(message: dict) -> int:
    return message['object']['message']['peer_id']

#_______________________________________________________________________
#                       PRIVATE API
#_______________________________________________________________________


# Создание списка вложений
def __create_list_attachments(message: dict) -> str:
    result = ""
    # Получаем список вложений
    for attach in __get_attachments(message):
        # Получаем тип вложения
        attach_type = attach['type']
        # Получаем id обладателя вложения (группа, пользователь и т.д.)
        owner_id = ''
        if 'owner_id' in attach[attach_type]:
            owner_id = str(attach[attach_type]['owner_id'])
        elif 'from_id' in attach[attach_type]:
            owner_id = str(attach[attach_type]['from_id'])
        # Получаем id вложения
        media_id = str(attach[attach_type]['id'])
        # Добавляем в результирующую строку
        result += attach_type + owner_id + '_' + media_id
        # Если есть ключ доступа, добавляем его
        if 'access_key' in attach[attach_type]:
            result += '_' + str(attach[attach_type]['access_key'])
        result += ','
    
    # Удаляеям запятую из конца строки
    return result[:-1]

# Получение текст сообщения
def __get_text_message(message: dict) -> str:
    return message['object']['message']['text']

# Получение списка вложений
def __get_attachments(message: dict) -> dict:
    return message['object']['message']['attachments']

# Получение ошибки
def __get_error(message: dict) -> str:
    if 'error' in message:
        return message['error']['error_msg']
    else:
        return ''
