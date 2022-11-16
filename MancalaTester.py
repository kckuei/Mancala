# Author: Kevin Kuei
# GitHub ID: kckuei
# Course: CS-162
# Date: 2022-11-12, Sat., 22:28
# Description: Unit tests for Mancala.py.

import unittest
import Mancala


class MancalaTester(unittest.TestCase):
    """Unit tests for Mancala class."""
    pass


class BoardTester(unittest.TestCase):
    """Unit tests for Board class."""

    def test_closed_circuit_1(self):
        """Should correctly loop back around the board to player 1, pit 1, if
        we call the next pointer 14 times."""
        board = Mancala.Board()
        board.setup_board()
        player_1_pit_1 = board.get_pits(1)[0]
        final = player_1_pit_1
        for i in range(0, 14):
            final = final.get_next()
        self.assertEqual(final, player_1_pit_1)

    def test_closed_circuit_2(self):
        """Should correctly loop back around the board to player 1, pit 2, if
        we call the next pointer 15 times."""
        board = Mancala.Board()
        board.setup_board()
        player_1_pit_1 = board.get_pits(1)[0]
        final = player_1_pit_1
        for i in range(0, 15):
            final = final.get_next()
        self.assertEqual(final.get_player(), 1)  # Player 1
        self.assertEqual(final.get_id(), 2)      # Pit 2
        self.assertNotEqual(final, player_1_pit_1)

    def test_is_game_over(self):
        """Should correctly return game that it is a game ending condition."""
        board = Mancala.Board()
        moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        for move in moves:
            board.play_turn(*move)
        self.assertEqual(board.is_game_over(), True)

    def test_player_1_seeds_zero(self):
        """Should correctly return zero seeds for player 1 when game ending condition."""
        board = Mancala.Board()
        moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        for move in moves:
            board.play_turn(*move)
        self.assertEqual(board.get_pit_seeds(1), [0, 0, 0, 0, 0, 0])

    def test_return_winner(self):
        """Should correctly return player 2 index as correct winner."""
        board = Mancala.Board()
        moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        for move in moves:
            board.play_turn(*move)
        self.assertEqual(board.return_winner(), 2)

    def test_final_score(self):
        """Should correctly return the final scores (seeds in store) for players."""
        board = Mancala.Board()
        moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        for move in moves:
            board.play_turn(*move)
        if board.is_game_over:
            board.final_tally()
        self.assertEqual(board.get_store_seeds(1), 12)
        self.assertEqual(board.get_store_seeds(2), 36)

    def test_is_game_over_2(self):
        """Should correctly return game ending condition."""
        board = Mancala.Board()
        moves = [(1, 4), (2, 4), (1, 3), (1, 1), (2, 1), (1, 2), (1, 4), (1, 5), (2, 1),
                 (1, 6), (2, 2), (1, 3), (1, 6), (1, 1), (2, 6), (1, 2), (2, 5), (1, 5),
                 (2, 3), (1, 6), (2, 1), (1, 1), (2, 4), (1, 2), (2, 3), (1, 4), (2, 3),
                 (1, 6), (1, 5)]
        for move in moves:
            board.play_turn(*move)
        self.assertEqual(board.is_game_over(), True)

    def test_not_game_over(self):
        """Should correctly return NOT game ending condition."""
        board = Mancala.Board()
        moves = [(1, 3), (1, 1), (2, 3), (2, 4), (1, 2), (2, 2), (1, 1)]
        for move in moves:
            board.play_turn(*move)
        self.assertEqual(board.is_game_over(), False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
