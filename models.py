import os
from peewee import *
from playhouse.db_url import connect

#database = PostgresqlDatabase('Bank-API', **{'host': '127.0.0.1', 'user': 'postgres', 'password': 'thegreenarrow'})
database = connect(os.environ.get('DATABASE_URL') or 'postgresql://postgres:thegreenarrow@localhost:5432/Bank-API')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Banks(BaseModel):
    id = BigAutoField()
    name = CharField(null=True)

    class Meta:
        table_name = 'banks'

class Branches(BaseModel):
    address = CharField(null=True)
    bank = ForeignKeyField(column_name='bank_id', field='id', model=Banks, null=True)
    branch = CharField(null=True)
    city = CharField(null=True)
    district = CharField(null=True)
    ifsc = CharField(primary_key=True)
    state = CharField(null=True)

    class Meta:
        table_name = 'branches'

