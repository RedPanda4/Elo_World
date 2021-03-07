import chess
import random
from typing import List

white_spaces = ["a2", "a4", "a6", "a8", "b1", "b3", "b5", "b7",
                "c2", "c4", "c6", "c8", "d1", "d3", "d5", "d7",
                "e2", "e4", "e6", "e8", "f1", "f3", "f5", "f7",
                "g2", "g4", "g6", "g8", "h1", "h3", "h5", "h7",
                ]

black_spaces = ["a1", "a3", "a5", "a7", "b2", "b4", "b6", "b8",
                "c1", "c3", "c5", "c7", "d2", "d4", "d6", "d8",
                "e1", "e3", "e5", "e7", "f2", "f4", "f6", "f8",
                "g1", "g3", "g5", "g7", "h2", "h4", "h6", "h8",
                ]

Vaules = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9}


class Bot:
    def __init__(self):
        pass

    def move(self, board: chess.Board):
        raise NotImplementedError


class random_move(Bot):

    def move(self, board: chess.Board):
        return random.choice(list(board.legal_moves))


class same_color(Bot):

    def move(self, board: chess.Board):

        if board.turn == chess.WHITE:
            color_space = white_spaces
        else:
            color_space = black_spaces

        moves = [move for move in board.legal_moves if move.uci()[2:4]
                 in color_space]

        if not moves:
            moves = list(board.legal_moves)

        return random.choice(moves)


class oposite_color(Bot):

    def move(self, board: chess.Board):

        if board.turn == chess.WHITE:
            color_space = black_spaces
        else:
            color_space = white_spaces

        moves = [move for move in board.legal_moves if move.uci()[2:4]
                 in color_space]

        if not moves:
            moves = list(board.legal_moves)

        return random.choice(moves)


class pacifist(Bot):
    """
    1.Avoid moves that mate the opponent
    2.avoid moves that check
    3.avoid moves that capture pieces
    4.capture lower value pieces. Break ties randomly.

    """

    def move(self, board: chess.Board):
        """
        arg moves 
        """
        moves: List[List, List, List, List, List,
                    List, List] = [[], [], [], [], [], [], []]
        # moves 0_Checkmate, 1_Checks, 2_QueenKill, 3_RookKill, 4_OrthersKill, 5_PawnKill, 6_Move

        for move in board.legal_moves:
            cp = board.copy()
            cp.push(move)
            if cp.is_checkmate():
                moves[0].append(move)
            elif board.gives_check(move):
                moves[1].append(move)
            elif board.is_en_passant(move):
                moves[5].append(move)
            elif board.is_capture(move):
                piece = (board.piece_at(chess.parse_square(
                    move.uci()[2:4]))).symbol().capitalize()
                if piece == 'Q':
                    moves[2].append(move)
                elif piece == 'R':
                    moves[3].append(move)
                elif piece == 'P':
                    moves[5].append(move)
                else:
                    moves[4].append(move)
            else:
                moves[6].append(move)

        choices = moves.pop()
        while not choices:
            choices = moves.pop()
        return random.choice(choices)


class first_move(Bot):

    def move(self, board: chess.Board):
        return list(board.legal_moves)[0]

class alphabetical(Bot):
    
    def move(self, board: chess.Board):
        move = sorted([move.uci() for move in board.legal_moves])[0]
        return chess.Move.from_uci(move)
        