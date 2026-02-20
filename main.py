"""King Pong - Entry point.

A 6-level Pong game.
Original authors: Rafael de Lima Pereira (@RafaelLime) and Pedro Guedes Guimaraes (@Guedxx)
Refactored to pure pygame-ce with OOP architecture.
"""

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
