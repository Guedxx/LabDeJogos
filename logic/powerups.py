"""Pure power-up rule helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PowerUpHitOutcome:
    lives_player: int
    lives_enemy: int
    vel_x: float
    vel_y: float
    power_up_active: bool
    power_up_activity_timer: float
    is_frozen: bool
    freeze_timer: float
    frozen_pos: tuple[float, float]


def should_spawn_powerup(*, level_index: int, cooldown: float, num_hits: int, roll: int, trigger_roll: int = 1) -> bool:
    """Return whether a spawn should happen this frame."""
    if roll != trigger_roll or cooldown > 0:
        return False
    if level_index == 5:
        return num_hits >= 2
    return True


def spawn_source_level(level_index: int) -> int:
    """Return source level used to choose the spawned power-up sprite."""
    if level_index == 5:
        return 4
    if level_index == 0:
        return 0
    return level_index - 1


def resolve_powerup_collision(
    *,
    level_index: int,
    lives_player: int,
    lives_enemy: int,
    vel_x: float,
    vel_y: float,
    power_up_active: bool,
    power_up_activity_timer: float,
    is_frozen: bool,
    freeze_timer: float,
    enemy_pad_position: tuple[float, float],
    max_lives: int,
    activity_base: float,
    freeze_duration: float,
) -> PowerUpHitOutcome:
    """Resolve state updates when a power-up is collected."""
    next_lives_player = lives_player
    next_lives_enemy = lives_enemy
    next_vel_x = vel_x
    next_vel_y = vel_y
    next_power_up_active = power_up_active
    next_activity_timer = power_up_activity_timer
    next_is_frozen = is_frozen
    next_freeze_timer = freeze_timer
    next_frozen_pos = enemy_pad_position

    if level_index == 0:
        if next_lives_enemy < max_lives:
            next_lives_enemy += 1

    elif level_index >= 1:
        if level_index == 1:
            if next_lives_player < max_lives:
                next_lives_player += 1
        elif level_index == 2:
            next_power_up_active = True
            next_activity_timer = activity_base
        elif level_index == 3:
            next_power_up_active = True
            next_activity_timer = activity_base
        elif level_index == 4:
            next_vel_y *= -1
            if next_vel_x > 0:
                next_vel_x *= -1
        elif level_index == 5:
            next_is_frozen = True
            next_freeze_timer = freeze_duration
            next_frozen_pos = enemy_pad_position

    return PowerUpHitOutcome(
        lives_player=next_lives_player,
        lives_enemy=next_lives_enemy,
        vel_x=next_vel_x,
        vel_y=next_vel_y,
        power_up_active=next_power_up_active,
        power_up_activity_timer=next_activity_timer,
        is_frozen=next_is_frozen,
        freeze_timer=next_freeze_timer,
        frozen_pos=next_frozen_pos,
    )


def update_speed_powerup(
    *,
    level_index: int,
    power_up_active: bool,
    power_up_activity_timer: float,
    current_player_speed: float,
    dt: float,
    tick_speed: float,
    base_player_speed: float,
    boosted_player_speed: float = 400.0,
) -> tuple[bool, float, float]:
    """Tick Ronaldinho level speed power-up and return updated state."""
    if not power_up_active or level_index != 3:
        return power_up_active, power_up_activity_timer, current_player_speed

    next_timer = power_up_activity_timer - (tick_speed * dt)
    if next_timer <= 0:
        return False, next_timer, base_player_speed
    return True, next_timer, boosted_player_speed

