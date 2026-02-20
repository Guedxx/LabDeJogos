"""Configurable enemy AI, replacing 6 near-identical IA_* functions."""

from settings import KING_PONG_AGGRESSION


class EnemyAI:
    """Data-driven AI that reproduces the behaviour of all 6 opponents.

    Parameters
    ----------
    base_speed : float
        Base movement speed when tracking the ball.
    momentum_gain : float
        How quickly momentum builds while moving.
    reaction_delay : float
        Initial reaction-delay counter value (reset after each decision).
    can_dash : bool
        Whether the enemy can dash (Ronaldinho).
    center_when_away : bool
        Whether the enemy drifts to centre when ball moves away (Ronaldinho).
    center_speed : float
        Speed at which the enemy drifts to centre.
    close_range : float
        X threshold for close-range behaviour (Ronaldinho dash zone).
    aggression_scaling : bool
        Whether speed/momentum scale with hits (King Pong).
    """

    def __init__(self, base_speed: float = 210,
                 momentum_gain: float = 100,
                 reaction_delay: float = 200,
                 can_dash: bool = False,
                 center_when_away: bool = False,
                 center_speed: float = 150,
                 close_range: float = 300,
                 aggression_scaling: bool = False):
        self.base_speed = base_speed
        self.momentum_gain = momentum_gain
        self.reaction_delay = reaction_delay
        self.can_dash = can_dash
        self.center_when_away = center_when_away
        self.center_speed = center_speed
        self.close_range = close_range
        self.aggression_scaling = aggression_scaling

    def update(self, pad_y: float, pad_h: float,
               ball_y: float, ball_h: float, ball_x: float,
               vel_x: float, dt: float,
               momentum: float, direction: int,
               delay_loop: float,
               num_hits: int = 0,
               # Dash state (only used by Ronaldinho)
               dash_cooldown: float = 0,
               dash_number: int = 3,
               dash_cooldown_max: float = 30,
               dash_segment_w: float = 80,
               enemy_dash_x: float = 0,
               ) -> dict:
        """Run one AI tick.

        Returns a dict with updated state values:
            direction, momentum, delay_loop,
            pad_dy (delta to add to pad y),
            dash_cooldown, dash_number, enemy_dash_x
        """
        speed = self.base_speed
        gain = self.momentum_gain

        # King Pong aggression scaling
        if self.aggression_scaling:
            clamped = min(num_hits, max(KING_PONG_AGGRESSION.keys()))
            speed = KING_PONG_AGGRESSION.get(clamped, 2000)
            gain = speed

        pad_dy = 0.0

        # Ronaldinho: drift to centre when ball moves away
        if self.center_when_away and vel_x > 0:
            mid = pad_y + pad_h / 2
            if mid < 450:
                pad_dy += (self.center_speed + momentum) * dt
            elif mid > 450:
                pad_dy -= (self.center_speed + momentum) * dt
            return {
                "direction": direction,
                "momentum": momentum,
                "delay_loop": delay_loop,
                "pad_dy": pad_dy,
                "dash_cooldown": dash_cooldown,
                "dash_number": dash_number,
                "enemy_dash_x": enemy_dash_x,
            }

        # Reaction-delay decision
        if delay_loop <= 0:
            pad_mid = pad_y + pad_h / 2
            ball_mid = ball_y + ball_h / 2
            if vel_x < 0:
                close_enough = True
                if self.center_when_away:
                    close_enough = ball_x < self.close_range
                if close_enough:
                    if pad_mid < ball_mid:
                        direction = -1  # need to move down
                    elif pad_mid > ball_mid:
                        direction = 1   # need to move up
                    delay_loop = self.reaction_delay

        # Movement
        if direction == -1 and vel_x < 0:
            pad_dy += (speed + momentum) * dt
            if momentum < 100 and pad_y > 150:
                momentum += gain * dt
            # Ronaldinho dash
            if (self.can_dash and ball_x < self.close_range
                    and (pad_y - ball_y) > 2 and dash_cooldown <= 0):
                pad_dy -= 100 * dt
                momentum += 5000 * dt
                enemy_dash_x -= dash_segment_w
                dash_cooldown = dash_cooldown_max
                dash_number -= 1

        elif direction == 1 and vel_x < 0:
            pad_dy -= (speed + momentum) * dt
            if momentum < 100 and pad_y > 150:
                momentum += gain * dt

        return {
            "direction": direction,
            "momentum": momentum,
            "delay_loop": delay_loop,
            "pad_dy": pad_dy,
            "dash_cooldown": dash_cooldown,
            "dash_number": dash_number,
            "enemy_dash_x": enemy_dash_x,
        }
