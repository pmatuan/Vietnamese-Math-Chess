import random

from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves, depth):
        random.shuffle(valid_moves)
        self.DEPTH = depth
        self.findMoveNegaScoutIterdeep(gs, valid_moves)
        return self.next_move

    def findMoveNegaScoutIterdeep(self, gs, valid_moves):
        bestValue = -self.CHECKMATE
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        turn = 1 if gs.red_to_move else -1
        bestMove = None
        for d in range(1, self.DEPTH + 1):
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getAllPossibleMoves()
                score = -self.quiescenceSearch(gs, -beta, -alpha, -turn, d)
                gs.undoMove()
                if score > bestValue:
                    bestValue = score
                    bestMove = move
                if score >= beta:
                    break
                alpha = max(alpha, score)
            if bestMove is not None:
                self.next_move = bestMove
            depth = self.getDynamicDepth(gs, bestValue)
            if depth == 0:
                break

    def quiescenceSearch(self, gs, alpha, beta, turn, depth):
        if depth == 0:
            return turn * self.scoreMaterial(gs)
        score = turn * self.scoreMaterial(gs)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
        captures = gs.getAllPossibleAttacks()
        for move in captures:
            gs.makeMove(move)
            score = -self.quiescenceSearch(gs, -beta, -alpha, -turn, depth - 1)
            gs.undoMove()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
            beta = alpha + 1
        return alpha

    def getDynamicDepth(self, gs, score):
        if score > self.CHECKMATE:
            return self.DEPTH + 2
        elif score < -self.CHECKMATE:
            return 0
        else:
            return self.DEPTH
