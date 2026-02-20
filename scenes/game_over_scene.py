"""Game over scene - character fall + bounce animation, try again / quit."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import (
    GAMEOVER_FALL_ACCEL, GAMEOVER_TOWER_ACCEL, GAMEOVER_LATERAL_ACCEL,
    GAMEOVER_BOUNCE_COUNT, GAMEOVER_TOWER_Y_STOP, GAMEOVER_FLOOR_Y,
    GAMEOVER_WALKING_SPEED, GAMEOVER_WALKING_EXIT_X,
    GAMEOVER_QUIT_AREA, GAMEOVER_RETRY_AREA,
)
from spritesheet import SpriteSheet


class GameOverScene(BaseScene):
    """Game over animation with fall, bounce, and retry/quit choice."""

    def __init__(self, game, level: int):
        super().__init__(game)
        self.level = level
        assets = game.assets

        # Tower background
        self.tower_surf = assets.get_image("ANIMATIONGameOver.png")
        self.tower_x = 2.0
        self.tower_y = 0.0

        # Falling character
        self.fall_sheet = assets.get_spritesheet(
            "ANIMATIONGameOverChar.png", 8, 50)
        self.fall_x = 750.0
        self.fall_y = 100.0

        # Sleeping character
        self.sleep_sheet = assets.get_spritesheet(
            "ANIMATIONGameOverEepy.png", 6, 300)
        self.sleep_x = 540.0
        self.sleep_y = 579.0
        self.show_sleep = False

        # Walking character
        self.walk_sheet = assets.get_spritesheet(
            "ANIMATIONGameOverWalking.png", 4, 150)
        self.walk_x = 540.0
        self.walk_y = 578.0
        self.show_walk = False

        # Text overlays
        self.game_over_surf = assets.get_image("ANIMATIONGameOverText.png")
        self.yes_surf = assets.get_image("ANIMATIONGameOverTextYes.png")
        self.no_surf = assets.get_image("ANIMATIONGameOverTextNo.png")

        # Animation state
        self.bounce_count = 0
        self.fall_accel = float(GAMEOVER_FALL_ACCEL)
        self.tower_accel = float(GAMEOVER_TOWER_ACCEL)
        self.lateral_accel = float(GAMEOVER_LATERAL_ACCEL)
        self.show_fall = True
        self.tried_again = False

        # Play explosion sound
        assets.play_sfx("ANIMATIONexplosion.ogg")

    def handle_events(self, events):
        if self.bounce_count < GAMEOVER_BOUNCE_COUNT:
            return None

        if self.tried_again:
            return None

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Quit button
        if _in_area(mouse_pos, GAMEOVER_QUIT_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                return SceneTransition("menu")

        # Try again button
        if _in_area(mouse_pos, GAMEOVER_RETRY_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.show_sleep = False
                self.show_walk = True
                self.tried_again = True

        return None

    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        if dt <= 0:
            return None

        self.fall_sheet.update(dt_ms)
        self.sleep_sheet.update(dt_ms)
        self.walk_sheet.update(dt_ms)

        # Tower scrolling down
        if self.tower_y >= GAMEOVER_TOWER_Y_STOP:
            self.tower_y -= self.tower_accel * dt
            self.tower_accel += 100 * dt
        if self.tower_y <= GAMEOVER_TOWER_Y_STOP:
            self.tower_y = GAMEOVER_TOWER_Y_STOP

        # Lateral throw
        if self.fall_x >= 540:
            self.fall_x -= (200 + self.lateral_accel) * dt
            self.lateral_accel -= 100 * dt

        # Falling after tower stops
        if (self.tower_y <= GAMEOVER_TOWER_Y_STOP
                and self.fall_y < GAMEOVER_FLOOR_Y):
            self.fall_y += self.fall_accel * dt
            self.fall_accel += 400 * dt

        # Bouncing
        if (self.tower_y <= GAMEOVER_TOWER_Y_STOP
                and self.fall_y >= GAMEOVER_FLOOR_Y
                and self.bounce_count <= GAMEOVER_BOUNCE_COUNT):
            self.fall_y += self.fall_accel * dt

            if self.fall_y > GAMEOVER_FLOOR_Y:
                self.game.assets.play_sfx("ANIMATIONHurt.ogg")
                self.bounce_count += 1

                # Recreate sheet with slower animation
                dur = max(50 * self.bounce_count, 50)
                self.fall_sheet = self.game.assets.get_spritesheet(
                    "ANIMATIONGameOverChar.png", 8, dur / 8)

                self.show_fall = False
                self.show_sleep = True
                self.fall_y = GAMEOVER_FLOOR_Y
                self.fall_accel *= -1
                self.fall_accel /= 2
                self.fall_accel += 20
            else:
                self.show_fall = True
                self.show_sleep = False

        # Walking exit
        if self.tried_again:
            self.walk_x += GAMEOVER_WALKING_SPEED * dt
            if self.walk_x >= GAMEOVER_WALKING_EXIT_X:
                return SceneTransition("gameplay", level=self.level)

        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.tower_surf, (int(self.tower_x), int(self.tower_y)))

        if self.show_fall:
            screen.blit(self.fall_sheet.get_current_frame(),
                        (int(self.fall_x), int(self.fall_y)))

        if self.show_sleep:
            screen.blit(self.sleep_sheet.get_current_frame(),
                        (int(self.sleep_x), int(self.sleep_y)))

        if self.bounce_count >= GAMEOVER_BOUNCE_COUNT and not self.tried_again:
            screen.blit(self.game_over_surf, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            if _in_area(mouse_pos, GAMEOVER_QUIT_AREA):
                screen.blit(self.yes_surf, (0, 0))
            if _in_area(mouse_pos, GAMEOVER_RETRY_AREA):
                screen.blit(self.no_surf, (0, 0))

        if self.show_walk:
            screen.blit(self.walk_sheet.get_current_frame(),
                        (int(self.walk_x), int(self.walk_y)))


def _in_area(pos, area) -> bool:
    (x1, y1), (x2, y2) = area
    return x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2
