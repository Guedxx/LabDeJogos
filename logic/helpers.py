"""Pure movement helpers for helper paddles."""

from __future__ import annotations


def track_target_center(
    *,
    y: float,
    height: float,
    target_y: float,
    target_height: float,
    speed: float,
    dt: float,
) -> float:
    """Move vertically towards target center with fixed speed."""
    mid_self = y + (height / 2)
    mid_target = target_y + (target_height / 2)
    if mid_self < mid_target:
        return y + (speed * dt)
    if mid_self > mid_target:
        return y - (speed * dt)
    return y


def patrol_vertical(
    *,
    y: float,
    height: float,
    min_y: float,
    max_y: float,
    speed: float,
    direction: int,
    dt: float,
) -> tuple[float, int]:
    """Patrol between min/max vertical bounds."""
    next_y = y + (speed * direction * dt)
    next_direction = direction

    if next_y <= min_y:
        next_y = min_y
        next_direction = 1
    elif next_y + height >= max_y:
        next_y = max_y - height
        next_direction = -1

    return next_y, next_direction

