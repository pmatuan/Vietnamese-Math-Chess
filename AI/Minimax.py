import random

from AI.AI import AI


class Minimax(AI):

    def findMove(self, gs, valid_moves, depth):
        random.shuffle(valid_moves)
        self.DEPTH = depth
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        self.findMoveMinimax(gs, valid_moves, self.DEPTH, gs.red_to_move, alpha, beta)
        return self.next_move

    def findMoveMinimax(self, gs, valid_moves, depth, red_to_move, alpha, beta):
        if depth == 0:
            return self.quiescenceSearch(gs, alpha, beta, red_to_move)
        if red_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, False, alpha, beta)
                gs.undoMove()
                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, True, alpha, beta)
                gs.undoMove()
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        self.next_move = move
                beta = min(beta, min_score)
                if alpha >= beta:
                    break
            return min_score

    def quiescenceSearch(self, gs, alpha, beta, red_to_move):
        best_score = self.scoreMaterial(gs)
        if red_to_move:
            captures = gs.getAllPossibleAttacks()
            for move in captures:
                gs.makeMove(move)
                score = self.quiescenceSearch(gs, alpha, beta, False)
                gs.undoMove()
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        else:
            captures = gs.getAllPossibleAttacks()
            for move in captures:
                gs.makeMove(move)
                score = self.quiescenceSearch(gs, alpha, beta, True)
                gs.undoMove()
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
        return best_score
