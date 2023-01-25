import random

from AI.AI import AI


class Negascout(AI):
    def findMove(self, gs, valid_moves, depth):
        random.shuffle(valid_moves)
        self.DEPTH = depth
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        self.next_move = valid_moves[0]
        self.findMoveNegascout(gs, valid_moves, self.DEPTH, alpha, beta)
        return self.next_move

    def findMoveNegascout(self, gs, valid_moves, depth, alpha, beta):
        if depth == 0:
            return self.quiescenceSearch(gs, alpha, beta)
        b = beta
        for i, move in enumerate(valid_moves):
            gs.makeMove(move)
            next_moves = gs.getValidMoves()
            t = -self.findMoveNegascout(gs, next_moves, depth - 1, -b, -alpha)
            gs.undoMove()
            if (t > alpha) and (t < beta) and (i > 0):
                t = -self.findMoveNegascout(gs, next_moves, depth - 1, -beta, -alpha)
            alpha = max(alpha, t)
            if alpha >= beta:
                break
            b = alpha + 1
            if depth == self.DEPTH:
                if alpha > self.scoreMaterial(gs):
                    self.next_move = move
        return alpha

    def quiescenceSearch(self, gs, alpha, beta):
        best_score = self.scoreMaterial(gs)
        captures = gs.getAllPossibleAttacks()
        for move in captures:
            gs.makeMove(move)
            score = self.quiescenceSearch(gs, alpha, beta)
            gs.undoMove()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score
