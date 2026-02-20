from logic.player_rules import (
    apply_player_input,
    apply_player_momentum_motion,
    clamp_player_bounds,
    decay_player_momentum,
    update_player_dash_state,
)


def test_update_player_dash_state_reloads_dash_when_timer_reaches_zero():
    outcome = update_player_dash_state(
        dash_cooldown=5,
        dash_reload=1,
        dash_number=1,
        first_dash=True,
        max_dashes=3,
        dash_reload_max=100,
    )
    assert outcome.dash_cooldown == 4
    assert outcome.dash_reload == 100
    assert outcome.dash_number == 2
    assert outcome.first_dash


def test_update_player_dash_state_disables_first_dash_flag_at_max_dashes():
    outcome = update_player_dash_state(
        dash_cooldown=5,
        dash_reload=20,
        dash_number=3,
        first_dash=True,
        max_dashes=3,
        dash_reload_max=100,
    )
    assert outcome.dash_cooldown == 4
    assert outcome.dash_reload == 19
    assert outcome.dash_number == 3
    assert not outcome.first_dash


def test_decay_player_momentum_zeroes_small_momentum_and_resets_direction():
    outcome = decay_player_momentum(
        momentum=0.2,
        momentum_direction=1,
        decay_rate=2.0,
        dt=0.1,
    )
    assert outcome.momentum == 0
    assert outcome.momentum_direction == 0


def test_apply_player_momentum_motion_moves_up_or_down_by_direction():
    assert apply_player_momentum_motion(y=100, momentum=50, momentum_direction=1, dt=0.1) == 95
    assert apply_player_momentum_motion(y=100, momentum=50, momentum_direction=-1, dt=0.1) == 105


def test_apply_player_input_with_up_dash_updates_position_momentum_and_dash_state():
    outcome = apply_player_input(
        y=200,
        height=100,
        char_h=50,
        screen_h=600,
        vel_player=200,
        momentum=0,
        momentum_direction=0,
        press_w=True,
        press_s=False,
        press_space=True,
        dash_cooldown=-1,
        dash_number=2,
        first_dash=False,
        momentum_cap=1000,
        momentum_gain=10,
        dash_move_boost_up=300,
        dash_move_boost_down=300,
        dash_momentum_boost=600,
        dash_cooldown_reset=50,
        dt=0.1,
    )
    assert outcome.y == 150
    assert outcome.momentum == 61
    assert outcome.momentum_direction == 1
    assert outcome.dash_cooldown == 50
    assert outcome.dash_number == 1
    assert outcome.first_dash


def test_apply_player_input_without_dash_still_accumulates_directional_momentum():
    outcome = apply_player_input(
        y=200,
        height=100,
        char_h=50,
        screen_h=600,
        vel_player=200,
        momentum=0,
        momentum_direction=0,
        press_w=False,
        press_s=True,
        press_space=False,
        dash_cooldown=20,
        dash_number=2,
        first_dash=False,
        momentum_cap=1000,
        momentum_gain=10,
        dash_move_boost_up=300,
        dash_move_boost_down=300,
        dash_momentum_boost=600,
        dash_cooldown_reset=50,
        dt=0.1,
    )
    assert outcome.y == 220
    assert outcome.momentum == 1
    assert outcome.momentum_direction == -1
    assert outcome.dash_cooldown == 20
    assert outcome.dash_number == 2
    assert not outcome.first_dash


def test_clamp_player_bounds_keeps_paddle_inside_top_and_bottom_edges():
    top_outcome, top_y = clamp_player_bounds(
        y=10,
        height=100,
        char_h=50,
        screen_h=600,
        momentum=20,
        momentum_direction=1,
        momentum_cap=100,
        dt=0.5,
    )
    assert top_y == 50
    assert top_outcome.momentum_direction == -1
    assert top_outcome.momentum == 30

    bottom_outcome, bottom_y = clamp_player_bounds(
        y=550,
        height=100,
        char_h=50,
        screen_h=600,
        momentum=20,
        momentum_direction=-1,
        momentum_cap=100,
        dt=0.5,
    )
    assert bottom_y == 500
    assert bottom_outcome.momentum_direction == 1
    assert bottom_outcome.momentum == 30
