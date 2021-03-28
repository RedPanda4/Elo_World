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

Values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}


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


class _hubble_swarm(Bot):
    def move(self, board: chess.Board, turn: bool = True):
        moves_by_distance = {}
        for move in board.legal_moves:
            cp = board.copy()
            cp.push(move)
            king_position = cp.king(turn)
            total_distance = sum([chess.square_distance(square, king_position)
                                  for (square, piece) in cp.piece_map().items()
                                  if piece.color == board.turn])
            if total_distance in moves_by_distance:
                moves_by_distance[total_distance].append(move)
            else:
                moves_by_distance[total_distance] = [move, ]
        distance = min(moves_by_distance.keys())
        return random.choice(moves_by_distance[distance])


class huddle(_hubble_swarm):

    def move(self, board: chess.Board, **kwargs):
        return super().move(board, board.turn)


class swarm(_hubble_swarm):

    def move(self, board: chess.Board, **kwargs):
        return super().move(board, not board.turn)


class generous(Bot):

    def move(self, board: chess.Board):
        turn = board.turn
        moves = []
        for move in board.legal_moves:
            points = 0
            cp = board.copy()
            cp.push(move)
            piece_map = cp.piece_map()
            for square in piece_map:
                if piece_map[square].color == turn:
                    attakers = len(cp.attackers(not turn, square))
                    piece = Values[piece_map[square].symbol().capitalize()]
                    points += attakers * piece
            moves.append((points, move.uci()))
        points = max(moves)[0]
        moves = [move[1] for move in moves if move[0] == points]
        return chess.Move.from_uci(random.choice(moves))


class no_i_insist(Bot):

    def move(self, board: chess.Board):
        moves = {}
        capture = {}
        check = []
        for move in board.legal_moves:
            board_move = board.copy()
            board_move.push(move)
            if board_move.is_check():
                check.append(move)
                continue
            if board.is_capture(move):
                piece = Values[board.piece_at(move.to_square).symbol().capitalize()]
                if piece in capture:
                    capture[piece].append(move)
                else:
                    capture[piece] = [move, ]
                continue

            possible_moves = board_move.legal_moves.count()
            captures = 0.0
            points = 0.0
            for move_s in board_move.legal_moves:
                if board_move.is_capture(move_s):
                    captures += 1
                    if board_move.is_en_passant(move_s):
                        points += 1
                    else:
                        points += Values[board_move.piece_at(move_s.to_square).symbol().capitalize()]
            final_score = (captures / possible_moves, points / possible_moves)
            if final_score in moves:
                moves[final_score].append(move)
            else:
                moves[final_score] = [move,]

        if moves:
            return random.choice(moves[sorted(moves.keys())[-1]])
        if capture:
            return random.choice(capture[sorted(capture.keys())[0]])
        return random.choice(check)


class reverse_starting(Bot):
    pass


class cccp(Bot):

    def move(self, board: chess.Board):
        checks = []
        captures = []
        for move in board.legal_moves:
            cp = board.copy()
            cp.push(move)
            if cp.is_checkmate():
                return move
            elif cp.is_check():
                checks.append(move)
            elif board.is_capture(move):
                captures.append(captures)
        if checks:
            return random.choice(checks)
        if captures:
            return random.choice(captures)
        huddle_b = huddle()
        return huddle_b.move(board, )
