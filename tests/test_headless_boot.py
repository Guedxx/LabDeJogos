import pygame

from game import Game


def test_game_initializes_and_steps_once_headless():
    game = Game()
    try:
        assert game.current_scene is not None
        transition = game.current_scene.update(16)
        game.current_scene.draw(game.screen)
        if transition is not None:
            assert hasattr(transition, "target")
    finally:
        pygame.quit()

