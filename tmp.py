from tinydb import TinyDB, Query
from tinydb.operations import delete

db = TinyDB('db.json')
GROUPS = db.table('groups')
SETTINGS = db.table('settings')
ADMIN = db.table('admin')

