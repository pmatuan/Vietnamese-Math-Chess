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
        self.red_to_move = True
        self.checkmate = False
        self.zeroRed = (9, 4)
        self.zeroBlue = (1, 4)
        self.move_log = []

    def check(self):
        if self.board[1][4] != "b0" or self.board[9][4] != "r0":
            return True
        return False

    def makeMove(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.red_to_move = not self.red_to_move  # swap player

    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.red_to_move = not self.red_to_move  # switch turn back

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        captures = self.getAllPossibleAttacks()
        return moves + captures

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color == 'r' and self.red_to_move) or (piece_color == 'b' and not self.red_to_move):
                    piece = int(self.board[r][c][1])
                    if piece == 0:
                        continue
                    moves += self.getPieceMove(r, c, piece)
        return moves

    def getPieceMove(self, r, c, piece):
        moves = []
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        self.getMoveWithDirection(r, c, piece, directions, moves)
        return moves

    def getMoveWithDirection(self, r, c, piece, direction, moves):
        for d in direction:
            for i in range(1, piece + 1):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 11 and 0 <= end_col < 9:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space valid
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    else:
                        break
                else:
                    break

    def getAllPossibleAttacks(self):
        captures = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color == 'r' and self.red_to_move) or (piece_color == 'b' and not self.red_to_move):
                    piece = int(self.board[r][c][1])
                    if piece == 0:
                        continue
                    captures += self.getAttackMove(r, c, piece_color, piece)
        return captures

    def getAttackMove(self, r, c, piece_color, piece):
        captures = []
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for (i, j) in directions:
            if 0 <= r + i < 11 and 0 <= c + j < 9:
                team = self.board[r + i][c + j][0]
                if team == piece_color:
                    team_piece = int(self.board[r + i][c + j][1])
                    if team_piece == 0:
                        continue
                    attack_add = (piece + team_piece)
                    attack_sub = (piece - team_piece)
                    attack_multi = (piece * team_piece)
                    attack_division = (piece // team_piece)
                    attack_remainder = piece % team_piece
                    attack = [attack_add, attack_sub, attack_multi, attack_division, attack_remainder]
                    self.getAttackWithDirection((r, c), attack, (i, j), captures)
        return captures

    def getAttackWithDirection(self, piece_state, attack, direction, captures):
        enemy_color = "b" if self.red_to_move else "r"
        r, c = piece_state
        i, j = direction
        r, c = (r + i), (c + j)  # Team state
        for a in attack:
            if a <= 0:
                continue
            a = a % 10
            attack_check = True
            for k in range(1, a):
                end_row = r + direction[0] * k
                end_col = c + direction[1] * k
                if 0 <= end_row < 11 and 0 <= end_col < 9:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        continue
                    else:
                        attack_check = False
                        break
                else:
                    attack_check = False
                    break
            if attack_check:
                end_row = r + direction[0] * a
                end_col = c + direction[1] * a
                if 0 <= end_row < 11 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == enemy_color:
                        captures.append(Move(piece_state, (end_row, end_col), self.board))
