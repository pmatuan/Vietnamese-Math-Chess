import random

from AI.AI import AI


class Greedy(AI):

    def findMove(self, gs, valid_moves):
        turn_multiplier = 1 if gs.red_to_move else -1
        max_score = -self.CHECKMATE
        best_move = None
        random.shuffle(valid_moves)
        for player_move in valid_moves:
            gs.makeMove(player_move)
            score = turn_multiplier * self.scoreMaterial(gs.board)
            if score > max_score:
                max_score = score
                best_move = player_move
            gs.undoMove()
        return best_move
