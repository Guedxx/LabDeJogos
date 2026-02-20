"""Pure decision helpers for enemy AI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EnemyProfile:
    base_speed: float
    momentum_gain: float
    reaction_delay: float
    can_dash: bool = False
    center_when_away: bool = False
    center_speed: float = 150.0
    close_range: float = 300.0
    aggression_scaling: bool = False
    momentum_cap: float = 100.0
    min_track_y: float = 150.0
    center_line: float = 450.0
    dash_push: float = 100.0
    dash_momentum_boost: float = 5000.0
    dash_y_threshold: float = 2.0


@dataclass(frozen=True)
class PaddleSnapshot:
    y: float
    height: float


@dataclass(frozen=True)
class OrbSnapshot:
    x: float
    y: float
    width: float
    height: float
    vel_x: float


def resolve_aggression(
    *,
    base_speed: float,
    momentum_gain: float,
    aggression_scaling: bool,
    num_hits: int,
    aggression_table: Mapping[int, float],
    fallback_speed: float = 2000.0,
) -> tuple[float, float]:
    """Resolve effective speed values for enemies with hit-based aggression."""
    speed = base_speed
    gain = momentum_gain

    if aggression_scaling and aggression_table:
        clamped_hits = min(num_hits, max(aggression_table.keys()))
        speed = aggression_table.get(clamped_hits, fallback_speed)
        gain = speed

    return speed, gain


def compute_center_drift(
    *,
    profile: EnemyProfile,
    paddle: PaddleSnapshot,
    orb: OrbSnapshot,
    momentum: float,
    dt: float,
) -> float:
    """Return patrol drift when enemy should re-center while orb moves away."""
    if not profile.center_when_away or orb.vel_x <= 0:
        return 0.0

    middle = paddle.y + (paddle.height / 2)
    delta = (profile.center_speed + momentum) * dt

    if middle < profile.center_line:
        return delta
    if middle > profile.center_line:
        return -delta
    return 0.0


def compute_tracking_direction(
    *,
    profile: EnemyProfile,
    paddle: PaddleSnapshot,
    orb: OrbSnapshot,
    delay_loop: float,
    current_direction: int,
) -> tuple[int, float]:
    """Compute enemy tracking direction, respecting reaction delay constraints."""
    if delay_loop > 0:
        return current_direction, delay_loop

    if orb.vel_x >= 0:
        return current_direction, delay_loop

    close_enough = True
    if profile.center_when_away:
        close_enough = orb.x < profile.close_range
    if not close_enough:
        return current_direction, delay_loop

    paddle_mid = paddle.y + (paddle.height / 2)
    orb_mid = orb.y + (orb.height / 2)

    if paddle_mid < orb_mid:
        return -1, profile.reaction_delay
    if paddle_mid > orb_mid:
        return 1, profile.reaction_delay
    return current_direction, delay_loop


def step_enemy_movement(
    *,
    profile: EnemyProfile,
    paddle: PaddleSnapshot,
    orb: OrbSnapshot,
    direction: int,
    momentum: float,
    dt: float,
    speed: float,
    gain: float,
    dash_cooldown: float,
    dash_number: int,
    dash_cooldown_max: float,
    dash_segment_w: float,
    enemy_dash_x: float,
) -> dict[str, float | int]:
    """Compute per-frame movement and dash updates for a tracking enemy."""
    pad_dy = 0.0

    if direction == -1 and orb.vel_x < 0:
        pad_dy += (speed + momentum) * dt
        if momentum < profile.momentum_cap and paddle.y > profile.min_track_y:
            momentum += gain * dt

        if (
            profile.can_dash
            and orb.x < profile.close_range
            and (paddle.y - orb.y) > profile.dash_y_threshold
            and dash_cooldown <= 0
        ):
            pad_dy -= profile.dash_push * dt
            momentum += profile.dash_momentum_boost * dt
            enemy_dash_x -= dash_segment_w
            dash_cooldown = dash_cooldown_max
            dash_number -= 1

    elif direction == 1 and orb.vel_x < 0:
        pad_dy -= (speed + momentum) * dt
        if momentum < profile.momentum_cap and paddle.y > profile.min_track_y:
            momentum += gain * dt

    return {
        "pad_dy": pad_dy,
        "momentum": momentum,
        "dash_cooldown": dash_cooldown,
        "dash_number": dash_number,
        "enemy_dash_x": enemy_dash_x,
    }


def run_enemy_step(
    *,
    profile: EnemyProfile,
    paddle: PaddleSnapshot,
    orb: OrbSnapshot,
    momentum: float,
    direction: int,
    delay_loop: float,
    dt: float,
    num_hits: int,
    dash_cooldown: float,
    dash_number: int,
    dash_cooldown_max: float,
    dash_segment_w: float,
    enemy_dash_x: float,
    aggression_table: Mapping[int, float],
) -> dict[str, float | int]:
    """Execute one full pure AI step and return updated AI state."""
    speed, gain = resolve_aggression(
        base_speed=profile.base_speed,
        momentum_gain=profile.momentum_gain,
        aggression_scaling=profile.aggression_scaling,
        num_hits=num_hits,
        aggression_table=aggression_table,
    )

    center_drift = compute_center_drift(
        profile=profile,
        paddle=paddle,
        orb=orb,
        momentum=momentum,
        dt=dt,
    )
    if center_drift != 0:
        return {
            "direction": direction,
            "momentum": momentum,
            "delay_loop": delay_loop,
            "pad_dy": center_drift,
            "dash_cooldown": dash_cooldown,
            "dash_number": dash_number,
            "enemy_dash_x": enemy_dash_x,
        }

    direction, delay_loop = compute_tracking_direction(
        profile=profile,
        paddle=paddle,
        orb=orb,
        delay_loop=delay_loop,
        current_direction=direction,
    )

    movement = step_enemy_movement(
        profile=profile,
        paddle=paddle,
        orb=orb,
        direction=direction,
        momentum=momentum,
        dt=dt,
        speed=speed,
        gain=gain,
        dash_cooldown=dash_cooldown,
        dash_number=dash_number,
        dash_cooldown_max=dash_cooldown_max,
        dash_segment_w=dash_segment_w,
        enemy_dash_x=enemy_dash_x,
    )

    return {
        "direction": direction,
        "momentum": movement["momentum"],
        "delay_loop": delay_loop,
        "pad_dy": movement["pad_dy"],
        "dash_cooldown": movement["dash_cooldown"],
        "dash_number": movement["dash_number"],
        "enemy_dash_x": movement["enemy_dash_x"],
    }
