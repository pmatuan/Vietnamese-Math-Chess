"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""


class GameState:
    def __init__(self):
        """
        Board is a 9x11 2d list, each element in list has 2 characters.
        The first character represents the color of the piece: 'b' or 'r'.
        The second character represents the value of the piece.
        "--" represents an empty space with no piece.
        """
        self.board = [
            ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9"],
            ["--", "--", "--", "--", "b0", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "r0", "--", "--", "--", "--"],
            ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
        ]
        self.redToMove = True
        self.moveLog = []
