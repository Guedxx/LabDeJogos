"""Pure rules for orb speed and wall/score handling."""

from __future__ import annotations

from dataclasses import dataclass

from logic.physics import accelerate_towards_cap, apply_speed_soft_limit


@dataclass(frozen=True)
class WallScoreOutcome:
    ball_x: float
    ball_y: float
    vel_x: float
    vel_y: float
    lives_player: int
    lives_enemy: int
    num_hits: int
    transition_target: str | None = None
    transition_level: int | None = None
    sounds: tuple[str, ...] = ()


def clamp_ball_speed_framewise(vel_x: float, cap: float, decay_per_frame: float = 10.0) -> float:
    """Keep legacy clamp behaviour that decays by a fixed amount each frame."""
    return apply_speed_soft_limit(vel_x, cap, decay_per_frame, 1.0)


def accelerate_ball(
    vel_x: float,
    vel_y: float,
    cruise_cap: float,
    accel_x: float,
    accel_y: float,
    dt: float,
) -> tuple[float, float]:
    """Apply progressive speed-up while preserving sign."""
    next_vx = accelerate_towards_cap(vel_x, cruise_cap, accel_x, dt)
    next_vy = accelerate_towards_cap(vel_y, cruise_cap, accel_y, dt)
    return next_vx, next_vy


def resolve_wall_and_scoring(
    *,
    ball_x: float,
    ball_y: float,
    ball_w: float,
    ball_h: float,
    vel_x: float,
    vel_y: float,
    lives_player: int,
    lives_enemy: int,
    num_hits: int,
    level_index: int,
    screen_w: float,
    screen_h: float,
    char_h: float,
) -> WallScoreOutcome:
    """Resolve wall collisions and scoring outcomes for one frame."""
    sounds: list[str] = []
    next_x = ball_x
    next_y = ball_y
    next_vx = vel_x
    next_vy = vel_y
    next_lives_player = lives_player
    next_lives_enemy = lives_enemy
    next_num_hits = num_hits

    # Right wall -> enemy scores
    if next_x + ball_w >= screen_w:
        sounds.append("hit_sound.ogg")
        next_x = screen_w - ball_w - 2
        next_lives_player -= 1
        next_vx = -(next_vx / 2)
        next_vy = next_vy / 2

    # Left wall -> player scores
    if next_x <= 0:
        sounds.append("hit_sound.ogg")
        next_x = 2
        next_lives_enemy -= 1
        next_num_hits += 1

        if next_lives_enemy <= 0 and level_index != 5:
            return WallScoreOutcome(
                ball_x=next_x,
                ball_y=next_y,
                vel_x=next_vx,
                vel_y=next_vy,
                lives_player=next_lives_player,
                lives_enemy=next_lives_enemy,
                num_hits=next_num_hits,
                transition_target="level_clear",
                transition_level=level_index,
                sounds=tuple(sounds),
            )

        if next_lives_enemy <= -1 and level_index == 5:
            return WallScoreOutcome(
                ball_x=next_x,
                ball_y=next_y,
                vel_x=next_vx,
                vel_y=next_vy,
                lives_player=next_lives_player,
                lives_enemy=next_lives_enemy,
                num_hits=next_num_hits,
                transition_target="credits",
                transition_level=None,
                sounds=tuple(sounds),
            )

        next_vx = -(next_vx - 30)
        next_vy = next_vy - 15

    # Bottom wall
    if next_y >= screen_h - ball_h:
        sounds.append("wall_sound.ogg")
        next_y = screen_h - ball_h
        next_vy *= -1

    # Top wall
    if next_y <= char_h:
        sounds.append("wall_sound.ogg")
        next_y = char_h
        next_vy *= -1

    return WallScoreOutcome(
        ball_x=next_x,
        ball_y=next_y,
        vel_x=next_vx,
        vel_y=next_vy,
        lives_player=next_lives_player,
        lives_enemy=next_lives_enemy,
        num_hits=next_num_hits,
        sounds=tuple(sounds),
    )

