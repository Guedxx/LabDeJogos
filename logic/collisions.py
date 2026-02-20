"""Pure collision helpers shared by gameplay systems."""

from __future__ import annotations


def resolve_paddle_bounce(
    *,
    ball_x: float,
    ball_y: float,
    ball_w: float,
    ball_h: float,
    pad_x: float,
    pad_y: float,
    pad_w: float,
    pad_h: float,
    vel_x: float,
    vel_y: float,
    front_face: str,
) -> tuple[float, float, float, float]:
    """Resolve orb bounce against a paddle-like collider.

    `front_face`:
    - `"right"` for paddles on the right side (player/helper).
    - `"left"` for paddles on the left side (enemy/helper).
    """
    next_x = ball_x
    next_y = ball_y
    next_vx = vel_x
    next_vy = vel_y

    if front_face == "right":
        if abs(ball_x + ball_w - pad_x) < 20:
            next_vx *= -1
            next_x = pad_x - ball_w
        elif abs(ball_y + ball_h - pad_y) < 20 and vel_y > 0:
            next_vy *= -1
            next_y = pad_y - ball_h
        elif abs(ball_y - (pad_y + pad_h)) < 20 and vel_y < 0:
            next_vy *= -1
            next_y = pad_y + pad_h
    else:
        if abs(ball_x - (pad_x + pad_w)) < 20:
            next_vx *= -1
            next_x = pad_x + pad_w
        elif abs(ball_y + ball_h - pad_y) < 20 and vel_y > 0:
            next_vy *= -1
            next_y = pad_y - ball_h
        elif abs(ball_y - (pad_y + pad_h)) < 20 and vel_y < 0:
            next_vy *= -1
            next_y = pad_y + pad_h

    return next_x, next_y, next_vx, next_vy


def apply_player_momentum_deflection(
    *, vel_x: float, vel_y: float, momentum_direction: int, momentum_enemy: float
) -> tuple[float, float]:
    """Apply legacy player-side momentum deflection rules."""
    next_vx = vel_x
    next_vy = vel_y
    if momentum_direction == 1 and vel_y > 0:
        next_vx += momentum_enemy * 2
        next_vy += momentum_enemy * 2
        next_vy *= -1
    if momentum_direction == -1 and vel_y < 0:
        next_vx += momentum_enemy * 2
        next_vy += momentum_enemy * 2
        next_vy *= -1
    return next_vx, next_vy


def apply_enemy_momentum_deflection(
    *, vel_x: float, vel_y: float, momentum_direction: int, momentum_enemy: float
) -> tuple[float, float]:
    """Apply legacy enemy-side momentum deflection rules."""
    next_vx = vel_x
    next_vy = vel_y
    if momentum_direction == -1 and vel_y > 0:
        next_vx += momentum_enemy * 2
        next_vy += momentum_enemy * 2
        next_vy *= -1
    if momentum_direction == 1 and vel_y < 0:
        next_vx += momentum_enemy * 2
        next_vy += momentum_enemy * 2
        next_vy *= -1
    return next_vx, next_vy

