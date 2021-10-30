import telebot
import re
import peewee
from random import shuffle
import json


sqlite_db = peewee.SqliteDatabase('app.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class BaseModel(peewee.Model):
    class Meta:
        database = sqlite_db


class User(BaseModel):
    external_id = peewee.BigIntegerField(unique=True)
    chat_id = peewee.BigIntegerField(unique=True)


class Word(BaseModel):
    user = peewee.ForeignKeyField(User)
    word = peewee.CharField(max_length=255)


class Translate(BaseModel):
    user = peewee.ForeignKeyField(User)
    translate = peewee.CharField(max_length=255)


class WordTranslate(BaseModel):
    user = peewee.ForeignKeyField(User)
    word = peewee.ForeignKeyField(Word)
    translate = peewee.ForeignKeyField(Translate)


if __name__ == '__main__':
    sqlite_db.create_tables([User, Word, Translate, WordTranslate])
