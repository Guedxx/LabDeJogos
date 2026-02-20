"""Level clear / victory tower animation - replaces passou_fase()."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import LEVEL_CLEAR_DATA


class LevelClearScene(BaseScene):
    """Shows the tower climbing animation when a level is cleared."""

    def __init__(self, game, level: int):
        super().__init__(game)
        self.level = level
        assets = game.assets

        self.tower_surf = assets.get_image("ANIMATIONTower.png")
        self.head_surf = assets.get_image("ANIMATIONPlayerHead.png")

        # Enemy felled animation (background for the scene)
        self.felled_sheet = assets.get_spritesheet(
            "ANIMATIONEnemyFelled.png", 3, 250)
        self.felled_sheet.play()

        # Use felled frame 1 as static background
        self.bg_sheet = assets.get_spritesheet(
            "ANIMATIONEnemyFelled.png", 3, 50000)
        self.bg_sheet.set_sequence_time(1, 2, 50000)

        # Get level-specific positions
        data = LEVEL_CLEAR_DATA[level]
        self.tower_y = float(data["tower_y"])
        self.head_x = float(data["head_x"])
        self.head_y = float(data["head_y"])
        self.target_head_y = float(data["target_head_y"])
        self.target_tower_y = float(data["target_tower_y"])

        # Phase: "felled" then "climb"
        self.phase = "felled"
        self.timer = 20.0
        self.accel = 100.0
        self.climb_timer = 30.0

    def handle_events(self, events):
        return None

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        if dt <= 0:
            return None

        if self.phase == "felled":
            self.felled_sheet.update(dt_ms)
            self.timer -= 10 * dt
            if self.timer <= 0:
                self.phase = "climb"
            return None

        # Climb phase
        if self.accel >= 0:
            self.accel -= 10 * dt
        if self.head_y > self.target_head_y:
            self.head_y -= (10 + self.accel) * dt
        if self.tower_y < self.target_tower_y:
            self.tower_y += (10 + self.accel) * dt

        self.climb_timer -= 10 * dt
        if self.climb_timer <= 0:
            next_level = self.level + 1
            if next_level >= 6:
                return SceneTransition("credits")
            return SceneTransition("gameplay", level=next_level)

        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))

        if self.phase == "felled":
            screen.blit(self.felled_sheet.get_current_frame(), (0, 0))
        else:
            screen.blit(self.bg_sheet.get_current_frame(), (0, 0))
            screen.blit(self.tower_surf, (0, int(self.tower_y)))
            screen.blit(self.head_surf, (int(self.head_x), int(self.head_y)))
