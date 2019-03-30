import unittest
import game

class GameStateTest(unittest.TestCase):

    def testFoo(self):
        """Foo"""
        state = game.GameState()
        newState = state.nextYear()
        assert newState.year == 2

if __name__ == "__main__":
    unittest.main()
