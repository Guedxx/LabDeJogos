from logic.ai_core import (
    EnemyProfile,
    OrbSnapshot,
    PaddleSnapshot,
    compute_tracking_direction,
    resolve_aggression,
    run_enemy_step,
    step_enemy_movement,
)


def _profile(**kwargs):
    return EnemyProfile(base_speed=210, momentum_gain=100, reaction_delay=50, **kwargs)


def test_resolve_aggression_scaling():
    speed, gain = resolve_aggression(
        base_speed=100,
        momentum_gain=100,
        aggression_scaling=True,
        num_hits=2,
        aggression_table={0: 100, 1: 200, 2: 400, 3: 2000},
    )
    assert speed == 400
    assert gain == 400


def test_compute_tracking_direction_respects_delay():
    direction, delay = compute_tracking_direction(
        profile=_profile(),
        paddle=PaddleSnapshot(y=200, height=100),
        orb=OrbSnapshot(x=100, y=50, width=10, height=10, vel_x=-300),
        delay_loop=10,
        current_direction=1,
    )
    assert direction == 1
    assert delay == 10


def test_compute_tracking_direction_tracks_orb_center():
    direction, delay = compute_tracking_direction(
        profile=_profile(),
        paddle=PaddleSnapshot(y=200, height=100),
        orb=OrbSnapshot(x=100, y=400, width=10, height=10, vel_x=-300),
        delay_loop=0,
        current_direction=0,
    )
    assert direction == -1
    assert delay == 50


def test_step_enemy_movement_updates_position_and_momentum():
    result = step_enemy_movement(
        profile=_profile(),
        paddle=PaddleSnapshot(y=200, height=100),
        orb=OrbSnapshot(x=100, y=400, width=10, height=10, vel_x=-200),
        direction=-1,
        momentum=0,
        dt=0.5,
        speed=210,
        gain=100,
        dash_cooldown=30,
        dash_number=3,
        dash_cooldown_max=30,
        dash_segment_w=80,
        enemy_dash_x=160,
    )
    assert result["pad_dy"] > 0
    assert result["momentum"] > 0


def test_run_enemy_step_returns_center_drift_when_orb_moves_away():
    profile = _profile(center_when_away=True)
    result = run_enemy_step(
        profile=profile,
        paddle=PaddleSnapshot(y=150, height=100),
        orb=OrbSnapshot(x=500, y=300, width=10, height=10, vel_x=300),
        momentum=10,
        direction=0,
        delay_loop=0,
        dt=1.0,
        num_hits=0,
        dash_cooldown=0,
        dash_number=3,
        dash_cooldown_max=30,
        dash_segment_w=80,
        enemy_dash_x=160,
        aggression_table={0: 100, 1: 200, 2: 400, 3: 2000},
    )
    assert result["pad_dy"] > 0
    assert result["direction"] == 0

