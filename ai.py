"""Enemy AI adapter built on top of pure logic helpers."""

from __future__ import annotations

from collections.abc import Mapping

from logic.ai_core import EnemyProfile, OrbSnapshot, PaddleSnapshot, run_enemy_step
from settings import KING_PONG_AGGRESSION


class EnemyAI:
    """Configurable enemy AI that delegates decisions to pure helpers."""

    def __init__(
        self,
        base_speed: float = 210,
        momentum_gain: float = 100,
        reaction_delay: float = 200,
        can_dash: bool = False,
        center_when_away: bool = False,
        center_speed: float = 150,
        close_range: float = 300,
        aggression_scaling: bool = False,
        aggression_table: Mapping[int, float] | None = None,
    ):
        self.profile = EnemyProfile(
            base_speed=base_speed,
            momentum_gain=momentum_gain,
            reaction_delay=reaction_delay,
            can_dash=can_dash,
            center_when_away=center_when_away,
            center_speed=center_speed,
            close_range=close_range,
            aggression_scaling=aggression_scaling,
        )
        self.aggression_table: Mapping[int, float] = (
            aggression_table if aggression_table is not None else KING_PONG_AGGRESSION
        )

    def update(
        self,
        pad_y: float,
        pad_h: float,
        ball_y: float,
        ball_h: float,
        ball_x: float,
        vel_x: float,
        dt: float,
        momentum: float,
        direction: int,
        delay_loop: float,
        num_hits: int = 0,
        # Dash state (only used by Ronaldinho)
        dash_cooldown: float = 0,
        dash_number: int = 3,
        dash_cooldown_max: float = 30,
        dash_segment_w: float = 80,
        enemy_dash_x: float = 0,
    ) -> dict[str, float | int]:
        """Run one AI tick."""
        paddle = PaddleSnapshot(y=pad_y, height=pad_h)
        orb = OrbSnapshot(x=ball_x, y=ball_y, width=0, height=ball_h, vel_x=vel_x)
        return run_enemy_step(
            profile=self.profile,
            paddle=paddle,
            orb=orb,
            momentum=momentum,
            direction=direction,
            delay_loop=delay_loop,
            dt=dt,
            num_hits=num_hits,
            dash_cooldown=dash_cooldown,
            dash_number=dash_number,
            dash_cooldown_max=dash_cooldown_max,
            dash_segment_w=dash_segment_w,
            enemy_dash_x=enemy_dash_x,
            aggression_table=self.aggression_table,
        )

