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
            ["b9", "b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1"],
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
            self.redToMove = not self.redToMove  # switch turn back

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color == 'r' and self.redToMove) or (piece_color == 'b' and not self.redToMove):
                    piece = int(self.board[r][c][1])
                    self.getPieceMove(r, c, piece, moves)
                    self.getAttackMove(r, c, piece_color, piece, moves)
        return moves

    def getPieceMove(self, r, c, piece, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        self.getMoveWithDirection(r, c, piece, directions, moves)

    def getMoveWithDirection(self, r, c, piece, direction, moves):
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

    def getAttackMove(self, r, c, piece_color, piece, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for (i, j) in directions:
            if 0 <= r + i < 11 and 0 <= c + j < 9:
                team = self.board[r + i][c + j][0]
                if team == piece_color:
                    team_piece = int(self.board[r + i][c + j][1])
                    if team_piece == 0:
                        continue
                    attack_add = (piece + team_piece) % 10
                    attack_sub = (piece - team_piece) % 10
                    attack_multi = (piece * team_piece) % 10
                    attack_division = int((piece / team_piece) % 10)
                    attack_remainder = piece % team_piece
                    attack = [attack_add, attack_sub, attack_multi, attack_division, attack_remainder]
                    self.getAttackWithDirection((r, c), attack, (i, j), moves)

    def getAttackWithDirection(self, piece_state, attack, direction, moves):
        enemyColor = "b" if self.redToMove else "r"
        r, c = piece_state
        i, j = direction
        r, c = (r + i), (c + j)     # Team state
        for a in attack:
            if a == 0:
                continue
            attack_check = True
            for i in range(1, a):
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i
                if 0 <= endRow < 11 and 0 <= endCol < 9:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        continue
                    else:
                        attack_check = False
                        break
                else:
                    attack_check = False
                    break
            if attack_check:
                endRow = r + direction[0] * a
                endCol = c + direction[1] * a
                if 0 <= endRow < 11 and 0 <= endCol < 9:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor:
                        moves.append(Move(piece_state, (endRow, endCol), self.board))
