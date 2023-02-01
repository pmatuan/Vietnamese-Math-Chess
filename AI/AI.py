import random


class AI:
    def __init__(self):
        self.CHECKMATE = 45
        self.DEPTH = 3
        self.next_move = None
        self.next_move1 = None

    def scoreMaterial(self, gs):
        score = 0
        for row in gs.board:
            for square in row:
                if square == "r0":
                    score += self.CHECKMATE
                elif square == "b0":
                    score -= self.CHECKMATE
                elif square[0] == "r":
                    score += int(square[1])
                elif square[0] == "b":
                    score -= int(square[1])
        score += self.scoreZeroSafety(gs.board)
        return score

    def scoreZeroSafety(self, board):
        score = 0
        red_direction = ((-1, -1), (-1, 1), (-1, 0), (0, -1), (0, 1))
        blue_direction = ((0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for d in red_direction:
            for i in range(1, 4, 1):
                if board[d[0] * i][d[1] * i][0] == 'b':
                    score -= 4 - i
        for d in blue_direction:
            for i in range(1, 4, 1):
                if board[d[0] * i][d[1] * i][0] == 'r':
                    score += 4 - i
        return score

    def findRandomMove(self, valid_moves):
        return random.choice(valid_moves)