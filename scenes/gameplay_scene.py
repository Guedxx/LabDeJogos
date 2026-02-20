"""Core gameplay scene - replaces the monolithic play() function."""

import random
import pygame
from scenes.base_scene import BaseScene, SceneTransition
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LEVELS,
    BALL_BASE_SPEED_X, BALL_BASE_SPEED_Y, BALL_SPEED_CAP, BALL_CRUISE_SPEED,
    BALL_SPEED_ACCEL_X, BALL_SPEED_ACCEL_Y,
    PLAYER_SPEED, MAX_LIVES, MAX_DASHES,
    DASH_COOLDOWN, DASH_RELOAD, DASH_MOMENTUM_BOOST,
    DASH_MOVE_BOOST_UP, DASH_MOVE_BOOST_DOWN,
    DASH_VEL_MULT_X, DASH_VEL_MULT_Y,
    MOMENTUM_DECAY, MOMENTUM_CAP, MOMENTUM_GAIN_PLAYER,
    PLAYER_HEARTS_POS, PLAYER_DASH_POS,
    ENEMY_HEARTS_POS, ENEMY_DASH_POS,
    POWERUP_COOLDOWN, POWERUP_ACTIVITY_BASE,
    POWERUP_TICK_SPEED, DELAY_REACT_TICK_SPEED,
    BULK_HOLD_TIME, BULK_SLOW_TIME, BULK_SLOW_SPEED, BULK_HOLD_CHANCE,
    KING_PONG_HOLD_TIME,
    RONALDINHO_OLE_CHANCE, RONALDINHO_OLE_VEL_Y_MULT, RONALDINHO_OLE_VEL_X_MULT,
    ORB_FRAMES, ORB_FRAME_DURATION,
    MAIN_CHAR_FRAMES, MAIN_CHAR_FRAME_DURATION,
    PLAYER_PAD_OFFSET_X, ENEMY_PAD_X,
)
from entities import Paddle, AnimatedEntity, Ball, HelperPaddle, PowerUp
from ai import EnemyAI
from hud import HUD
from scenes.gameplay_update_systems import (
    update_helpers as run_helper_update,
    update_powerups as run_powerup_update,
)
from logic.ball_rules import accelerate_ball, clamp_ball_speed_framewise, resolve_wall_and_scoring
from logic.collisions import (
    apply_enemy_momentum_deflection,
    apply_player_momentum_deflection,
    resolve_paddle_bounce,
)
from logic.enemy_rules import (
    apply_enemy_momentum_motion,
    apply_post_ai_momentum_motion,
    clamp_enemy_bounds,
    decay_enemy_momentum,
    tick_delay_react,
)
from logic.level_mechanics import (
    apply_ronaldinho_ole,
    update_bulk_hold_mechanic,
    update_king_pong_freeze,
)
from logic.player_rules import (
    apply_player_input,
    apply_player_momentum_motion,
    clamp_player_bounds,
    decay_player_momentum,
    update_player_dash_state,
)


