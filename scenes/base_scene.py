"""Base scene ABC."""

from abc import ABC, abstractmethod
import pygame


class SceneTransition:
    """Describes a transition to another scene."""

    def __init__(self, target: str, **kwargs):
        self.target = target
        self.kwargs = kwargs


class BaseScene(ABC):
    """Abstract base for all scenes."""

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]):
        """Process input events.  Return SceneTransition or None."""

    @abstractmethod
    def update(self, dt_ms: float):
        """Update logic.  Return SceneTransition or None."""

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Render the scene."""
