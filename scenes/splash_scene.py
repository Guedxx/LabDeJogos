"""Splash / intro screens ("A Game Lab Project", "Made By")."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import SPLASH_DURATION, SPLASH_SPEED


class SplashScene(BaseScene):
    """Shows two timed splash screens then transitions to menu."""

    def __init__(self, game):
        super().__init__(game)
        self.screen1 = game.assets.get_image("INIT_aGameLabProject.png")
        self.screen2 = game.assets.get_image("INIT_madeBy.png")
        self.timer = SPLASH_DURATION
        self.phase = 0  # 0 = first screen, 1 = second screen

    def handle_events(self, events):
        return None

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        self.timer -= SPLASH_SPEED * dt
        if self.timer <= 0:
            if self.phase == 0:
                self.phase = 1
                self.timer = SPLASH_DURATION
            else:
                return SceneTransition("menu")
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.phase == 0:
            screen.blit(self.screen1, (0, 0))
        else:
            screen.blit(self.screen2, (0, 0))
