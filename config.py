from db import SETTINGS
from tinydb import Query

# Токен бота
TOKEN = SETTINGS.get(Query().TOKEN)['TOKEN']
# Ссылка на API вк
URL_API = SETTINGS.get(Query().URL_API)['URL_API']
# Секретный ключ для запросов
SECRET = SETTINGS.get(Query().SECRET)['SECRET']
# Приветсвующее сообщение
START_MESSAGE = SETTINGS.get(Query().START_MESSAGE)['START_MESSAGE']