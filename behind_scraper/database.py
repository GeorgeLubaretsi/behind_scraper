from playhouse.sqlite_ext import *

db = SqliteExtDatabase('db.sqlite')


class Name(Model):
    name = CharField(max_length=100)
    gender = JSONField(default=list)
    other_scripts = JSONField(default=list)
    usage = JSONField(default=list)
