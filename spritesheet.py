"""SpriteSheet class for frame-based animation, replacing PPlay's Animation."""

import pygame


class SpriteSheet:
    """Handles horizontal spritesheet animation.

    The source image is split into ``frame_count`` equal-width horizontal
    slices.  Call :meth:`update` each frame with the elapsed milliseconds
    and :meth:`get_current_frame` to obtain the surface to blit.
    """

    def __init__(self, surface: pygame.Surface, frame_count: int,
                 frame_duration_ms: float = 100, loop: bool = True):
        self.full_surface = surface
        self.frame_count = frame_count
        self.frame_width = surface.get_width() // frame_count
        self.frame_height = surface.get_height()
        self.frame_duration = frame_duration_ms
        self.loop = loop
        self.playing = True
        self.drawable = True
        self.current_frame = 0
        self._timer = 0.0

        # Pre-slice frames
        self.frames: list[pygame.Surface] = []
        for i in range(frame_count):
            rect = pygame.Rect(i * self.frame_width, 0,
                               self.frame_width, self.frame_height)
            self.frames.append(surface.subsurface(rect).copy())

    def update(self, dt_ms: float) -> None:
        """Advance animation by *dt_ms* milliseconds."""
        if not self.playing or self.frame_count <= 1:
            return
        self._timer += dt_ms
        while self._timer >= self.frame_duration:
            self._timer -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.playing = False
                    break

    def get_current_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame]

    def play(self) -> None:
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def stop(self) -> None:
        self.current_frame = 0
        self.playing = False
        self._timer = 0.0

    def reset(self) -> None:
        self.current_frame = 0
        self._timer = 0.0

    def hide(self) -> None:
        self.drawable = False

    def unhide(self) -> None:
        self.drawable = True

    def set_sequence_time(self, initial_frame: int, final_frame: int,
                          total_duration: float, loop: bool = True) -> None:
        """Mimic PPlay's set_sequence_time for compatibility.

        Recalculates frame duration so that frames ``initial_frame`` through
        ``final_frame - 1`` play over ``total_duration`` ms total.
        """
        n_frames = max(final_frame - initial_frame, 1)
        self.frame_duration = total_duration / n_frames
        self.current_frame = initial_frame
        self.loop = loop
        self._timer = 0.0
