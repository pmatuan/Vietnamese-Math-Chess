import random

class Minimax:
    def __init__(self):
        self.CHECKMATE = 45
        self.STALEMATE = 0
        self.DEPTH = 2
        self.next_move = None
    def scoreMaterial(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "r":
                    if int(square[1]) == 0:
                        score += 1000
                    else:
                        score += int(square[1])
                elif square[0] == "b":
                    if int(square[1]) == 0:
                        score -= 1000
                    else:
                        score -= int(square[1])
        return score
    def findMove(self, gs, valid_moves):
        self.findMoveMinMax(gs, valid_moves, self.DEPTH, gs.red_to_move)
        return self.next_move

    def findMoveMinMax(self, gs, valid_moves, depth, red_to_move):
        if depth == 0:
            return self.scoreMaterial(gs.board)
        if red_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinMax(gs, next_moves, depth - 1, False)
                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                gs.undoMove()
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinMax(gs, next_moves, depth - 1, True)
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                gs.undoMove()
            return min_score