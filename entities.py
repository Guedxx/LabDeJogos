"""Game entities: Paddle, Ball, HelperPaddle, PowerUp."""

import random
import pygame
from spritesheet import SpriteSheet
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_X_RANGE, POWERUP_Y_RANGE,
)


class Paddle(pygame.sprite.Sprite):
    """Static-image paddle (player or enemy)."""

    def __init__(self, surface: pygame.Surface, x: float, y: float):
        super().__init__()
        self.image = surface.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(x)
        self.y = float(y)

    def sync_rect(self) -> None:
        self.rect.topleft = (int(self.x), int(self.y))

    @property
    def width(self) -> int:
        return self.rect.width

    @property
    def height(self) -> int:
        return self.rect.height

    def draw(self, screen: pygame.Surface) -> None:
        self.sync_rect()
        screen.blit(self.image, self.rect)


class AnimatedEntity(pygame.sprite.Sprite):
    """Base for entities with spritesheet animation."""

    def __init__(self, spritesheet: SpriteSheet, x: float, y: float):
        super().__init__()
        self.spritesheet = spritesheet
        self.image = spritesheet.get_current_frame()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(x)
        self.y = float(y)

    @property
    def width(self) -> int:
        return self.spritesheet.frame_width

    @property
    def height(self) -> int:
        return self.spritesheet.frame_height

    def sync_rect(self) -> None:
        self.rect.topleft = (int(self.x), int(self.y))

    def update_animation(self, dt_ms: float) -> None:
        self.spritesheet.update(dt_ms)
        self.image = self.spritesheet.get_current_frame()

    def draw(self, screen: pygame.Surface) -> None:
        if not self.spritesheet.drawable:
            return
        self.sync_rect()
        screen.blit(self.image, self.rect)

    def hide(self) -> None:
        self.spritesheet.hide()

    def unhide(self) -> None:
        self.spritesheet.unhide()

    def collided(self, other) -> bool:
        """AABB collision check compatible with any entity type."""
        self.sync_rect()
        if isinstance(other, (Paddle, AnimatedEntity)):
            other.sync_rect()
            return self.rect.colliderect(other.rect)
        if isinstance(other, pygame.sprite.Sprite):
            return self.rect.colliderect(other.rect)
        return False


class Ball(AnimatedEntity):
    """The orb / ball."""

    def __init__(self, spritesheet: SpriteSheet, x: float, y: float,
                 vel_x: float = 0.0, vel_y: float = 0.0):
        super().__init__(spritesheet, x, y)
        self.vel_x = vel_x
        self.vel_y = vel_y


class HelperPaddle(AnimatedEntity):
    """NPC helper paddle (Dr. Rippon's helper or player helper)."""

    def __init__(self, spritesheet: SpriteSheet, x: float, y: float,
                 speed: float = 300):
        super().__init__(spritesheet, x, y)
        self.speed = speed
        self.patrol_direction = 1  # 1 = down, -1 = up


class PowerUp(AnimatedEntity):
    """Collectible power-up."""

    def __init__(self, spritesheet: SpriteSheet, power_type: str):
        # Start off-screen
        super().__init__(spritesheet, -50, -50)
        self.power_type = power_type
        self.visible = False

    def randomize_position(self) -> None:
        self.x = float(random.randint(*POWERUP_X_RANGE))
        self.y = float(random.randint(*POWERUP_Y_RANGE))
        self.visible = True

    def deactivate(self) -> None:
        self.x = -50
        self.y = -50
        self.visible = False

    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return
        super().draw(screen)
