from logic.helpers import patrol_vertical, track_target_center


def test_track_target_center_moves_down_when_target_below():
    new_y = track_target_center(
        y=100,
        height=20,
        target_y=200,
        target_height=20,
        speed=300,
        dt=0.5,
    )
    assert new_y == 250


def test_track_target_center_moves_up_when_target_above():
    new_y = track_target_center(
        y=200,
        height=20,
        target_y=100,
        target_height=20,
        speed=300,
        dt=0.5,
    )
    assert new_y == 50


def test_patrol_vertical_reverses_at_bottom():
    y, direction = patrol_vertical(
        y=650,
        height=100,
        min_y=150,
        max_y=720,
        speed=300,
        direction=1,
        dt=1.0,
    )
    assert y == 620
    assert direction == -1


def test_patrol_vertical_reverses_at_top():
    y, direction = patrol_vertical(
        y=160,
        height=100,
        min_y=150,
        max_y=720,
        speed=300,
        direction=-1,
        dt=1.0,
    )
    assert y == 150
    assert direction == 1

