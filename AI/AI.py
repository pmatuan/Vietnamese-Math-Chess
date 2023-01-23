import random


class AI:
    def __init__(self):
        self.CHECKMATE = 45
        self.STALEMATE = 0
        self.DEPTH = 3
        self.next_move = None

    def scoreMaterial(self, gs):
        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == "r":
                    if int(square[1]) == 0:
                        score += self.CHECKMATE
                    else:
                        score += int(square[1])
                elif square[0] == "b":
                    if int(square[1]) == 0:
                        score -= self.CHECKMATE
                    else:
                        score -= int(square[1])
        score += self.scoreZeroSafety(gs.board)
        return score

    def scoreZeroSafety(self, board):
        red_direction = ((-1, -1), (-1, 1), (-1, 0), (0, -1), (0, 1))
        blue_direction = ((0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        score = 0
        for d in red_direction:
            for i in range(1, 4, 1):
                if board[d[0]*i][d[1]*i][0] == 'b':
                    score -= 1
        for d in blue_direction:
            for i in range(1, 4, 1):
                if board[d[0]*i][d[1]*i][0] == 'r':
                    score += 1
        return score

    def quiescenceSearch(self, gs, alpha, beta, turn):
        best_score = turn * self.scoreMaterial(gs)
        alpha = max(alpha, best_score)
        if alpha >= beta:
            return best_score
        captures = gs.getAllPossibleAttacks()
        for move in captures:
            gs.makeMove(move)
            score = -self.quiescenceSearch(gs, -beta, -alpha, -turn)
            gs.undoMove()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return alpha
    
    def findRandomMove(self, valid_moves):
        return random.choice(valid_moves)
