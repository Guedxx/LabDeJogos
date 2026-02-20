"""Pause overlay scene - replaces pause() and confirmExit()."""

import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import (
    PAUSE_RETURN_AREA, PAUSE_MENU_AREA, PAUSE_QUIT_AREA,
    CONFIRM_YES_AREA, CONFIRM_NO_AREA,
)


class PauseScene(BaseScene):
    """Pause menu overlay.  Keeps a reference to the gameplay scene so it
    can be resumed."""

    def __init__(self, game, level: int, gameplay_scene):
        super().__init__(game)
        self.level = level
        self.gameplay_scene = gameplay_scene
        assets = game.assets

        self.pause_img = assets.get_image("PAUSEneutro.png")
        self.return_img = assets.get_image("PAUSEreturn.png")
        self.menu_img = assets.get_image("PAUSEmenu.png")
        self.quit_img = assets.get_image("PAUSEquit.png")
        self.sure_img = assets.get_image("PAUSEsure.png")
        self.sure_yes_img = assets.get_image("PAUSEsureYes.png")
        self.sure_no_img = assets.get_image("PAUSEsureNo.png")

        self.confirming = False  # True when "Are you sure?" dialog shown
        self.confirm_action = None  # "menu" or "quit"

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.confirming:
            return self._handle_confirm(mouse_pos, mouse_click)
        return self._handle_pause(mouse_pos, mouse_click)

    def _handle_pause(self, mouse_pos, mouse_click):
        # Return to game
        if _in_area(mouse_pos, PAUSE_RETURN_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                return SceneTransition("resume_gameplay",
                                       gameplay_scene=self.gameplay_scene)

        # Menu
        if _in_area(mouse_pos, PAUSE_MENU_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.confirming = True
                self.confirm_action = "menu"

        # Quit
        if _in_area(mouse_pos, PAUSE_QUIT_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.confirming = True
                self.confirm_action = "quit"

        return None

    def _handle_confirm(self, mouse_pos, mouse_click):
        if _in_area(mouse_pos, CONFIRM_NO_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                self.confirming = False
                return None

        if _in_area(mouse_pos, CONFIRM_YES_AREA):
            if mouse_click:
                self.game.assets.play_sfx("MENUSelect.ogg")
                if self.confirm_action == "menu":
                    return SceneTransition("menu")
                elif self.confirm_action == "quit":
                    return SceneTransition("quit")

        return None

    def update(self, dt_ms):
        return None

    def draw(self, screen):
        # Draw the frozen gameplay underneath
        self.gameplay_scene.draw(screen)

        mouse_pos = pygame.mouse.get_pos()

        if self.confirming:
            screen.blit(self.sure_img, (0, 0))
            if _in_area(mouse_pos, CONFIRM_YES_AREA):
                screen.blit(self.sure_yes_img, (0, 0))
            if _in_area(mouse_pos, CONFIRM_NO_AREA):
                screen.blit(self.sure_no_img, (0, 0))
        else:
            screen.blit(self.pause_img, (0, 0))
            if _in_area(mouse_pos, PAUSE_RETURN_AREA):
                screen.blit(self.return_img, (0, 0))
            if _in_area(mouse_pos, PAUSE_MENU_AREA):
                screen.blit(self.menu_img, (0, 0))
            if _in_area(mouse_pos, PAUSE_QUIT_AREA):
                screen.blit(self.quit_img, (0, 0))


def _in_area(pos, area) -> bool:
    (x1, y1), (x2, y2) = area
    return x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2