class GameplayScene(BaseScene):
    """Runs a single level of gameplay."""

    def __init__(self, game, level_index: int):
        super().__init__(game)
        self.level_index = level_index
        self.cfg = LEVELS[level_index]
        assets = game.assets

        # ---- Player character (animated, top-right corner) ----
        self.player_sheet = assets.get_spritesheet(
            "SHEETMainChar.png", MAIN_CHAR_FRAMES, MAIN_CHAR_FRAME_DURATION)
        self.player_anim = AnimatedEntity(
            self.player_sheet,
            SCREEN_WIDTH - self.player_sheet.frame_width, 0)
        self.player_anim.spritesheet.play()

        # ---- Player paddle ----
        pad_surf = assets.get_image("PAD_Player.png")
        pad_x = SCREEN_WIDTH - pad_surf.get_width() - PLAYER_PAD_OFFSET_X
        pad_y = ((SCREEN_HEIGHT + self.player_anim.height) / 2
                 - pad_surf.get_height() / 2)
        self.player_pad = Paddle(pad_surf, pad_x, pad_y)

        # ---- Enemy character ----
        self.enemy_sheet = assets.get_spritesheet(
            self.cfg["enemy_sheet"], self.cfg["enemy_frames"],
            self.cfg["enemy_frame_duration"])
        self.enemy_anim = AnimatedEntity(self.enemy_sheet, 0, 0)
        self.enemy_anim.spritesheet.play()

        # ---- Enemy paddle ----
        if self.cfg.get("enemy_pad_animated", False):
            epad_sheet = assets.get_spritesheet(
                self.cfg["enemy_pad"],
                self.cfg.get("enemy_pad_frames", 4),
                self.cfg.get("enemy_pad_frame_duration", 100))
            self.enemy_pad_animated = True
            self.enemy_pad_sheet = epad_sheet
            first_frame = epad_sheet.get_current_frame()
            ep_x = ENEMY_PAD_X
            ep_y = ((SCREEN_HEIGHT + self.player_anim.height) / 2
                    - epad_sheet.frame_height / 2)
            self.enemy_pad = Paddle(first_frame, ep_x, ep_y)
        else:
            self.enemy_pad_animated = False
            self.enemy_pad_sheet = None
            epad_surf = assets.get_image(self.cfg["enemy_pad"])
            ep_x = ENEMY_PAD_X
            ep_y = ((SCREEN_HEIGHT + self.player_anim.height) / 2
                    - epad_surf.get_height() / 2)
            self.enemy_pad = Paddle(epad_surf, ep_x, ep_y)

        # ---- Background ----
        if self.cfg["bg_animated"]:
            self.bg_sheet = assets.get_spritesheet(
                self.cfg["background"], self.cfg["bg_frames"],
                self.cfg["bg_frame_duration"])
            self.bg_static = None
        else:
            self.bg_sheet = None
            self.bg_static = assets.get_image(self.cfg["background"])

        # ---- Hotbar ----
        self.hotbar = assets.get_image("HOTBAR.png")

        # ---- Orb / Ball ----
        orb_sheet = assets.get_spritesheet(
            "SHEETORB.png", ORB_FRAMES, ORB_FRAME_DURATION)
        self.ball = Ball(
            orb_sheet,
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            BALL_BASE_SPEED_X, BALL_BASE_SPEED_Y)
        self.ball.spritesheet.play()

        # ---- Velocities ----
        self.vel_x = float(BALL_BASE_SPEED_X)
        self.vel_y = float(BALL_BASE_SPEED_Y)
        self.vel_player = float(PLAYER_SPEED)

        # ---- Dash state ----
        self.dash_cooldown_player = float(DASH_COOLDOWN)
        self.dash_cooldown_enemy = float(DASH_COOLDOWN)
        self.dash_reload_player = float(DASH_RELOAD)
        self.dash_reload_enemy = float(DASH_RELOAD)
        self.dash_number_player = MAX_DASHES
        self.dash_number_enemy = MAX_DASHES
        self.first_dash_player = False

        # ---- Momentum ----
        self.momentum_player = 0.0
        self.momentum_dir_player = 0
        self.momentum_enemy = 0.0
        self.momentum_dir_enemy = 0

        # ---- Lives ----
        self.lives_player = MAX_LIVES
        self.lives_enemy = MAX_LIVES

        # ---- HUD ----
        hearts_surf = assets.get_image("HEARTS.png")
        dash_surf = assets.get_image("DASHBAR.png")
        self.hud_player = HUD(hearts_surf, dash_surf,
                              PLAYER_HEARTS_POS, PLAYER_DASH_POS, True)
        self.hud_enemy = HUD(hearts_surf, dash_surf,
                             ENEMY_HEARTS_POS, ENEMY_DASH_POS, False)

        # ---- Power-up ----
        pu_sprite_name = self.cfg["power_up_sprite"]
        pu_frames = self.cfg["power_up_frames"]
        pu_sheet = assets.get_spritesheet(pu_sprite_name, pu_frames, 100)
        self.power_up = PowerUp(pu_sheet, self.cfg["power_up_type"])
        self.power_up_cooldown = float(POWERUP_COOLDOWN)
        self.power_up_active = False
        self.power_up_activity_timer = float(POWERUP_ACTIVITY_BASE)
        self.can_draw_powerup = False

        # ---- AI ----
        self.ai = EnemyAI(
            base_speed=self.cfg["ai_speed"],
            momentum_gain=self.cfg["ai_momentum_gain"],
            reaction_delay=self.cfg["ai_delay"],
            can_dash=self.cfg["enemy_can_dash"],
            center_when_away=(level_index == 3),  # Ronaldinho
            center_speed=150,
            close_range=300,
            aggression_scaling=self.cfg["aggression_scaling"],
        )
        self.delay_react = float(self.cfg["ai_delay"])
        self.delay_react_loop = float(self.cfg["ai_delay"])
        self.num_hits = 0

        # ---- Enemy helper (Dr. Rippon) ----
        self.enemy_helper = None
        if self.cfg["has_enemy_helper"]:
            eh_sheet = assets.get_spritesheet(
                self.cfg["enemy_helper_sprite"],
                self.cfg["enemy_helper_frames"],
                self.cfg["enemy_helper_frame_duration"])
            eh_x = ENEMY_PAD_X
            eh_y = self.player_anim.height + 5
            self.enemy_helper = HelperPaddle(eh_sheet, eh_x, eh_y,
                                             self.cfg["enemy_helper_speed"])

        # ---- Player helper (Cinos) ----
        self.player_helper = None
        if self.cfg["has_player_helper"]:
            ph_sheet = assets.get_spritesheet(
                self.cfg["player_helper_sprite"],
                self.cfg["player_helper_frames"],
                self.cfg["player_helper_frame_duration"])
            ph_x = self.player_pad.x
            ph_y = self.player_pad.y
            self.player_helper = HelperPaddle(ph_sheet, ph_x, ph_y,
                                              self.cfg["player_helper_speed"])

        # ---- Bulk hold mechanic ----
        self.is_holding = False
        self.hold_timer = float(BULK_HOLD_TIME)
        self.thrown = False
        self.is_slow = False
        self.slow_timer = float(BULK_SLOW_TIME)
        self.bulk_hold_surf = None
        self.bulk_throw_dir = 1  # direction for Bulk's throw
        if self.cfg["bulk_hold_sprite"]:
            self.bulk_hold_surf = assets.get_image(self.cfg["bulk_hold_sprite"])

        # ---- King Pong freeze ----
        self.is_frozen = False
        self.freeze_timer = float(KING_PONG_HOLD_TIME)
        self.frozen_pos = (0.0, 0.0)

        # ---- Enemy dash x tracking (for HUD segment offsets) ----
        self.enemy_dash_x = float(ENEMY_DASH_POS[0])

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if self.level_index < 5:
                    return SceneTransition("level_clear", level=self.level_index)
                return SceneTransition("credits")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return SceneTransition("pause", level=self.level_index,
                                   gameplay_scene=self)
        return None

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt_ms):
        dt = dt_ms / 1000.0
        if dt <= 0:
            return None

        keys = pygame.key.get_pressed()

        # ---- Ball speed clamping ----
        self.vel_x = clamp_ball_speed_framewise(self.vel_x, BALL_SPEED_CAP, 10)

        # ---- Ball wall collisions ----
        transition = self._ball_wall_collisions(dt)
        if transition:
            return transition

        # ---- Ball-paddle collisions ----
        self._ball_paddle_collisions(keys)

        # ---- Ball movement ----
        self.ball.x += self.vel_x * dt
        self.ball.y += self.vel_y * dt

        # ---- Ball speed gradual increase ----
        self.vel_x, self.vel_y = accelerate_ball(
            self.vel_x,
            self.vel_y,
            BALL_CRUISE_SPEED,
            BALL_SPEED_ACCEL_X,
            BALL_SPEED_ACCEL_Y,
            dt,
        )

        # ---- Player input ----
        self._handle_player_input(keys, dt)

        # ---- Enemy AI ----
        self._update_enemy_ai(dt)

        # ---- Power-ups ----
        run_powerup_update(self, dt)

        # ---- Helpers ----
        run_helper_update(self, dt)

        # ---- Level-specific mechanics ----
        self._update_level_mechanics(dt)

        # ---- Animations ----
        self.ball.update_animation(dt_ms)
        self.enemy_anim.update_animation(dt_ms)
        self.player_anim.update_animation(dt_ms)
        if self.bg_sheet:
            self.bg_sheet.update(dt_ms)
        if self.enemy_pad_animated and self.enemy_pad_sheet:
            self.enemy_pad_sheet.update(dt_ms)
            self.enemy_pad.image = self.enemy_pad_sheet.get_current_frame()

        # ---- Game over check ----
        if self.lives_player <= 0:
            return SceneTransition("game_over", level=self.level_index)

        return None

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, screen):
        # Background
        if self.bg_sheet:
            screen.blit(self.bg_sheet.get_current_frame(), (0, 0))
        else:
            screen.blit(self.bg_static, (0, 0))

        # Hotbar
        screen.blit(self.hotbar, (0, 0))

        # Ball
        self.ball.draw(screen)

        # HUD
        self.hud_player.draw(screen, self.lives_player, self.dash_number_player)
        self.hud_enemy.draw(screen, self.lives_enemy, self.dash_number_enemy)

        # Paddles
        self.player_pad.draw(screen)
        self.enemy_pad.draw(screen)

        # Characters
        self.player_anim.draw(screen)
        self.enemy_anim.draw(screen)

        # Enemy helper
        if self.enemy_helper:
            self.enemy_helper.draw(screen)

        # Player helper (only when power-up active)
        if (self.player_helper and self.power_up_active
                and self.level_index == 2):
            self.player_helper.draw(screen)

        # Bulk hold sprite
        if self.is_holding and self.bulk_hold_surf:
            screen.blit(self.bulk_hold_surf,
                         (int(self.enemy_pad.x), int(self.enemy_pad.y)))

        # Power-up
        if self.can_draw_powerup:
            self.power_up.draw(screen)

    # ------------------------------------------------------------------
    # Ball-wall collisions
    # ------------------------------------------------------------------
    def _ball_wall_collisions(self, dt) -> SceneTransition | None:
        outcome = resolve_wall_and_scoring(
            ball_x=self.ball.x,
            ball_y=self.ball.y,
            ball_w=self.ball.width,
            ball_h=self.ball.height,
            vel_x=self.vel_x,
            vel_y=self.vel_y,
            lives_player=self.lives_player,
            lives_enemy=self.lives_enemy,
            num_hits=self.num_hits,
            level_index=self.level_index,
            screen_w=SCREEN_WIDTH,
            screen_h=SCREEN_HEIGHT,
            char_h=self.enemy_anim.height,
        )

        for sound_name in outcome.sounds:
            self.game.assets.play_sfx(sound_name)

        self.ball.x = outcome.ball_x
        self.ball.y = outcome.ball_y
        self.vel_x = outcome.vel_x
        self.vel_y = outcome.vel_y
        self.lives_player = outcome.lives_player
        self.lives_enemy = outcome.lives_enemy
        self.num_hits = outcome.num_hits

        if outcome.transition_target == "level_clear":
            return SceneTransition("level_clear", level=outcome.transition_level)
        if outcome.transition_target == "credits":
            return SceneTransition("credits")
        return None

    # ------------------------------------------------------------------
    # Ball-paddle collisions
    # ------------------------------------------------------------------
    def _ball_paddle_collisions(self, keys):
        assets = self.game.assets
        bx, by, bw, bh = self.ball.x, self.ball.y, self.ball.width, self.ball.height
        self.ball.sync_rect()

        # Player pad collision
        self.player_pad.sync_rect()
        if self.ball.rect.colliderect(self.player_pad.rect):
            assets.play_sfx("paddle_sound.ogg")
            px, py, pw, ph = (self.player_pad.x, self.player_pad.y,
                               self.player_pad.width, self.player_pad.height)
            self.ball.x, self.ball.y, self.vel_x, self.vel_y = resolve_paddle_bounce(
                ball_x=bx,
                ball_y=by,
                ball_w=bw,
                ball_h=bh,
                pad_x=px,
                pad_y=py,
                pad_w=pw,
                pad_h=ph,
                vel_x=self.vel_x,
                vel_y=self.vel_y,
                front_face="right",
            )

            # Momentum-based deflection
            self.vel_x, self.vel_y = apply_player_momentum_deflection(
                vel_x=self.vel_x,
                vel_y=self.vel_y,
                momentum_direction=self.momentum_dir_player,
                momentum_enemy=self.momentum_enemy,
            )

            # Dash on hit
            if keys[pygame.K_SPACE] and self.dash_number_player > 0:
                assets.play_sfx("ANIMATIONexplosion.ogg")
                self.vel_x *= DASH_VEL_MULT_X
                self.vel_y *= DASH_VEL_MULT_Y

        # Enemy pad collision
        self.enemy_pad.sync_rect()
        if self.ball.rect.colliderect(self.enemy_pad.rect):
            assets.play_sfx("paddle_sound.ogg")
            ex, ey, ew, eh = (self.enemy_pad.x, self.enemy_pad.y,
                               self.enemy_pad.width, self.enemy_pad.height)
            self.ball.x, self.ball.y, self.vel_x, self.vel_y = resolve_paddle_bounce(
                ball_x=bx,
                ball_y=by,
                ball_w=bw,
                ball_h=bh,
                pad_x=ex,
                pad_y=ey,
                pad_w=ew,
                pad_h=eh,
                vel_x=self.vel_x,
                vel_y=self.vel_y,
                front_face="left",
            )

            # Enemy momentum-based deflection
            self.vel_x, self.vel_y = apply_enemy_momentum_deflection(
                vel_x=self.vel_x,
                vel_y=self.vel_y,
                momentum_direction=self.momentum_dir_enemy,
                momentum_enemy=self.momentum_enemy,
            )

    # ------------------------------------------------------------------
    # Player input
    # ------------------------------------------------------------------
    def _handle_player_input(self, keys, dt):
        char_h = self.player_anim.height

        # Dash counters
        dash = update_player_dash_state(
            dash_cooldown=self.dash_cooldown_player,
            dash_reload=self.dash_reload_player,
            dash_number=self.dash_number_player,
            first_dash=self.first_dash_player,
            max_dashes=MAX_DASHES,
            dash_reload_max=DASH_RELOAD,
        )
        self.dash_cooldown_player = dash.dash_cooldown
        self.dash_reload_player = dash.dash_reload
        self.dash_number_player = dash.dash_number
        self.first_dash_player = dash.first_dash

        # Player momentum decay
        momentum = decay_player_momentum(
            momentum=self.momentum_player,
            momentum_direction=self.momentum_dir_player,
            decay_rate=MOMENTUM_DECAY,
            dt=dt,
        )
        self.momentum_player = momentum.momentum
        self.momentum_dir_player = momentum.momentum_direction

        # Momentum movement
        self.player_pad.y = apply_player_momentum_motion(
            y=self.player_pad.y,
            momentum=self.momentum_player,
            momentum_direction=self.momentum_dir_player,
            dt=dt,
        )

        input_outcome = apply_player_input(
            y=self.player_pad.y,
            height=self.player_pad.height,
            char_h=char_h,
            screen_h=SCREEN_HEIGHT,
            vel_player=self.vel_player,
            momentum=self.momentum_player,
            momentum_direction=self.momentum_dir_player,
            press_w=bool(keys[pygame.K_w]),
            press_s=bool(keys[pygame.K_s]),
            press_space=bool(keys[pygame.K_SPACE]),
            dash_cooldown=self.dash_cooldown_player,
            dash_number=self.dash_number_player,
            first_dash=self.first_dash_player,
            momentum_cap=MOMENTUM_CAP,
            momentum_gain=MOMENTUM_GAIN_PLAYER,
            dash_move_boost_up=DASH_MOVE_BOOST_UP,
            dash_move_boost_down=DASH_MOVE_BOOST_DOWN,
            dash_momentum_boost=DASH_MOMENTUM_BOOST,
            dash_cooldown_reset=DASH_COOLDOWN,
            dt=dt,
        )
        self.player_pad.y = input_outcome.y
        self.momentum_player = input_outcome.momentum
        self.momentum_dir_player = input_outcome.momentum_direction
        self.dash_cooldown_player = input_outcome.dash_cooldown
        self.dash_number_player = input_outcome.dash_number
        self.first_dash_player = input_outcome.first_dash

        # Wall clamping
        clamp_outcome, clamped_y = clamp_player_bounds(
            y=self.player_pad.y,
            height=self.player_pad.height,
            char_h=char_h,
            screen_h=SCREEN_HEIGHT,
            momentum=self.momentum_player,
            momentum_direction=self.momentum_dir_player,
            momentum_cap=MOMENTUM_CAP,
            dt=dt,
        )
        self.player_pad.y = clamped_y
        self.momentum_player = clamp_outcome.momentum
        self.momentum_dir_player = clamp_outcome.momentum_direction

    # ------------------------------------------------------------------
    # Enemy AI
    # ------------------------------------------------------------------
    def _update_enemy_ai(self, dt):
        char_h = self.player_anim.height

        # Enemy momentum decay
        decayed = decay_enemy_momentum(
            momentum=self.momentum_enemy,
            momentum_direction=self.momentum_dir_enemy,
            decay_rate=MOMENTUM_DECAY,
            dt=dt,
        )
        self.momentum_enemy = decayed.momentum
        self.momentum_dir_enemy = decayed.momentum_direction

        # Momentum movement (applied before AI)
        self.enemy_pad.y = apply_enemy_momentum_motion(
            y=self.enemy_pad.y,
            momentum=self.momentum_enemy,
            momentum_direction=self.momentum_dir_enemy,
            dt=dt,
        )

        # Wall clamping
        self.enemy_pad.y, clamp_outcome = clamp_enemy_bounds(
            y=self.enemy_pad.y,
            height=self.enemy_pad.height,
            min_y=char_h,
            max_y=SCREEN_HEIGHT,
            momentum=self.momentum_enemy,
            momentum_direction=self.momentum_dir_enemy,
        )
        self.momentum_enemy = clamp_outcome.momentum
        self.momentum_dir_enemy = clamp_outcome.momentum_direction

        # Delay react countdown
        self.delay_react_loop = tick_delay_react(
            self.delay_react_loop,
            DELAY_REACT_TICK_SPEED,
            dt,
        )

        # Run AI
        result = self.ai.update(
            pad_y=self.enemy_pad.y,
            pad_h=self.enemy_pad.height,
            ball_y=self.ball.y,
            ball_h=self.ball.height,
            ball_x=self.ball.x,
            vel_x=self.vel_x,
            dt=dt,
            momentum=self.momentum_enemy,
            direction=self.momentum_dir_enemy,
            delay_loop=self.delay_react_loop,
            num_hits=self.num_hits,
            dash_cooldown=self.dash_cooldown_enemy,
            dash_number=self.dash_number_enemy,
            dash_cooldown_max=DASH_COOLDOWN,
            dash_segment_w=80,
            enemy_dash_x=self.enemy_dash_x,
        )

        self.momentum_dir_enemy = result["direction"]
        self.momentum_enemy = result["momentum"]
        self.delay_react_loop = result["delay_loop"]
        self.dash_cooldown_enemy = result["dash_cooldown"]
        self.dash_number_enemy = result["dash_number"]
        self.enemy_dash_x = result["enemy_dash_x"]

        # Apply AI movement
        if result["pad_dy"] != 0:
            self.enemy_pad.y += result["pad_dy"]

        # Post-AI momentum movement
        self.enemy_pad.y = apply_post_ai_momentum_motion(
            y=self.enemy_pad.y,
            momentum=self.momentum_enemy,
            momentum_direction=self.momentum_dir_enemy,
            dt=dt,
        )

    # ------------------------------------------------------------------
    # Level-specific mechanics
    # ------------------------------------------------------------------
    def _update_level_mechanics(self, dt):
        level = self.level_index

        ole = apply_ronaldinho_ole(
            level_index=level,
            has_ole=self.cfg["has_ole"],
            vel_x=self.vel_x,
            vel_y=self.vel_y,
            roll=random.randint(0, 200),
            trigger_roll=RONALDINHO_OLE_CHANCE,
            vel_y_multiplier=RONALDINHO_OLE_VEL_Y_MULT,
            vel_x_multiplier=RONALDINHO_OLE_VEL_X_MULT,
        )
        self.vel_x = ole.vel_x
        self.vel_y = ole.vel_y
        if ole.triggered:
            self.game.assets.play_sfx("paddle_sound.ogg")

        self.enemy_pad.sync_rect()
        self.ball.sync_rect()
        enemy_ball_collided = self.ball.rect.colliderect(self.enemy_pad.rect)
        hold_roll = -1
        throw_dir = self.bulk_throw_dir
        if enemy_ball_collided:
            hold_roll = random.randint(0, 10)
            if hold_roll == BULK_HOLD_CHANCE:
                throw_dir = random.choice([-1, 1])

        player_ball_collided = self.ball.rect.colliderect(self.player_pad.rect)

        bulk = update_bulk_hold_mechanic(
            level_index=level,
            has_hold=self.cfg["has_hold"],
            enemy_ball_collided=enemy_ball_collided,
            player_ball_collided=player_ball_collided,
            hold_roll=hold_roll,
            hold_trigger_roll=BULK_HOLD_CHANCE,
            throw_direction_roll=throw_dir,
            is_holding=self.is_holding,
            hold_timer=self.hold_timer,
            thrown=self.thrown,
            is_slow=self.is_slow,
            slow_timer=self.slow_timer,
            bulk_throw_dir=self.bulk_throw_dir,
            momentum_dir_enemy=self.momentum_dir_enemy,
            momentum_player=self.momentum_player,
            vel_player=self.vel_player,
            vel_x=self.vel_x,
            vel_y=self.vel_y,
            ball_x=self.ball.x,
            ball_y=self.ball.y,
            ball_h=self.ball.height,
            enemy_pad_x=self.enemy_pad.x,
            enemy_pad_y=self.enemy_pad.y,
            enemy_pad_h=self.enemy_pad.height,
            dt=dt,
            hold_duration=BULK_HOLD_TIME,
            slow_duration=BULK_SLOW_TIME,
            tick_speed=POWERUP_TICK_SPEED,
            slow_player_speed=BULK_SLOW_SPEED,
            base_player_speed=PLAYER_SPEED,
        )
        self.is_holding = bulk.is_holding
        self.hold_timer = bulk.hold_timer
        self.thrown = bulk.thrown
        self.is_slow = bulk.is_slow
        self.slow_timer = bulk.slow_timer
        self.bulk_throw_dir = bulk.bulk_throw_dir
        self.momentum_dir_enemy = bulk.momentum_dir_enemy
        self.momentum_player = bulk.momentum_player
        self.vel_player = bulk.vel_player
        self.vel_x = bulk.vel_x
        self.vel_y = bulk.vel_y
        self.ball.x = bulk.ball_x
        self.ball.y = bulk.ball_y

        freeze = update_king_pong_freeze(
            level_index=level,
            num_hits=self.num_hits,
            is_frozen=self.is_frozen,
            freeze_timer=self.freeze_timer,
            enemy_pad_x=self.enemy_pad.x,
            enemy_pad_y=self.enemy_pad.y,
            frozen_pos=self.frozen_pos,
            dt=dt,
            tick_speed=POWERUP_TICK_SPEED,
        )
        self.is_frozen = freeze.is_frozen
        self.freeze_timer = freeze.freeze_timer
        self.enemy_pad.x = freeze.enemy_pad_x
        self.enemy_pad.y = freeze.enemy_pad_y
