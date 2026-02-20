from logic.ball_rules import accelerate_ball, clamp_ball_speed_framewise, resolve_wall_and_scoring


def test_clamp_ball_speed_framewise_limits_positive_and_negative_speed():
    assert clamp_ball_speed_framewise(1200, 1000, 10) == 1190
    assert clamp_ball_speed_framewise(-1200, 1000, 10) == -1190


def test_accelerate_ball_preserves_sign_and_accelerates_toward_cap():
    next_vx, next_vy = accelerate_ball(
        vel_x=300,
        vel_y=-300,
        cruise_cap=550,
        accel_x=10,
        accel_y=20,
        dt=1.0,
    )
    assert next_vx == 310
    assert next_vy == -320


def test_resolve_wall_and_scoring_right_wall_costs_player_life():
    outcome = resolve_wall_and_scoring(
        ball_x=791,
        ball_y=200,
        ball_w=10,
        ball_h=10,
        vel_x=300,
        vel_y=200,
        lives_player=3,
        lives_enemy=3,
        num_hits=0,
        level_index=2,
        screen_w=800,
        screen_h=600,
        char_h=50,
    )
    assert outcome.ball_x == 788
    assert outcome.lives_player == 2
    assert outcome.vel_x == -150
    assert outcome.vel_y == 100
    assert outcome.transition_target is None
    assert outcome.sounds == ("hit_sound.ogg",)


def test_resolve_wall_and_scoring_left_wall_triggers_level_clear():
    outcome = resolve_wall_and_scoring(
        ball_x=-1,
        ball_y=200,
        ball_w=10,
        ball_h=10,
        vel_x=300,
        vel_y=200,
        lives_player=3,
        lives_enemy=1,
        num_hits=4,
        level_index=2,
        screen_w=800,
        screen_h=600,
        char_h=50,
    )
    assert outcome.lives_enemy == 0
    assert outcome.num_hits == 5
    assert outcome.transition_target == "level_clear"
    assert outcome.transition_level == 2
    assert outcome.sounds == ("hit_sound.ogg",)


def test_resolve_wall_and_scoring_left_wall_triggers_credits_on_final_level():
    outcome = resolve_wall_and_scoring(
        ball_x=-1,
        ball_y=200,
        ball_w=10,
        ball_h=10,
        vel_x=300,
        vel_y=200,
        lives_player=3,
        lives_enemy=0,
        num_hits=4,
        level_index=5,
        screen_w=800,
        screen_h=600,
        char_h=50,
    )
    assert outcome.lives_enemy == -1
    assert outcome.transition_target == "credits"
    assert outcome.transition_level is None
    assert outcome.sounds == ("hit_sound.ogg",)


def test_resolve_wall_and_scoring_top_and_bottom_walls_reflect_vertical_velocity():
    bottom = resolve_wall_and_scoring(
        ball_x=100,
        ball_y=390,
        ball_w=10,
        ball_h=10,
        vel_x=300,
        vel_y=250,
        lives_player=3,
        lives_enemy=3,
        num_hits=0,
        level_index=2,
        screen_w=800,
        screen_h=400,
        char_h=50,
    )
    assert bottom.ball_y == 390
    assert bottom.vel_y == -250
    assert bottom.sounds == ("wall_sound.ogg",)

    top = resolve_wall_and_scoring(
        ball_x=100,
        ball_y=20,
        ball_w=10,
        ball_h=10,
        vel_x=300,
        vel_y=-220,
        lives_player=3,
        lives_enemy=3,
        num_hits=0,
        level_index=2,
        screen_w=800,
        screen_h=400,
        char_h=50,
    )
    assert top.ball_y == 50
    assert top.vel_y == 220
    assert top.sounds == ("wall_sound.ogg",)
