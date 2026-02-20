from logic.powerups import (
    resolve_powerup_collision,
    should_spawn_powerup,
    spawn_source_level,
    update_speed_powerup,
)


def test_should_spawn_regular_levels():
    assert should_spawn_powerup(level_index=2, cooldown=0, num_hits=0, roll=1)
    assert not should_spawn_powerup(level_index=2, cooldown=10, num_hits=0, roll=1)
    assert not should_spawn_powerup(level_index=2, cooldown=0, num_hits=0, roll=2)


def test_should_spawn_level_five_requires_hits():
    assert not should_spawn_powerup(level_index=5, cooldown=0, num_hits=1, roll=1)
    assert should_spawn_powerup(level_index=5, cooldown=0, num_hits=2, roll=1)


def test_spawn_source_level_mapping():
    assert spawn_source_level(0) == 0
    assert spawn_source_level(3) == 2
    assert spawn_source_level(5) == 4


def test_resolve_powerup_collision_heals_player_on_level_one():
    outcome = resolve_powerup_collision(
        level_index=1,
        lives_player=2,
        lives_enemy=3,
        vel_x=300,
        vel_y=200,
        power_up_active=False,
        power_up_activity_timer=0,
        is_frozen=False,
        freeze_timer=0,
        enemy_pad_position=(10, 20),
        max_lives=3,
        activity_base=600,
        freeze_duration=300,
    )
    assert outcome.lives_player == 3
    assert outcome.lives_enemy == 3


def test_resolve_powerup_collision_reflects_on_level_four():
    outcome = resolve_powerup_collision(
        level_index=4,
        lives_player=3,
        lives_enemy=3,
        vel_x=300,
        vel_y=200,
        power_up_active=False,
        power_up_activity_timer=0,
        is_frozen=False,
        freeze_timer=0,
        enemy_pad_position=(10, 20),
        max_lives=3,
        activity_base=600,
        freeze_duration=300,
    )
    assert outcome.vel_x < 0
    assert outcome.vel_y == -200


def test_resolve_powerup_collision_freezes_on_level_five():
    outcome = resolve_powerup_collision(
        level_index=5,
        lives_player=3,
        lives_enemy=3,
        vel_x=300,
        vel_y=200,
        power_up_active=False,
        power_up_activity_timer=0,
        is_frozen=False,
        freeze_timer=0,
        enemy_pad_position=(123, 456),
        max_lives=3,
        activity_base=600,
        freeze_duration=300,
    )
    assert outcome.is_frozen
    assert outcome.freeze_timer == 300
    assert outcome.frozen_pos == (123, 456)


def test_update_speed_powerup_expires_to_base_speed():
    active, timer, speed = update_speed_powerup(
        level_index=3,
        power_up_active=True,
        power_up_activity_timer=50,
        current_player_speed=400,
        dt=1.0,
        tick_speed=100,
        base_player_speed=200,
        boosted_player_speed=400,
    )
    assert not active
    assert timer < 0
    assert speed == 200

