"""Pure player movement and dash rules."""

from __future__ import annotations

from dataclasses import dataclass

from logic.physics import decay_momentum


@dataclass(frozen=True)
class PlayerDashOutcome:
    dash_cooldown: float
    dash_reload: float
    dash_number: int
    first_dash: bool


@dataclass(frozen=True)
class PlayerMomentumOutcome:
    momentum: float
    momentum_direction: int


@dataclass(frozen=True)
class PlayerInputOutcome:
    y: float
    momentum: float
    momentum_direction: int
    dash_cooldown: float
    dash_number: int
    first_dash: bool


def update_player_dash_state(
    *,
    dash_cooldown: float,
    dash_reload: float,
    dash_number: int,
    first_dash: bool,
    max_dashes: int,
    dash_reload_max: float,
) -> PlayerDashOutcome:
    """Update player dash counters with legacy frame semantics."""
    next_cooldown = dash_cooldown - 1
    next_reload = dash_reload
    next_dash_number = dash_number
    next_first_dash = first_dash

    if next_first_dash:
        next_reload -= 1
    if next_dash_number >= max_dashes:
        next_first_dash = False
    if next_reload <= 0 and next_dash_number < max_dashes:
        next_dash_number += 1
        next_reload = dash_reload_max

    return PlayerDashOutcome(
        dash_cooldown=next_cooldown,
        dash_reload=next_reload,
        dash_number=next_dash_number,
        first_dash=next_first_dash,
    )


def decay_player_momentum(
    *,
    momentum: float,
    momentum_direction: int,
    decay_rate: float,
    dt: float,
) -> PlayerMomentumOutcome:
    """Decay player momentum and reset direction when momentum reaches zero."""
    next_momentum = momentum
    next_direction = momentum_direction
    if next_momentum > 0:
        next_momentum = decay_momentum(next_momentum, decay_rate, dt)
        if next_momentum < 1 * dt:
            next_momentum = 0
            next_direction = 0
    return PlayerMomentumOutcome(momentum=next_momentum, momentum_direction=next_direction)


def apply_player_momentum_motion(
    *,
    y: float,
    momentum: float,
    momentum_direction: int,
    dt: float,
) -> float:
    """Apply current directional momentum to player paddle y."""
    next_y = y
    if momentum_direction == 1:
        next_y -= momentum * dt
    elif momentum_direction == -1:
        next_y += momentum * dt
    return next_y


def apply_player_input(
    *,
    y: float,
    height: float,
    char_h: float,
    screen_h: float,
    vel_player: float,
    momentum: float,
    momentum_direction: int,
    press_w: bool,
    press_s: bool,
    press_space: bool,
    dash_cooldown: float,
    dash_number: int,
    first_dash: bool,
    momentum_cap: float,
    momentum_gain: float,
    dash_move_boost_up: float,
    dash_move_boost_down: float,
    dash_momentum_boost: float,
    dash_cooldown_reset: float,
    dt: float,
) -> PlayerInputOutcome:
    """Apply immediate key input effects for the current frame."""
    next_y = y
    next_momentum = momentum
    next_direction = momentum_direction
    next_cooldown = dash_cooldown
    next_dash_number = dash_number
    next_first_dash = first_dash

    if press_w:
        next_y -= (vel_player * dt) + (next_momentum * dt)
        if next_momentum < momentum_cap and next_y > char_h:
            next_momentum += momentum_gain * dt
        next_direction = 1

        if press_space and next_cooldown < 0 and next_dash_number > 0:
            next_first_dash = True
            next_y -= dash_move_boost_up * dt
            next_momentum += dash_momentum_boost * dt
            next_cooldown = dash_cooldown_reset
            next_dash_number -= 1

    elif press_s:
        next_y += (vel_player * dt) + (next_momentum * dt)
        if next_momentum < momentum_cap and next_y + height < screen_h:
            next_momentum += momentum_gain * dt
        next_direction = -1

        if press_space and next_cooldown < 0 and next_dash_number > 0:
            next_first_dash = True
            next_y += dash_move_boost_down * dt
            next_momentum += dash_momentum_boost * dt
            next_cooldown = dash_cooldown_reset
            next_dash_number -= 1

    return PlayerInputOutcome(
        y=next_y,
        momentum=next_momentum,
        momentum_direction=next_direction,
        dash_cooldown=next_cooldown,
        dash_number=next_dash_number,
        first_dash=next_first_dash,
    )


def clamp_player_bounds(
    *,
    y: float,
    height: float,
    char_h: float,
    screen_h: float,
    momentum: float,
    momentum_direction: int,
    momentum_cap: float,
    dt: float,
) -> tuple[PlayerMomentumOutcome, float]:
    """Clamp player paddle vertically and keep legacy momentum side-effects."""
    next_y = y
    next_momentum = momentum
    next_direction = momentum_direction

    if next_y < char_h:
        next_y = char_h
        next_direction = -1
        if next_momentum < momentum_cap:
            next_momentum += next_momentum * dt
    elif next_y + height > screen_h:
        next_y = screen_h - height
        next_direction = 1
        if next_momentum < momentum_cap:
            next_momentum += next_momentum * dt

    return PlayerMomentumOutcome(momentum=next_momentum, momentum_direction=next_direction), next_y
