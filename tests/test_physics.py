from logic.physics import accelerate_towards_cap, apply_speed_soft_limit, decay_momentum


def test_apply_speed_soft_limit_above_cap():
    assert apply_speed_soft_limit(1200, 1000, 10, 1.0) == 1190


def test_apply_speed_soft_limit_within_cap():
    assert apply_speed_soft_limit(300, 1000, 10, 1.0) == 300


def test_accelerate_towards_cap_positive_and_negative():
    assert accelerate_towards_cap(300, 550, 10, 1.0) == 310
    assert accelerate_towards_cap(-300, 550, 10, 1.0) == -310


def test_decay_momentum_never_negative():
    assert decay_momentum(1.0, 75.0, 0.1) == 0.0
    assert decay_momentum(100.0, 75.0, 0.1) == 92.5

