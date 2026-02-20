"""Pure enemy-side motion and timing rules."""

from __future__ import annotations

from dataclasses import dataclass

from logic.physics import decay_momentum


@dataclass(frozen=True)
class EnemyMomentumOutcome:
    momentum: float
    momentum_direction: int


def decay_enemy_momentum(
    *,
    momentum: float,
    momentum_direction: int,
    decay_rate: float,
    dt: float,
) -> EnemyMomentumOutcome:
    """Decay enemy momentum and reset direction when it reaches zero."""
    next_momentum = momentum
    next_direction = momentum_direction

    if next_momentum > 0:
        next_momentum = decay_momentum(next_momentum, decay_rate, dt)
        if next_momentum <= 0:
            next_momentum = 0
            next_direction = 0

    return EnemyMomentumOutcome(momentum=next_momentum, momentum_direction=next_direction)


def apply_enemy_momentum_motion(
    *,
    y: float,
    momentum: float,
    momentum_direction: int,
    dt: float,
) -> float:
    """Apply directional momentum movement to enemy paddle before AI."""
    next_y = y
    if momentum_direction == 1:
        next_y -= momentum * dt
    elif momentum_direction == -1:
        next_y += momentum * dt
    return next_y


def clamp_enemy_bounds(
    *,
    y: float,
    height: float,
    min_y: float,
    max_y: float,
    momentum: float,
    momentum_direction: int,
) -> tuple[float, EnemyMomentumOutcome]:
    """Clamp enemy paddle and reset momentum when touching bounds."""
    next_y = y
    next_momentum = momentum
    next_direction = momentum_direction

    if next_y < min_y:
        next_y = min_y
        next_momentum = 0
        next_direction = 0
    if next_y + height > max_y:
        next_y = max_y - height
        next_momentum = 0
        next_direction = 0

    return next_y, EnemyMomentumOutcome(momentum=next_momentum, momentum_direction=next_direction)


def tick_delay_react(delay_loop: float, tick_speed: float, dt: float) -> float:
    """Advance reaction-delay timer."""
    return delay_loop - (tick_speed * dt)


def apply_post_ai_momentum_motion(
    *,
    y: float,
    momentum: float,
    momentum_direction: int,
    dt: float,
) -> float:
    """Apply directional momentum movement after AI updates direction."""
    next_y = y
    if momentum_direction == 1:
        next_y -= momentum * dt
    elif momentum_direction == -1:
        next_y += momentum * dt
    return next_y

