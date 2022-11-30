"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""


class GameState:
    def __init__(self):
        """
        Board is a 11x9 2d list, each element in list has 2 characters.
        The first character represents the color of the piece: 'b' or 'r'.
        The second character represents the value of the piece.
        "--" represents an empty space with no piece.
        """
        self.board = [
            ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9"],
            ["--", "--", "--", "--", "b0", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "r0", "--", "--", "--", "--"],
            ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
        ]
        self.redToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.redToMove = not self.redToMove  # swap player

    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove  # switch turns back

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    piece = int(self.board[r][c][1])
                    self.getPieceMove(r, c, piece, moves)
        return moves

    def getPieceMove(self, r, c, piece, moves):
        cross_direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        horizon_vertical_direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        self.getMoveWithDirection(r, c, piece + 1, cross_direction, moves)
        self.getMoveWithDirection(r, c, piece + 1, horizon_vertical_direction, moves)

    def getMoveWithDirection(self, r, c, piece, direction, moves):
        enemyColor = "b" if self.redToMove else "r"
        for d in direction:
            for row in range(1, piece):
                for col in range(1, piece):
                    endRow = r + d[0] * row
                    endCol = c + d[1] * col
                    if 0 <= endRow < 11 and 0 <= endCol < 9:  # on board
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                    else:
                        break


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
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
