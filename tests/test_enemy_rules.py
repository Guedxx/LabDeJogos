from logic.enemy_rules import (
    apply_enemy_momentum_motion,
    apply_post_ai_momentum_motion,
    clamp_enemy_bounds,
    decay_enemy_momentum,
    tick_delay_react,
)


def test_decay_enemy_momentum_resets_direction_when_momentum_reaches_zero():
    outcome = decay_enemy_momentum(
        momentum=5,
        momentum_direction=1,
        decay_rate=100,
        dt=0.1,
    )
    assert outcome.momentum == 0
    assert outcome.momentum_direction == 0


def test_apply_enemy_momentum_motion_moves_by_direction():
    assert apply_enemy_momentum_motion(y=100, momentum=50, momentum_direction=1, dt=0.1) == 95
    assert apply_enemy_momentum_motion(y=100, momentum=50, momentum_direction=-1, dt=0.1) == 105


def test_clamp_enemy_bounds_clamps_top_and_bottom_and_resets_momentum():
    top_y, top_outcome = clamp_enemy_bounds(
        y=20,
        height=80,
        min_y=50,
        max_y=600,
        momentum=100,
        momentum_direction=1,
    )
    assert top_y == 50
    assert top_outcome.momentum == 0
    assert top_outcome.momentum_direction == 0

    bottom_y, bottom_outcome = clamp_enemy_bounds(
        y=590,
        height=50,
        min_y=50,
        max_y=600,
        momentum=100,
        momentum_direction=-1,
    )
    assert bottom_y == 550
    assert bottom_outcome.momentum == 0
    assert bottom_outcome.momentum_direction == 0


def test_tick_delay_react_counts_down():
    assert tick_delay_react(delay_loop=10, tick_speed=2, dt=0.5) == 9


def test_apply_post_ai_momentum_motion_moves_by_direction():
    assert apply_post_ai_momentum_motion(y=100, momentum=40, momentum_direction=1, dt=0.25) == 90
    assert apply_post_ai_momentum_motion(y=100, momentum=40, momentum_direction=-1, dt=0.25) == 110
