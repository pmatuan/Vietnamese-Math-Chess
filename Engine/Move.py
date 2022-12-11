class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is
    # corresponding to rows) and the second one being a letter between a-f (corresponding to columns), in order to
    # use this notation we need to map our [row][col] coordinates to match the ones used in the original chess game
    ranks_to_rows = {"1": 10, "2": 9, "3": 8, "4": 7, "5": 6, "6": 5,
                     "7": 4, "8": 3, "9": 2, "10": 1, "11": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                     "f": 5, "g": 6, "h": 7, "i": 8}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, startSq, endSq, board):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)

    def getRankFile(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
