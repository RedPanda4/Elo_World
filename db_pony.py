from pony.orm import *

db = Database()

class Board(db.Entity):
    id_n = Required(int,size=64)
    fen = Required(str)
    moves = Set('Move')
    
class Move(db.Entity):
    board = Required(Board)
    move = Required(str)
    number = Required(int)

db.bind(provider="sqlite", filename='db_pnoy.sqlite', create_db=True)

db.generate_mapping(create_tables=True)
db.commit()