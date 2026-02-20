from logic.collisions import (
    apply_enemy_momentum_deflection,
    apply_player_momentum_deflection,
    resolve_paddle_bounce,
)


def test_resolve_paddle_bounce_front_face_right():
    x, y, vx, vy = resolve_paddle_bounce(
        ball_x=90,
        ball_y=200,
        ball_w=10,
        ball_h=10,
        pad_x=100,
        pad_y=180,
        pad_w=20,
        pad_h=80,
        vel_x=300,
        vel_y=0,
        front_face="right",
    )
    assert vx == -300
    assert x == 90
    assert y == 200
    assert vy == 0


def test_resolve_paddle_bounce_front_face_left():
    x, y, vx, vy = resolve_paddle_bounce(
        ball_x=120,
        ball_y=200,
        ball_w=10,
        ball_h=10,
        pad_x=100,
        pad_y=180,
        pad_w=20,
        pad_h=80,
        vel_x=-300,
        vel_y=0,
        front_face="left",
    )
    assert vx == 300
    assert x == 120
    assert y == 200
    assert vy == 0


def test_player_momentum_deflection_flips_vertical():
    vx, vy = apply_player_momentum_deflection(
        vel_x=100,
        vel_y=10,
        momentum_direction=1,
        momentum_enemy=5,
    )
    assert vx == 110
    assert vy == -20


def test_enemy_momentum_deflection_flips_vertical():
    vx, vy = apply_enemy_momentum_deflection(
        vel_x=100,
        vel_y=-10,
        momentum_direction=1,
        momentum_enemy=5,
    )
    assert vx == 110
    assert vy == 0
