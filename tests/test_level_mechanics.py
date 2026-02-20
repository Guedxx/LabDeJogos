from logic.level_mechanics import (
    apply_ronaldinho_ole,
    update_bulk_hold_mechanic,
    update_king_pong_freeze,
)


def test_apply_ronaldinho_ole_triggers_only_when_conditions_match():
    triggered = apply_ronaldinho_ole(
        level_index=3,
        has_ole=True,
        vel_x=300,
        vel_y=200,
        roll=4,
        trigger_roll=4,
        vel_y_multiplier=1.2,
        vel_x_multiplier=1.3,
    )
    assert triggered.triggered
    assert triggered.vel_x == 390
    assert triggered.vel_y == 240

    not_triggered = apply_ronaldinho_ole(
        level_index=3,
        has_ole=True,
        vel_x=-300,
        vel_y=200,
        roll=4,
        trigger_roll=4,
        vel_y_multiplier=1.2,
        vel_x_multiplier=1.3,
    )
    assert not not_triggered.triggered
    assert not_triggered.vel_x == -300
    assert not_triggered.vel_y == 200


def test_update_bulk_hold_mechanic_noop_when_feature_disabled():
    outcome = update_bulk_hold_mechanic(
        level_index=4,
        has_hold=False,
        enemy_ball_collided=True,
        player_ball_collided=True,
        hold_roll=1,
        hold_trigger_roll=1,
        throw_direction_roll=-1,
        is_holding=False,
        hold_timer=300,
        thrown=False,
        is_slow=False,
        slow_timer=300,
        bulk_throw_dir=1,
        momentum_dir_enemy=1,
        momentum_player=25,
        vel_player=200,
        vel_x=300,
        vel_y=200,
        ball_x=400,
        ball_y=300,
        ball_h=20,
        enemy_pad_x=50,
        enemy_pad_y=150,
        enemy_pad_h=120,
        dt=1.0,
        hold_duration=300,
        slow_duration=300,
        tick_speed=100,
        slow_player_speed=120,
        base_player_speed=200,
    )
    assert not outcome.is_holding
    assert not outcome.thrown
    assert not outcome.is_slow
    assert outcome.vel_player == 200
    assert outcome.ball_x == 400
    assert outcome.ball_y == 300


def test_update_bulk_hold_mechanic_enters_hold_and_repositions_ball():
    outcome = update_bulk_hold_mechanic(
        level_index=4,
        has_hold=True,
        enemy_ball_collided=True,
        player_ball_collided=False,
        hold_roll=1,
        hold_trigger_roll=1,
        throw_direction_roll=-1,
        is_holding=False,
        hold_timer=300,
        thrown=False,
        is_slow=False,
        slow_timer=300,
        bulk_throw_dir=1,
        momentum_dir_enemy=1,
        momentum_player=25,
        vel_player=200,
        vel_x=300,
        vel_y=200,
        ball_x=400,
        ball_y=300,
        ball_h=20,
        enemy_pad_x=50,
        enemy_pad_y=150,
        enemy_pad_h=120,
        dt=1.0,
        hold_duration=300,
        slow_duration=300,
        tick_speed=100,
        slow_player_speed=120,
        base_player_speed=200,
    )
    assert outcome.is_holding
    assert outcome.thrown
    assert outcome.bulk_throw_dir == -1
    assert outcome.momentum_dir_enemy == 0
    assert outcome.hold_timer == 200
    assert outcome.ball_x == 100
    assert outcome.ball_y == 200
    assert outcome.vel_x == 200
    assert outcome.vel_y == -200


def test_update_bulk_hold_mechanic_thrown_hit_applies_slow():
    outcome = update_bulk_hold_mechanic(
        level_index=4,
        has_hold=True,
        enemy_ball_collided=False,
        player_ball_collided=True,
        hold_roll=0,
        hold_trigger_roll=1,
        throw_direction_roll=1,
        is_holding=False,
        hold_timer=200,
        thrown=True,
        is_slow=False,
        slow_timer=0,
        bulk_throw_dir=1,
        momentum_dir_enemy=0,
        momentum_player=40,
        vel_player=200,
        vel_x=260,
        vel_y=130,
        ball_x=400,
        ball_y=300,
        ball_h=20,
        enemy_pad_x=50,
        enemy_pad_y=150,
        enemy_pad_h=120,
        dt=1.0,
        hold_duration=300,
        slow_duration=300,
        tick_speed=100,
        slow_player_speed=120,
        base_player_speed=200,
    )
    assert not outcome.thrown
    assert outcome.is_slow
    assert outcome.slow_timer == 200
    assert outcome.momentum_player == 0
    assert outcome.vel_player == 120
    assert outcome.vel_x == 200
    assert outcome.vel_y == 100


def test_update_bulk_hold_mechanic_slow_expiry_restores_player_speed():
    outcome = update_bulk_hold_mechanic(
        level_index=4,
        has_hold=True,
        enemy_ball_collided=False,
        player_ball_collided=False,
        hold_roll=0,
        hold_trigger_roll=1,
        throw_direction_roll=1,
        is_holding=False,
        hold_timer=200,
        thrown=False,
        is_slow=True,
        slow_timer=50,
        bulk_throw_dir=1,
        momentum_dir_enemy=0,
        momentum_player=40,
        vel_player=120,
        vel_x=260,
        vel_y=130,
        ball_x=400,
        ball_y=300,
        ball_h=20,
        enemy_pad_x=50,
        enemy_pad_y=150,
        enemy_pad_h=120,
        dt=1.0,
        hold_duration=300,
        slow_duration=300,
        tick_speed=100,
        slow_player_speed=120,
        base_player_speed=200,
    )
    assert not outcome.is_slow
    assert outcome.vel_player == 200
    assert outcome.momentum_player == 0


def test_update_king_pong_freeze_holds_position_then_unfreezes():
    active = update_king_pong_freeze(
        level_index=5,
        num_hits=2,
        is_frozen=True,
        freeze_timer=120,
        enemy_pad_x=10,
        enemy_pad_y=20,
        frozen_pos=(123, 456),
        dt=1.0,
        tick_speed=100,
    )
    assert active.is_frozen
    assert active.freeze_timer == 20
    assert active.enemy_pad_x == 123
    assert active.enemy_pad_y == 456

    expired = update_king_pong_freeze(
        level_index=5,
        num_hits=2,
        is_frozen=True,
        freeze_timer=50,
        enemy_pad_x=10,
        enemy_pad_y=20,
        frozen_pos=(123, 456),
        dt=1.0,
        tick_speed=100,
    )
    assert not expired.is_frozen
    assert expired.freeze_timer == -50
