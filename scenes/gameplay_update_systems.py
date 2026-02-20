"""Extracted gameplay update systems used by GameplayScene."""

from __future__ import annotations

import random

from entities import PowerUp
from logic.collisions import resolve_paddle_bounce
from logic.helpers import patrol_vertical, track_target_center
from logic.powerups import (
    resolve_powerup_collision,
    should_spawn_powerup,
    spawn_source_level,
    update_speed_powerup,
)
from settings import (
    HELPER_PATROL_MIN_Y,
    KING_PONG_HOLD_TIME,
    LEVELS,
    MAX_LIVES,
    PLAYER_SPEED,
    POWERUP_ACTIVITY_BASE,
    POWERUP_COOLDOWN,
    POWERUP_SPAWN_CHANCE,
    POWERUP_TICK_SPEED,
    SCREEN_HEIGHT,
)


def update_powerups(scene, dt: float) -> None:
    assets = scene.game.assets
    level = scene.level_index

    scene.power_up_cooldown -= POWERUP_TICK_SPEED * dt

    roll = random.randint(0, 100)
    if should_spawn_powerup(
        level_index=level,
        cooldown=scene.power_up_cooldown,
        num_hits=scene.num_hits,
        roll=roll,
        trigger_roll=POWERUP_SPAWN_CHANCE,
    ):
        pu_level = spawn_source_level(level)
        pu_name = LEVELS[pu_level]["power_up_sprite"]
        pu_frames = LEVELS[pu_level]["power_up_frames"]
        pu_sheet = assets.get_spritesheet(pu_name, pu_frames, 100)
        scene.power_up = PowerUp(pu_sheet, scene.cfg["power_up_type"])
        scene.power_up.randomize_position()
        scene.can_draw_powerup = True
        scene.power_up_cooldown = POWERUP_COOLDOWN

    if scene.can_draw_powerup:
        scene.power_up.update_animation(dt * 1000)

    scene.ball.sync_rect()
    scene.power_up.sync_rect()

    if scene.power_up.visible and scene.ball.rect.colliderect(scene.power_up.rect):
        assets.play_sfx("powerUp.ogg")
        scene.power_up.deactivate()
        scene.can_draw_powerup = False

        outcome = resolve_powerup_collision(
            level_index=level,
            lives_player=scene.lives_player,
            lives_enemy=scene.lives_enemy,
            vel_x=scene.vel_x,
            vel_y=scene.vel_y,
            power_up_active=scene.power_up_active,
            power_up_activity_timer=scene.power_up_activity_timer,
            is_frozen=scene.is_frozen,
            freeze_timer=scene.freeze_timer,
            enemy_pad_position=(scene.enemy_pad.x, scene.enemy_pad.y),
            max_lives=MAX_LIVES,
            activity_base=POWERUP_ACTIVITY_BASE,
            freeze_duration=KING_PONG_HOLD_TIME,
        )
        scene.lives_player = outcome.lives_player
        scene.lives_enemy = outcome.lives_enemy
        scene.vel_x = outcome.vel_x
        scene.vel_y = outcome.vel_y
        scene.power_up_active = outcome.power_up_active
        scene.power_up_activity_timer = outcome.power_up_activity_timer
        scene.is_frozen = outcome.is_frozen
        scene.freeze_timer = outcome.freeze_timer
        scene.frozen_pos = outcome.frozen_pos

    scene.power_up_active, scene.power_up_activity_timer, scene.vel_player = update_speed_powerup(
        level_index=level,
        power_up_active=scene.power_up_active,
        power_up_activity_timer=scene.power_up_activity_timer,
        current_player_speed=scene.vel_player,
        dt=dt,
        tick_speed=POWERUP_TICK_SPEED,
        base_player_speed=PLAYER_SPEED,
        boosted_player_speed=400,
    )


def update_helpers(scene, dt: float) -> None:
    level = scene.level_index
    char_h = scene.player_anim.height

    if scene.enemy_helper and level == 1:
        scene.enemy_helper.update_animation(dt * 1000)
        threshold = scene.cfg["enemy_helper_track_threshold"]
        track_speed = scene.cfg["enemy_helper_track_speed"]
        helper = scene.enemy_helper

        if scene.vel_x < threshold:
            helper.y = track_target_center(
                y=helper.y,
                height=helper.height,
                target_y=scene.ball.y,
                target_height=scene.ball.height,
                speed=track_speed,
                dt=dt,
            )
        else:
            helper.y, helper.patrol_direction = patrol_vertical(
                y=helper.y,
                height=helper.height,
                min_y=char_h,
                max_y=SCREEN_HEIGHT,
                speed=helper.speed,
                direction=helper.patrol_direction,
                dt=dt,
            )

        _resolve_helper_collision(scene, helper, front_face="left")

    if scene.player_helper and level == 2 and scene.power_up_active:
        scene.power_up_activity_timer -= POWERUP_TICK_SPEED * dt
        helper = scene.player_helper
        helper.update_animation(dt * 1000)

        if scene.power_up_activity_timer > 0:
            threshold = scene.cfg["player_helper_track_threshold"]
            track_speed = scene.cfg["player_helper_track_speed"]

            if scene.vel_x > threshold:
                helper.y = track_target_center(
                    y=helper.y,
                    height=helper.height,
                    target_y=scene.ball.y,
                    target_height=scene.ball.height,
                    speed=track_speed,
                    dt=dt,
                )
            else:
                helper.y, helper.patrol_direction = patrol_vertical(
                    y=helper.y,
                    height=helper.height,
                    min_y=HELPER_PATROL_MIN_Y,
                    max_y=SCREEN_HEIGHT,
                    speed=helper.speed,
                    direction=helper.patrol_direction,
                    dt=dt,
                )

            _resolve_helper_collision(scene, helper, front_face="right")
        else:
            scene.power_up_active = False


def _resolve_helper_collision(scene, helper, *, front_face: str) -> None:
    helper.sync_rect()
    scene.ball.sync_rect()

    if scene.ball.rect.colliderect(helper.rect):
        scene.game.assets.play_sfx("paddle_sound.ogg")
        bx, by = scene.ball.x, scene.ball.y
        bw, bh = scene.ball.width, scene.ball.height
        hx, hy = helper.x, helper.y
        hw, hh = helper.width, helper.height
        scene.ball.x, scene.ball.y, scene.vel_x, scene.vel_y = resolve_paddle_bounce(
            ball_x=bx,
            ball_y=by,
            ball_w=bw,
            ball_h=bh,
            pad_x=hx,
            pad_y=hy,
            pad_w=hw,
            pad_h=hh,
            vel_x=scene.vel_x,
            vel_y=scene.vel_y,
            front_face=front_face,
        )
