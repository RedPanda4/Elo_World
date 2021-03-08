import chess.pgn
import glob
from threading import Thread, Semaphore
from copy import deepcopy
import peewee # TODO try with db to see if uses less space

import gc

CLEAN = True

boards = {}
dict_lock = Semaphore()
file_lock = Semaphore()

def join_boards(board_a, board_b):
    for key in board_b.keys():
        if key in board_a:
            for key_2 in board_b[key].keys():
                if key_2 in board_a[key]:
                    board_a[key][key_2] += board_b[key][key_2]
                else:
                    board_a[key][key_2] =board_b[key][key_2]
        else:
            board_a[key] = board_b[key]
    
    return board_a


def clean_game(game:chess.pgn.Game, local_boards: dict):
    board = game.board()
    for move in game.mainline_moves():
        
        board_fen = " ".join(board.fen().split(' ')[:4])
        if board_fen in local_boards:
            fen = local_boards[board_fen]
            
            if move.uci() in fen:
                fen[move.uci()] += 1
            
            else:
                fen[move.uci()] = 1
        
        else:
            local_boards[board_fen] = {move.uci():1,}
        board.push(move)
    
    return local_boards


files = sorted(glob.glob("**/*.pgn"))
del glob
index_file = 0
s_file = 0

n_files = len(files)
s = "{0} of {1} files| {2} games loaded"
games = 0

def thread_f(filelock: Semaphore, dict_lock: Semaphore, n):
    global index_file, boards, games, s, s_file
    while 1:
        g = 0
        file_lock.acquire()
        if index_file >= n_files:
            file_lock.release()
            return None
        else:
            file = files[index_file]
            index_file += 1
        file_lock.release()
        thread_boards = {}
        with open(file, "r") as inFile:
            game = True
            while game:
                g += 1
                game = chess.pgn.read_game(inFile)
                if game:
                    thread_boards = clean_game(game, thread_boards)
        
        dict_lock.acquire()
        games += g
        boards = deepcopy(join_boards(boards, thread_boards))
        s_file += 1
        print(s.format(s_file, n_files, games))
        gc.collect()
        dict_lock.release()
    

thread_l = [Thread(target=thread_f, args=(file_lock, dict_lock, n)) for n in range(8)]
[t.start() for t in thread_l]
[t.join() for t in thread_l]


#import json
import pickle

with open("bjson.pkl", 'wb') as Outfile:
    pickle.dump(boards, Outfile)
#with open("json.json", 'w') as Outfile:
#    Outfile.write(json.dumps(boards, indent=4))
#" ".join(board.fen().split(' ')[:4])
#print(games[0].game())