from Engine.Move import Move


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
        moves = self.getAllPossibleMoves()
        return moves

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
        self.getMoveWithDirection(r, c, piece, cross_direction, moves)
        self.getMoveWithDirection(r, c, piece, horizon_vertical_direction, moves)

    def getMoveWithDirection(self, r, c, piece, direction, moves):
        enemyColor = "b" if self.redToMove else "r"
        for d in direction:
            for i in range(1, piece + 1):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 11 and 0 <= endCol < 9:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break
