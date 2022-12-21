import random

from AI.AI import AI


class Minimax(AI):

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveMinimax(gs, valid_moves, self.DEPTH, gs.red_to_move)
        return self.next_move

    def findMoveMinimax(self, gs, valid_moves, depth, red_to_move):
        if depth == 0:
            return self.scoreMaterial(gs.board)
        if red_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, False)
                gs.undoMove()
                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, True)
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                gs.undoMove()
            return min_score