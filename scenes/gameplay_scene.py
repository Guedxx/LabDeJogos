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
    POWERUP_COOLDOWN, POWERUP_SPAWN_CHANCE, POWERUP_ACTIVITY_BASE,
    POWERUP_TICK_SPEED, DELAY_REACT_TICK_SPEED,
    BULK_HOLD_TIME, BULK_SLOW_TIME, BULK_SLOW_SPEED, BULK_HOLD_CHANCE,
    KING_PONG_HOLD_TIME,
    RONALDINHO_OLE_CHANCE, RONALDINHO_OLE_VEL_Y_MULT, RONALDINHO_OLE_VEL_X_MULT,
    ORB_FRAMES, ORB_FRAME_DURATION,
    MAIN_CHAR_FRAMES, MAIN_CHAR_FRAME_DURATION,
    PLAYER_PAD_OFFSET_X, ENEMY_PAD_X,
    HELPER_PATROL_MIN_Y,
)
from entities import Paddle, AnimatedEntity, Ball, HelperPaddle, PowerUp
from ai import EnemyAI
from hud import HUD
from logic.physics import accelerate_towards_cap, apply_speed_soft_limit, decay_momentum
from logic.powerups import (
    resolve_powerup_collision,
    should_spawn_powerup,
    spawn_source_level,
    update_speed_powerup,
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
        # Keep legacy frame-based clamp behaviour by using dt=1.0.
        self.vel_x = apply_speed_soft_limit(self.vel_x, BALL_SPEED_CAP, 10, 1.0)

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
        self.vel_x = accelerate_towards_cap(
            self.vel_x,
            BALL_CRUISE_SPEED,
            BALL_SPEED_ACCEL_X,
            dt,
        )
        self.vel_y = accelerate_towards_cap(
            self.vel_y,
            BALL_CRUISE_SPEED,
            BALL_SPEED_ACCEL_Y,
            dt,
        )

        # ---- Player input ----
        self._handle_player_input(keys, dt)

        # ---- Enemy AI ----
        self._update_enemy_ai(dt)

        # ---- Power-ups ----
        self._update_powerups(dt)

        # ---- Helpers ----
        self._update_helpers(dt)

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
        assets = self.game.assets

        # Right wall -> enemy scores
        if self.ball.x + self.ball.width >= SCREEN_WIDTH:
            assets.play_sfx("hit_sound.ogg")
            self.ball.x = SCREEN_WIDTH - self.ball.width - 2
            self.lives_player -= 1
            self.vel_x = -(self.vel_x / 2)
            self.vel_y = self.vel_y / 2

        # Left wall -> player scores
        if self.ball.x <= 0:
            assets.play_sfx("hit_sound.ogg")
            self.ball.x = 2
            self.lives_enemy -= 1
            self.num_hits += 1

            if self.lives_enemy <= 0 and self.level_index != 5:
                return SceneTransition("level_clear", level=self.level_index)
            if self.lives_enemy <= -1 and self.level_index == 5:
                return SceneTransition("credits")

            self.vel_x = -(self.vel_x - 30)
            self.vel_y = self.vel_y - 15

        # Bottom wall
        if self.ball.y >= SCREEN_HEIGHT - self.ball.height:
            assets.play_sfx("wall_sound.ogg")
            self.ball.y = SCREEN_HEIGHT - self.ball.height
            self.vel_y *= -1

        # Top wall (below character banner)
        char_h = self.enemy_anim.height
        if self.ball.y <= char_h:
            assets.play_sfx("wall_sound.ogg")
            self.ball.y = char_h
            self.vel_y *= -1

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
            if abs(bx + bw - px) < 20:
                self.vel_x *= -1
                self.ball.x = px - bw
            elif abs(by + bh - py) < 20 and self.vel_y > 0:
                self.vel_y *= -1
                self.ball.y = py - bh
            elif abs(by - (py + ph)) < 20 and self.vel_y < 0:
                self.vel_y *= -1
                self.ball.y = py + ph

            # Momentum-based deflection
            if self.momentum_dir_player == 1 and self.vel_y > 0:
                self.vel_x += self.momentum_enemy * 2
                self.vel_y += self.momentum_enemy * 2
                self.vel_y *= -1
            if self.momentum_dir_player == -1 and self.vel_y < 0:
                self.vel_x += self.momentum_enemy * 2
                self.vel_y += self.momentum_enemy * 2
                self.vel_y *= -1

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
            if abs(bx - (ex + ew)) < 20:
                self.vel_x *= -1
                self.ball.x = ex + ew
            elif abs(by + bh - ey) < 20 and self.vel_y > 0:
                self.vel_y *= -1
                self.ball.y = ey - bh
            elif abs(by - (ey + eh)) < 20 and self.vel_y < 0:
                self.vel_y *= -1
                self.ball.y = ey + eh

            # Enemy momentum-based deflection
            if self.momentum_dir_enemy == -1 and self.vel_y > 0:
                self.vel_x += self.momentum_enemy * 2
                self.vel_y += self.momentum_enemy * 2
                self.vel_y *= -1
            if self.momentum_dir_enemy == 1 and self.vel_y < 0:
                self.vel_x += self.momentum_enemy * 2
                self.vel_y += self.momentum_enemy * 2
                self.vel_y *= -1

    # ------------------------------------------------------------------
    # Player input
    # ------------------------------------------------------------------
    def _handle_player_input(self, keys, dt):
        char_h = self.player_anim.height

        # Dash counters
        self.dash_cooldown_player -= 1
        if self.first_dash_player:
            self.dash_reload_player -= 1
        if self.dash_number_player >= MAX_DASHES:
            self.first_dash_player = False
        if (self.dash_reload_player <= 0
                and self.dash_number_player < MAX_DASHES):
            self.dash_number_player += 1
            self.dash_reload_player = DASH_RELOAD

        # Player momentum decay
        if self.momentum_player > 0:
            self.momentum_player = decay_momentum(self.momentum_player, MOMENTUM_DECAY, dt)
            if self.momentum_player < 1 * dt:
                self.momentum_player = 0
                self.momentum_dir_player = 0

        # Momentum movement
        if self.momentum_dir_player == 1:
            self.player_pad.y -= self.momentum_player * dt
        elif self.momentum_dir_player == -1:
            self.player_pad.y += self.momentum_player * dt

        # W = up
        if keys[pygame.K_w]:
            self.player_pad.y -= (self.vel_player * dt
                                  + self.momentum_player * dt)
            if (self.momentum_player < MOMENTUM_CAP
                    and self.player_pad.y > char_h):
                self.momentum_player += MOMENTUM_GAIN_PLAYER * dt
            self.momentum_dir_player = 1

            if (keys[pygame.K_SPACE]
                    and self.dash_cooldown_player < 0
                    and self.dash_number_player > 0):
                self.first_dash_player = True
                self.player_pad.y -= DASH_MOVE_BOOST_UP * dt
                self.momentum_player += DASH_MOMENTUM_BOOST * dt
                self.dash_cooldown_player = DASH_COOLDOWN
                self.dash_number_player -= 1

        # S = down
        elif keys[pygame.K_s]:
            self.player_pad.y += (self.vel_player * dt
                                  + self.momentum_player * dt)
            if (self.momentum_player < MOMENTUM_CAP
                    and self.player_pad.y + self.player_pad.height < SCREEN_HEIGHT):
                self.momentum_player += MOMENTUM_GAIN_PLAYER * dt
            self.momentum_dir_player = -1

            if (keys[pygame.K_SPACE]
                    and self.dash_cooldown_player < 0
                    and self.dash_number_player > 0):
                self.first_dash_player = True
                self.player_pad.y += DASH_MOVE_BOOST_DOWN * dt
                self.momentum_player += DASH_MOMENTUM_BOOST * dt
                self.dash_cooldown_player = DASH_COOLDOWN
                self.dash_number_player -= 1

        # Wall clamping
        if self.player_pad.y < char_h:
            self.player_pad.y = char_h
            self.momentum_dir_player = -1
            if self.momentum_player < MOMENTUM_CAP:
                self.momentum_player += self.momentum_player * dt
        elif self.player_pad.y + self.player_pad.height > SCREEN_HEIGHT:
            self.player_pad.y = SCREEN_HEIGHT - self.player_pad.height
            self.momentum_dir_player = 1
            if self.momentum_player < MOMENTUM_CAP:
                self.momentum_player += self.momentum_player * dt

    # ------------------------------------------------------------------
    # Enemy AI
    # ------------------------------------------------------------------
    def _update_enemy_ai(self, dt):
        char_h = self.player_anim.height

        # Enemy momentum decay
        if self.momentum_enemy > 0:
            self.momentum_enemy = decay_momentum(self.momentum_enemy, MOMENTUM_DECAY, dt)
            if self.momentum_enemy <= 0:
                self.momentum_enemy = 0
                self.momentum_dir_enemy = 0

        # Momentum movement (applied before AI)
        if self.momentum_dir_enemy == 1:
            self.enemy_pad.y -= self.momentum_enemy * dt
        elif self.momentum_dir_enemy == -1:
            self.enemy_pad.y += self.momentum_enemy * dt

        # Wall clamping
        if self.enemy_pad.y < char_h:
            self.enemy_pad.y = char_h
            self.momentum_enemy = 0
            self.momentum_dir_enemy = 0
        if self.enemy_pad.y + self.enemy_pad.height > SCREEN_HEIGHT:
            self.enemy_pad.y = SCREEN_HEIGHT - self.enemy_pad.height
            self.momentum_enemy = 0
            self.momentum_dir_enemy = 0

        # Delay react countdown
        self.delay_react_loop -= DELAY_REACT_TICK_SPEED * dt

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
        if self.momentum_dir_enemy == 1:
            self.enemy_pad.y -= self.momentum_enemy * dt
        elif self.momentum_dir_enemy == -1:
            self.enemy_pad.y += self.momentum_enemy * dt

    # ------------------------------------------------------------------
    # Power-ups
    # ------------------------------------------------------------------
    def _update_powerups(self, dt):
        assets = self.game.assets
        level = self.level_index

        self.power_up_cooldown -= POWERUP_TICK_SPEED * dt

        # Spawn logic
        roll = random.randint(0, 100)
        if should_spawn_powerup(
            level_index=level,
            cooldown=self.power_up_cooldown,
            num_hits=self.num_hits,
            roll=roll,
            trigger_roll=POWERUP_SPAWN_CHANCE,
        ):
            pu_level = spawn_source_level(level)
            pu_name = LEVELS[pu_level]["power_up_sprite"]
            pu_frames = LEVELS[pu_level]["power_up_frames"]
            pu_sheet = assets.get_spritesheet(pu_name, pu_frames, 100)
            self.power_up = PowerUp(pu_sheet, self.cfg["power_up_type"])
            self.power_up.randomize_position()
            self.can_draw_powerup = True
            self.power_up_cooldown = POWERUP_COOLDOWN

        # Animate power-up
        if self.can_draw_powerup:
            self.power_up.update_animation(dt * 1000)

        # Collision with ball
        self.ball.sync_rect()
        self.power_up.sync_rect()

        if self.power_up.visible and self.ball.rect.colliderect(self.power_up.rect):
            assets.play_sfx("powerUp.ogg")
            self.power_up.deactivate()
            self.can_draw_powerup = False

            outcome = resolve_powerup_collision(
                level_index=level,
                lives_player=self.lives_player,
                lives_enemy=self.lives_enemy,
                vel_x=self.vel_x,
                vel_y=self.vel_y,
                power_up_active=self.power_up_active,
                power_up_activity_timer=self.power_up_activity_timer,
                is_frozen=self.is_frozen,
                freeze_timer=self.freeze_timer,
                enemy_pad_position=(self.enemy_pad.x, self.enemy_pad.y),
                max_lives=MAX_LIVES,
                activity_base=POWERUP_ACTIVITY_BASE,
                freeze_duration=KING_PONG_HOLD_TIME,
            )
            self.lives_player = outcome.lives_player
            self.lives_enemy = outcome.lives_enemy
            self.vel_x = outcome.vel_x
            self.vel_y = outcome.vel_y
            self.power_up_active = outcome.power_up_active
            self.power_up_activity_timer = outcome.power_up_activity_timer
            self.is_frozen = outcome.is_frozen
            self.freeze_timer = outcome.freeze_timer
            self.frozen_pos = outcome.frozen_pos

        # Speed power-up (Ronaldinho level)
        self.power_up_active, self.power_up_activity_timer, self.vel_player = update_speed_powerup(
            level_index=level,
            power_up_active=self.power_up_active,
            power_up_activity_timer=self.power_up_activity_timer,
            current_player_speed=self.vel_player,
            dt=dt,
            tick_speed=POWERUP_TICK_SPEED,
            base_player_speed=PLAYER_SPEED,
            boosted_player_speed=400,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _update_helpers(self, dt):
        level = self.level_index
        char_h = self.player_anim.height

        # Enemy helper (Dr. Rippon - level 1)
        if self.enemy_helper and level == 1:
            self.enemy_helper.update_animation(dt * 1000)
            threshold = self.cfg["enemy_helper_track_threshold"]
            track_speed = self.cfg["enemy_helper_track_speed"]
            helper = self.enemy_helper

            if self.vel_x < threshold:
                # Track ball
                mid_h = helper.y + helper.height / 2
                mid_b = self.ball.y + self.ball.height / 2
                if mid_h < mid_b:
                    helper.y += track_speed * dt
                elif mid_h > mid_b:
                    helper.y -= track_speed * dt
            else:
                # Patrol
                helper.y += helper.speed * helper.patrol_direction * dt
                if helper.y <= char_h:
                    helper.patrol_direction = 1
                    helper.y = char_h
                if helper.y + helper.height >= SCREEN_HEIGHT:
                    helper.patrol_direction = -1
                    helper.y = SCREEN_HEIGHT - helper.height

            # Helper-ball collision
            helper.sync_rect()
            self.ball.sync_rect()
            if self.ball.rect.colliderect(helper.rect):
                self.game.assets.play_sfx("paddle_sound.ogg")
                bx = self.ball.x
                by = self.ball.y
                bw = self.ball.width
                bh = self.ball.height
                hx = helper.x
                hy = helper.y
                hw = helper.width
                hh = helper.height
                if abs(bx - (hx + hw)) < 20:
                    self.vel_x *= -1
                    self.ball.x = hx + hw
                elif abs(by + bh - hy) < 20 and self.vel_y > 0:
                    self.vel_y *= -1
                    self.ball.y = hy - bh
                elif abs(by - (hy + hh)) < 20 and self.vel_y < 0:
                    self.vel_y *= -1
                    self.ball.y = hy + hh

        # Player helper (Cinos - level 2, only when power-up active)
        if self.player_helper and level == 2 and self.power_up_active:
            self.power_up_activity_timer -= POWERUP_TICK_SPEED * dt
            helper = self.player_helper
            helper.update_animation(dt * 1000)

            if self.power_up_activity_timer > 0:
                threshold = self.cfg["player_helper_track_threshold"]
                track_speed = self.cfg["player_helper_track_speed"]

                if self.vel_x > threshold:
                    mid_h = helper.y + helper.height / 2
                    mid_b = self.ball.y + self.ball.height / 2
                    if mid_h < mid_b:
                        helper.y += track_speed * dt
                    elif mid_h > mid_b:
                        helper.y -= track_speed * dt
                else:
                    helper.y += helper.speed * helper.patrol_direction * dt
                    if helper.y <= HELPER_PATROL_MIN_Y:
                        helper.patrol_direction = 1
                        helper.y = HELPER_PATROL_MIN_Y
                    if helper.y + helper.height >= SCREEN_HEIGHT:
                        helper.patrol_direction = -1
                        helper.y = SCREEN_HEIGHT - helper.height

                # Helper-ball collision
                helper.sync_rect()
                self.ball.sync_rect()
                if self.ball.rect.colliderect(helper.rect):
                    self.game.assets.play_sfx("paddle_sound.ogg")
                    bx, by = self.ball.x, self.ball.y
                    bw, bh = self.ball.width, self.ball.height
                    hx, hy = helper.x, helper.y
                    hw, hh = helper.width, helper.height
                    if abs(bx + bw - hx) < 20:
                        self.vel_x *= -1
                        self.ball.x = hx - bw
                    elif abs(by + bh - hy) < 20 and self.vel_y > 0:
                        self.vel_y *= -1
                        self.ball.y = hy - bh
                    elif abs(by - (hy + hh)) < 20 and self.vel_y < 0:
                        self.vel_y *= -1
                        self.ball.y = hy + hh
            else:
                self.power_up_active = False

    # ------------------------------------------------------------------
    # Level-specific mechanics
    # ------------------------------------------------------------------
    def _update_level_mechanics(self, dt):
        level = self.level_index

        # Ronaldinho random "ole" deflection
        if level == 3 and self.cfg["has_ole"]:
            if random.randint(0, 200) == RONALDINHO_OLE_CHANCE and self.vel_x > 0:
                self.game.assets.play_sfx("paddle_sound.ogg")
                self.vel_y *= RONALDINHO_OLE_VEL_Y_MULT
                self.vel_x *= RONALDINHO_OLE_VEL_X_MULT

        # Bulk hold mechanic
        if level == 4 and self.cfg["has_hold"]:
            self.enemy_pad.sync_rect()
            self.ball.sync_rect()
            if (self.ball.rect.colliderect(self.enemy_pad.rect)
                    and random.randint(0, 10) == BULK_HOLD_CHANCE):
                if not self.is_holding:
                    self.hold_timer = BULK_HOLD_TIME
                self.is_holding = True
                self.bulk_throw_dir = random.choice([-1, 1])
                self.thrown = True

            if self.is_holding:
                self.momentum_dir_enemy = 0
                self.ball.x = self.enemy_pad.x + 50
                self.ball.y = (self.enemy_pad.y + self.enemy_pad.height / 2
                               - self.ball.height / 2)
                self.vel_x -= 100 * dt
                self.vel_y *= self.bulk_throw_dir

                self.hold_timer -= POWERUP_TICK_SPEED * dt
                if self.hold_timer <= 0:
                    self.is_holding = False

            if self.thrown and self.ball.rect.colliderect(self.player_pad.rect):
                self.vel_x /= 1.3
                self.vel_y /= 1.3
                self.thrown = False
                self.is_slow = True
                self.slow_timer = BULK_SLOW_TIME

            if self.is_slow:
                self.slow_timer -= POWERUP_TICK_SPEED * dt
                self.vel_player = BULK_SLOW_SPEED
                self.momentum_player = 0
                if self.slow_timer <= 0:
                    self.is_slow = False
                    self.vel_player = PLAYER_SPEED

        # King Pong freeze (only when num_hits == 2)
        if level == 5 and self.num_hits == 2:
            if self.is_frozen:
                self.enemy_pad.x = self.frozen_pos[0]
                self.enemy_pad.y = self.frozen_pos[1]
                self.freeze_timer -= POWERUP_TICK_SPEED * dt
                if self.freeze_timer <= 0:
                    self.is_frozen = False
