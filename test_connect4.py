import unittest
from connect4 import Connect4, PLAYER1, PLAYER2

class TestConnect4(unittest.TestCase):
    def test_initial_state(self):
        game = Connect4()
        self.assertIsNone(game.winner)
        # Ensure the board is empty
        for row in game.board:
            for cell in row:
                self.assertIsNone(cell)

    def test_play_move(self):
        game = Connect4()
        # Player1 plays in column 0
        row = game.play(PLAYER1, 0)
        self.assertEqual(game.board[row][0], PLAYER1)
        # Player2 plays in the same column
        row = game.play(PLAYER2, 0)
        self.assertEqual(game.board[row][0], PLAYER2)

if __name__ == '__main__':
    unittest.main()
