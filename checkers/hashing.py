import hashlib

class TranspositionEntry:
    def __init__(self, board, value, depth, best_move):
        self.board = board
        self.value = value
        self.depth = depth
        self.best_move = best_move

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def hash_position(self, board_state):
        board_string = ''.join(str(piece) for row in board_state.get_board() for piece in row)
        return hashlib.sha256(board_string.encode()).hexdigest()

    def store(self, board, value, depth, best_move):
        hash_key = hash(board)  
        self.table[hash_key] = TranspositionEntry(board, value, depth, best_move)

    def lookup(self, board):
        hash_key = hash(board)
        return self.table.get(hash_key)