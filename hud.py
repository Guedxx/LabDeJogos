"""HUD rendering: hearts and dash bars."""

import pygame
from settings import HEART_SEGMENT_WIDTH, DASH_SEGMENT_WIDTH, MAX_LIVES, MAX_DASHES


class HUD:
    """Draws hearts and dash bars for one side (player or enemy).

    Rather than sliding the sprite off-screen, we crop the surface to show
    only the visible portion corresponding to the current value.
    """

    def __init__(self, hearts_surface: pygame.Surface,
                 dash_surface: pygame.Surface,
                 hearts_pos: tuple[int, int],
                 dash_pos: tuple[int, int],
                 is_player: bool = True):
        self.hearts_full = hearts_surface.copy()
        self.dash_full = dash_surface.copy()
        self.hearts_pos = hearts_pos
        self.dash_pos = dash_pos
        self.is_player = is_player

        self.full_hearts_w = self.hearts_full.get_width()
        self.full_dash_w = self.dash_full.get_width()
        self.hearts_h = self.hearts_full.get_height()
        self.dash_h = self.dash_full.get_height()

    def draw(self, screen: pygame.Surface, lives: int, dashes: int) -> None:
        self._draw_hearts(screen, lives)
        self._draw_dashes(screen, dashes)

    def _draw_hearts(self, screen: pygame.Surface, lives: int) -> None:
        lives = max(0, min(lives, MAX_LIVES))
        visible_w = HEART_SEGMENT_WIDTH * lives
        if visible_w <= 0:
            return

        if self.is_player:
            # Player hearts: rightmost segments visible, crop from left
            src_x = self.full_hearts_w - visible_w
            src_rect = pygame.Rect(src_x, 0, visible_w, self.hearts_h)
            dest_x = self.hearts_pos[0] + (self.full_hearts_w - visible_w)
        else:
            # Enemy hearts: leftmost segments visible, crop from right
            src_rect = pygame.Rect(0, 0, visible_w, self.hearts_h)
            dest_x = self.hearts_pos[0]

        screen.blit(self.hearts_full, (dest_x, self.hearts_pos[1]), src_rect)

    def _draw_dashes(self, screen: pygame.Surface, dashes: int) -> None:
        dashes = max(0, min(dashes, MAX_DASHES))
        visible_w = DASH_SEGMENT_WIDTH * dashes
        if visible_w <= 0:
            return

        if self.is_player:
            src_x = self.full_dash_w - visible_w
            src_rect = pygame.Rect(src_x, 0, visible_w, self.dash_h)
            dest_x = self.dash_pos[0] + (self.full_dash_w - visible_w)
        else:
            src_rect = pygame.Rect(0, 0, visible_w, self.dash_h)
            dest_x = self.dash_pos[0]

        screen.blit(self.dash_full, (dest_x, self.dash_pos[1]), src_rect)
