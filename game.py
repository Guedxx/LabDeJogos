"""Game class - initialisation, scene management, main loop."""

import os
import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from assets import AssetManager
from scenes.splash_scene import SplashScene
from scenes.menu_scene import MenuScene
from scenes.gameplay_scene import GameplayScene
from scenes.pause_scene import PauseScene
from scenes.game_over_scene import GameOverScene
from scenes.level_clear_scene import LevelClearScene
from scenes.credits_scene import CreditsScene


class Game:
    """Top-level game object.  Owns the display, clock, assets, and scene."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        # Try to set icon
        project_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(project_dir, "IconKP.ico")
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
            except pygame.error:
                pass

        self.clock = pygame.time.Clock()
        self.assets = AssetManager(project_dir)
        self.assets.load_all()

        self.running = True
        self.difficulty = 0
        self.current_level = 0
        self.current_scene = SplashScene(self)

    def run(self) -> None:
        """Main loop with proper FPS cap."""
        while self.running:
            dt_ms = self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            if not self.running:
                break

            transition = self.current_scene.handle_events(events)
            if not transition:
                transition = self.current_scene.update(dt_ms)
            if transition:
                self._change_scene(transition)
                if not self.running:
                    break

            self.current_scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def _change_scene(self, transition) -> None:
        target = transition.target
        kw = transition.kwargs

        if target == "menu":
            self.current_scene = MenuScene(self)
        elif target == "gameplay":
            level = kw.get("level", 0)
            self.current_level = level
            self.current_scene = GameplayScene(self, level)
        elif target == "pause":
            self.current_scene = PauseScene(
                self,
                level=kw["level"],
                gameplay_scene=kw["gameplay_scene"])
        elif target == "resume_gameplay":
            self.current_scene = kw["gameplay_scene"]
        elif target == "game_over":
            level = kw.get("level", self.current_level)
            self.current_scene = GameOverScene(self, level)
        elif target == "level_clear":
            level = kw.get("level", self.current_level)
            self.current_scene = LevelClearScene(self, level)
        elif target == "credits":
            self.current_scene = CreditsScene(self)
        elif target == "quit":
            self.running = False
