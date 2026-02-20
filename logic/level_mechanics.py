"""Pure level-specific mechanic rules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RonaldinhoOutcome:
    vel_x: float
    vel_y: float
    triggered: bool


@dataclass(frozen=True)
class BulkOutcome:
    is_holding: bool
    hold_timer: float
    thrown: bool
    is_slow: bool
    slow_timer: float
    bulk_throw_dir: int
    momentum_dir_enemy: int
    momentum_player: float
    vel_player: float
    vel_x: float
    vel_y: float
    ball_x: float
    ball_y: float


@dataclass(frozen=True)
class FreezeOutcome:
    is_frozen: bool
    freeze_timer: float
    enemy_pad_x: float
    enemy_pad_y: float


def apply_ronaldinho_ole(
    *,
    level_index: int,
    has_ole: bool,
    vel_x: float,
    vel_y: float,
    roll: int,
    trigger_roll: int,
    vel_y_multiplier: float,
    vel_x_multiplier: float,
) -> RonaldinhoOutcome:
    """Apply Ronaldinho random deflection when trigger condition is met."""
    next_vx = vel_x
    next_vy = vel_y
    triggered = False

    if level_index == 3 and has_ole and roll == trigger_roll and vel_x > 0:
        triggered = True
        next_vy *= vel_y_multiplier
        next_vx *= vel_x_multiplier

    return RonaldinhoOutcome(vel_x=next_vx, vel_y=next_vy, triggered=triggered)


def update_bulk_hold_mechanic(
    *,
    level_index: int,
    has_hold: bool,
    enemy_ball_collided: bool,
    player_ball_collided: bool,
    hold_roll: int,
    hold_trigger_roll: int,
    throw_direction_roll: int,
    is_holding: bool,
    hold_timer: float,
    thrown: bool,
    is_slow: bool,
    slow_timer: float,
    bulk_throw_dir: int,
    momentum_dir_enemy: int,
    momentum_player: float,
    vel_player: float,
    vel_x: float,
    vel_y: float,
    ball_x: float,
    ball_y: float,
    ball_h: float,
    enemy_pad_x: float,
    enemy_pad_y: float,
    enemy_pad_h: float,
    dt: float,
    hold_duration: float,
    slow_duration: float,
    tick_speed: float,
    slow_player_speed: float,
    base_player_speed: float,
) -> BulkOutcome:
    """Update Bulk hold/throw/slow state machine."""
    next_is_holding = is_holding
    next_hold_timer = hold_timer
    next_thrown = thrown
    next_is_slow = is_slow
    next_slow_timer = slow_timer
    next_bulk_throw_dir = bulk_throw_dir
    next_momentum_dir_enemy = momentum_dir_enemy
    next_momentum_player = momentum_player
    next_vel_player = vel_player
    next_vel_x = vel_x
    next_vel_y = vel_y
    next_ball_x = ball_x
    next_ball_y = ball_y

    if level_index != 4 or not has_hold:
        return BulkOutcome(
            is_holding=next_is_holding,
            hold_timer=next_hold_timer,
            thrown=next_thrown,
            is_slow=next_is_slow,
            slow_timer=next_slow_timer,
            bulk_throw_dir=next_bulk_throw_dir,
            momentum_dir_enemy=next_momentum_dir_enemy,
            momentum_player=next_momentum_player,
            vel_player=next_vel_player,
            vel_x=next_vel_x,
            vel_y=next_vel_y,
            ball_x=next_ball_x,
            ball_y=next_ball_y,
        )

    if enemy_ball_collided and hold_roll == hold_trigger_roll:
        if not next_is_holding:
            next_hold_timer = hold_duration
        next_is_holding = True
        next_bulk_throw_dir = throw_direction_roll
        next_thrown = True

    if next_is_holding:
        next_momentum_dir_enemy = 0
        next_ball_x = enemy_pad_x + 50
        next_ball_y = (enemy_pad_y + enemy_pad_h / 2) - (ball_h / 2)
        next_vel_x -= 100 * dt
        next_vel_y *= next_bulk_throw_dir

        next_hold_timer -= tick_speed * dt
        if next_hold_timer <= 0:
            next_is_holding = False

    if next_thrown and player_ball_collided:
        next_vel_x /= 1.3
        next_vel_y /= 1.3
        next_thrown = False
        next_is_slow = True
        next_slow_timer = slow_duration

    if next_is_slow:
        next_slow_timer -= tick_speed * dt
        next_vel_player = slow_player_speed
        next_momentum_player = 0
        if next_slow_timer <= 0:
            next_is_slow = False
            next_vel_player = base_player_speed

    return BulkOutcome(
        is_holding=next_is_holding,
        hold_timer=next_hold_timer,
        thrown=next_thrown,
        is_slow=next_is_slow,
        slow_timer=next_slow_timer,
        bulk_throw_dir=next_bulk_throw_dir,
        momentum_dir_enemy=next_momentum_dir_enemy,
        momentum_player=next_momentum_player,
        vel_player=next_vel_player,
        vel_x=next_vel_x,
        vel_y=next_vel_y,
        ball_x=next_ball_x,
        ball_y=next_ball_y,
    )


def update_king_pong_freeze(
    *,
    level_index: int,
    num_hits: int,
    is_frozen: bool,
    freeze_timer: float,
    enemy_pad_x: float,
    enemy_pad_y: float,
    frozen_pos: tuple[float, float],
    dt: float,
    tick_speed: float,
) -> FreezeOutcome:
    """Update King Pong freeze lock."""
    next_is_frozen = is_frozen
    next_timer = freeze_timer
    next_x = enemy_pad_x
    next_y = enemy_pad_y

    if level_index == 5 and num_hits == 2 and next_is_frozen:
        next_x = frozen_pos[0]
        next_y = frozen_pos[1]
        next_timer -= tick_speed * dt
        if next_timer <= 0:
            next_is_frozen = False

    return FreezeOutcome(
        is_frozen=next_is_frozen,
        freeze_timer=next_timer,
        enemy_pad_x=next_x,
        enemy_pad_y=next_y,
    )

