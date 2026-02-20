import pygame

from game import Game
from scenes.gameplay_scene import GameplayScene


def test_pressing_n_skips_to_level_clear():
    game = Game()
    try:
        scene = GameplayScene(game, 0)
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_n})
        transition = scene.handle_events([event])
        assert transition is not None
        assert transition.target == "level_clear"
        assert transition.kwargs["level"] == 0
    finally:
        pygame.quit()


def test_pressing_n_on_final_level_goes_to_credits():
    game = Game()
    try:
        scene = GameplayScene(game, 5)
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_n})
        transition = scene.handle_events([event])
        assert transition is not None
        assert transition.target == "credits"
    finally:
        pygame.quit()

