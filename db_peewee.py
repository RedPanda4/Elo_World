from peewee import *

db = SqliteDatabase('chess_peewee.db')

class Board(Model):
    id = IntegerField(primary_key=True, unique=True)
    fen = CharField()
    
    class Meta:
        database = db

class Move(Model):
    move = CharField()
    board = ForeignKeyField(Board)
    number = IntegerField()
    
    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Board, Move])
    db.close()