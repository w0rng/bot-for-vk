from tinydb import TinyDB, Query

# Получаем базу данных
db = TinyDB('db.json')
# Получаем таблицу групп
GROUPS = db.table('groups')
# Получаем настройки
SETTINGS = db.table('settings')
# Получаем таблицу админов
ADMIN = db.table('admin')


# Метод провери является ли id админом
def is_admin(peer_id: int) -> bool:
    return ADMIN.search(Query().id == peer_id)

# Проверка новая ли это беседа
def check_group(peer_id: int) -> bool:
    # Если id нет в базе
    if not GROUPS.search(Query().id == peer_id):
        # Добавляем его
        GROUPS.insert({'id': peer_id})
        return True
    else:
        return False

# Получение списка всех бесед
def get_all_groups() -> list:
    return [group['id'] for group in GROUPS.all()]

# Удаление беседы
def remove_groups(peer_id: int) -> None:
    GROUPS.remove(Query().id == peer_id)
