"""Credits scene - "You're the King Pong" + credits scroll."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import CREDITS_SCROLL_SPEED, CREDITS_END_Y, ENDGAME_DISPLAY_TIME


class CreditsScene(BaseScene):
    """Shows the endgame message then scrolls credits."""

    def __init__(self, game):
        super().__init__(game)
        assets = game.assets
        self.endgame_surf = assets.get_image("ENDGAME.png")
        self.credits_surf = assets.get_image("ENDGAMECREDITS.png")
        self.credits_y = 0.0
        self.phase = "endgame"  # "endgame" -> "scroll"
        self.timer = float(ENDGAME_DISPLAY_TIME)

    def handle_events(self, events):
        return None

    def update(self, dt_ms):
        dt = dt_ms / 1000.0

        if self.phase == "endgame":
            self.timer -= 10 * dt
            if self.timer <= 0:
                self.phase = "scroll"
            return None

        # Scroll credits up
        self.credits_y -= CREDITS_SCROLL_SPEED * dt
        if self.credits_y <= CREDITS_END_Y:
            return SceneTransition("menu")
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.phase == "endgame":
            screen.blit(self.endgame_surf, (0, 0))
        else:
            screen.blit(self.credits_surf, (0, int(self.credits_y)))
