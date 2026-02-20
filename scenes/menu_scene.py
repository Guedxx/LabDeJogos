"""Main menu scene."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MENU_PLAY_AREA, MENU_DIFF_AREA, MENU_QUIT_AREA,
    MENU_SIDEBAR_INITIAL_X, MENU_SIDEBAR_DECEL, MENU_SIDEBAR_SPEED,
    DIFFICULTY_COOLDOWN, MENU_BG_DURATIONS,
)
from spritesheet import SpriteSheet


class MenuScene(BaseScene):
    """Main menu with background animation, sidebar slide-in, difficulty toggle."""

    def __init__(self, game):
        super().__init__(game)
        assets = game.assets

        # Logo / press-space screen
        self.logo = assets.get_image("INIT_LOGO.png")

        # Animated backgrounds per difficulty
        self.bg_easy = assets.get_spritesheet(
            "MENU_bg_easy.png", 3, MENU_BG_DURATIONS["easy"] / 3)
        self.bg_normal = assets.get_spritesheet(
            "MENU_bg_normal.png", 3, MENU_BG_DURATIONS["normal"] / 3)
        self.bg_hard = assets.get_spritesheet(
            "MENU_bg_hard.png", 3, MENU_BG_DURATIONS["hard"] / 3)

        # Sidebars per difficulty
        self.side_easy = assets.get_image("MENU_side_easy.png")
        self.side_normal = assets.get_image("MENU_side_normal.png")
        self.side_hard = assets.get_image("MENU_side_hard.png")

        # Little animated character
        self.lil_man = assets.get_spritesheet("MENU_Char.png", 4, 100)
        self.lil_man_pos = (220, 445)

        # State
        self.phase = "press_space"  # "press_space" -> "slide_in" -> "main"
        self.difficulty = 0   # -1=easy, 0=normal, 1=hard
        self.diff_cooldown = 0.0
        self.sidebar_x = float(MENU_SIDEBAR_INITIAL_X)
        self.decel = 0.0

        # Music
        self._music_name = "menu.ogg"
        assets.play_music("menu.ogg")

    def _current_bg(self) -> SpriteSheet:
        if self.difficulty == -1:
            return self.bg_easy
        if self.difficulty == 1:
            return self.bg_hard
        return self.bg_normal

    def _current_side(self) -> pygame.Surface:
        if self.difficulty == -1:
            return self.side_easy
        if self.difficulty == 1:
            return self.side_hard
        return self.side_normal

    def _switch_music(self) -> None:
        if self.difficulty == 0:
            name = "menu.ogg"
        elif self.difficulty == 1:
            name = "menuHARD.ogg"
        else:
            name = "menuEASY.ogg"
        if name != self._music_name:
            self._music_name = name
            self.game.assets.play_music(name)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.phase == "press_space":
            if keys[pygame.K_SPACE]:
                self.phase = "slide_in"
                self.sidebar_x = float(MENU_SIDEBAR_INITIAL_X)
                self.decel = 0.0
            return None

        if self.phase != "main":
            return None

        # Play button
        if self._mouse_in_area(mouse_pos, MENU_PLAY_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.game.assets.pause_music()
                return SceneTransition("gameplay", level=0)

        # Difficulty button
        self.diff_cooldown = max(0, self.diff_cooldown)
        if self._mouse_in_area(mouse_pos, MENU_DIFF_AREA):
            if mouse_click and self.diff_cooldown <= 0:
                self.game.assets.play_sfx("MENUSelect.ogg")
                if self.difficulty < 1:
                    self.difficulty += 1
                else:
                    self.difficulty = -1
                self.diff_cooldown = DIFFICULTY_COOLDOWN
                self._switch_music()
                self.game.difficulty = self.difficulty

        # Quit button
        if self._mouse_in_area(mouse_pos, MENU_QUIT_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.game.assets.pause_music()
                return SceneTransition("quit")

        return None

    def update(self, dt_ms):
        dt = dt_ms / 1000.0

        # Keep music looping
        if not self.game.assets.music_playing():
            self.game.assets.play_music(self._music_name)

        # Animate backgrounds
        self._current_bg().update(dt_ms)
        self.lil_man.update(dt_ms)

        # Difficulty cooldown
        self.diff_cooldown -= 60 * dt

        # Sidebar slide-in
        if self.phase == "slide_in":
            self.decel += MENU_SIDEBAR_DECEL * dt
            self.sidebar_x += (MENU_SIDEBAR_SPEED - self.decel) * dt
            if self.sidebar_x >= 0:
                self.sidebar_x = 0
                self.phase = "main"

        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        bg = self._current_bg()
        screen.blit(bg.get_current_frame(), (0, 0))

        if self.phase == "press_space":
            screen.blit(self.logo, (0, 0))
            screen.blit(self.lil_man.get_current_frame(), self.lil_man_pos)
            return

        # Sidebar (during slide-in or main)
        side = self._current_side()
        screen.blit(side, (int(self.sidebar_x), 0))

    @staticmethod
    def _mouse_in_area(pos, area) -> bool:
        (x1, y1), (x2, y2) = area
        return x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2
