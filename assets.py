"""AssetManager - loads all images and sounds once at startup."""

import os
import pygame
from spritesheet import SpriteSheet


class AssetManager:
    """Centralised asset loader.

    All images and sounds are loaded once and cached.  Background music
    uses ``pygame.mixer.music`` (streaming); every other sound uses
    ``pygame.mixer.Sound`` (multi-channel, can overlap).
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.sprites_dir = os.path.join(base_path, "Sprites")
        self.sounds_dir = os.path.join(base_path, "Sounds")
        self.images: dict[str, pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.spritesheets: dict[str, SpriteSheet] = {}

    # ------------------------------------------------------------------
    # Bulk loaders
    # ------------------------------------------------------------------
    def load_all(self) -> None:
        """Load every PNG in Sprites/ and every OGG in Sounds/."""
        self._load_images()
        self._load_sounds()

    def _load_images(self) -> None:
        for fname in os.listdir(self.sprites_dir):
            if fname.lower().endswith(".png"):
                path = os.path.join(self.sprites_dir, fname)
                self.images[fname] = pygame.image.load(path).convert_alpha()

    def _load_sounds(self) -> None:
        for fname in os.listdir(self.sounds_dir):
            if fname.lower().endswith(".ogg"):
                path = os.path.join(self.sounds_dir, fname)
                self.sounds[fname] = pygame.mixer.Sound(path)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    def get_image(self, name: str) -> pygame.Surface:
        return self.images[name]

    def get_sound(self, name: str) -> pygame.mixer.Sound:
        return self.sounds[name]

    def get_spritesheet(self, name: str, frame_count: int,
                        frame_duration_ms: float = 100,
                        loop: bool = True) -> SpriteSheet:
        """Return a *new* SpriteSheet each call (independent animation state)."""
        surface = self.images[name]
        return SpriteSheet(surface, frame_count, frame_duration_ms, loop)

    # ------------------------------------------------------------------
    # Music helpers (streaming BGM via pygame.mixer.music)
    # ------------------------------------------------------------------
    def play_music(self, name: str, loops: int = -1) -> None:
        path = os.path.join(self.sounds_dir, name)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()

    def pause_music(self) -> None:
        pygame.mixer.music.pause()

    def unpause_music(self) -> None:
        pygame.mixer.music.unpause()

    def music_playing(self) -> bool:
        return pygame.mixer.music.get_busy()

    def play_sfx(self, name: str) -> None:
        """Play a sound effect (can overlap with other sounds)."""
        self.sounds[name].play()
