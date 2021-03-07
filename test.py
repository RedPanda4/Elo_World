import chess
import chess.svg
import random
import time
import bots

def save(Board:chess.Board):
    last = Board.move_stack[-1]
    a = chess.svg.board(Board,lastmove=last, size=350)
    with open("board.svg", 'w') as outfile:
        outfile.write(a)


b = chess.Board()
p1 = bots.alphabetical()
p2 = bots.first_move()

while not b.is_game_over():
    cp = b.copy()
    if b.turn == chess.WHITE:
        b.push(p1.move(cp))
    else:
        b.push(p2.move(cp))
    save(b)
    time.sleep(0.8)
