import random

from AI.AI import AI


class Greedy(AI):

    def findMove(self, gs, valid_moves):
        turn_multiplier = 1 if gs.red_to_move else -1
        max_score = -self.CHECKMATE
        random.shuffle(valid_moves)
        for player_move in valid_moves:
            gs.makeMove(player_move)
            score = turn_multiplier * self.scoreMaterial(gs.board)
            gs.undoMove()
            if score > max_score:
                max_score = score
                self.next_move = player_move
        return self.next_move
