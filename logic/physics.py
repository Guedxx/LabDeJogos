"""Pure math helpers for gameplay movement and momentum."""

from __future__ import annotations


def apply_speed_soft_limit(value: float, max_abs: float, decay: float, dt: float) -> float:
    """Apply a soft clamp when speed exceeds the absolute cap."""
    if value > max_abs:
        return value - (decay * dt)
    if value < -max_abs:
        return value + (decay * dt)
    return value


def accelerate_towards_cap(value: float, cap: float, acceleration: float, dt: float) -> float:
    """Accelerate while preserving sign until the given cruise cap."""
    if 0 < value < cap:
        return min(cap, value + (acceleration * dt))
    if -cap < value < 0:
        return max(-cap, value - (acceleration * dt))
    return value


def decay_momentum(momentum: float, decay_rate: float, dt: float) -> float:
    """Decay momentum, never returning negative values."""
    if momentum <= 0:
        return 0.0
    return max(0.0, momentum - (decay_rate * dt))

