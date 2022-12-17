import random

class Negamax:
    def __init__(self, valid_moves):
        self.valid_moves = valid_moves
        self.CHECKMATE = 45
        self.STALEMATE = 0
    def scoreMaterial(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "r":
                    score += int(square[1])
                elif square[0] == "b":
                    score -= int(square[1])
        return score
    def findMove(self, gs):
        turn_multiplier = 1 if gs.red_to_move else -1
        max_score = -self.CHECKMATE
        best_move = None
        for player_move in self.valid_moves:
            gs.makeMove(player_move)
            score = turn_multiplier * self.scoreMaterial(gs.board)
            if score > max_score:
                max_score = score
                best_move = player_move
            gs.undoMove()
        return best_move
