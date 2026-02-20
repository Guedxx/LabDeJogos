"""All game constants and level configurations."""

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "King Pong"

# Physics
BALL_BASE_SPEED_X = 300
BALL_BASE_SPEED_Y = 300
BALL_SPEED_CAP = 1000
BALL_SPEED_ACCEL_X = 10
BALL_SPEED_ACCEL_Y = 5
BALL_CRUISE_SPEED = 550

PLAYER_SPEED = 200

# Dash
DASH_COOLDOWN = 30
DASH_RELOAD = 600
MAX_DASHES = 3
DASH_MOMENTUM_BOOST = 5000
DASH_MOVE_BOOST_UP = 100
DASH_MOVE_BOOST_DOWN = 1000
DASH_VEL_MULT_X = 1.3
DASH_VEL_MULT_Y = 1.5

# Momentum
MOMENTUM_DECAY = 75
MOMENTUM_CAP = 100
MOMENTUM_GAIN_PLAYER = 100

# Lives
MAX_LIVES = 3

# HUD
HEART_SEGMENT_WIDTH = 80
DASH_SEGMENT_WIDTH = 80
PLAYER_HEARTS_POS = (890, 20)
PLAYER_DASH_POS = (890, 90)
ENEMY_HEARTS_POS = (160, 20)
ENEMY_DASH_POS = (160, 90)

# Power-ups
POWERUP_COOLDOWN = 600
POWERUP_SPAWN_CHANCE = 1  # out of 100
POWERUP_ACTIVITY_BASE = 600
POWERUP_X_RANGE = (40, 1200)
POWERUP_Y_RANGE = (150, 630)

# Bulk hold mechanic
BULK_HOLD_TIME = 200
BULK_SLOW_TIME = 300
BULK_SLOW_SPEED = 100
BULK_HOLD_CHANCE = 1  # out of 10

# King Pong hold mechanic
KING_PONG_HOLD_TIME = 300

# Ronaldinho random deflection
RONALDINHO_OLE_CHANCE = 1  # out of 200
RONALDINHO_OLE_VEL_Y_MULT = -1.2
RONALDINHO_OLE_VEL_X_MULT = 1.3

# Splash screen timing
SPLASH_DURATION = 15
SPLASH_SPEED = 10

# Menu
MENU_SIDEBAR_INITIAL_X = -780
MENU_SIDEBAR_DECEL = 40
MENU_SIDEBAR_SPEED = 700
DIFFICULTY_COOLDOWN = 30

# Menu button areas (top-left, bottom-right)
MENU_PLAY_AREA = ((95, 380), (250, 412))
MENU_DIFF_AREA = ((95, 470), (280, 500))
MENU_QUIT_AREA = ((95, 550), (222, 577))

# Pause button areas
PAUSE_RETURN_AREA = ((490, 275), (800, 340))
PAUSE_MENU_AREA = ((523, 408), (753, 470))
PAUSE_QUIT_AREA = ((530, 530), (740, 580))

# Confirm dialog areas
CONFIRM_YES_AREA = ((387, 472), (561, 532))
CONFIRM_NO_AREA = ((734, 472), (852, 532))

# Game over button areas
GAMEOVER_QUIT_AREA = ((192, 333), (355, 391))
GAMEOVER_RETRY_AREA = ((457, 333), (548, 391))

# Game over animation
GAMEOVER_FALL_ACCEL = 1200
GAMEOVER_TOWER_ACCEL = 800
GAMEOVER_LATERAL_ACCEL = 400
GAMEOVER_BOUNCE_COUNT = 5
GAMEOVER_TOWER_Y_STOP = -765
GAMEOVER_FLOOR_Y = 570
GAMEOVER_WALKING_SPEED = 200
GAMEOVER_WALKING_EXIT_X = 1100

# Level clear tower positions
LEVEL_CLEAR_DATA = [
    {"tower_y": -720, "head_x": 850, "head_y": 555, "target_head_y": 360, "target_tower_y": -720},
    {"tower_y": -720, "head_x": 850, "head_y": 360, "target_head_y": 165, "target_tower_y": -720},
    {"tower_y": -720, "head_x": 850, "head_y": 165, "target_head_y": 170, "target_tower_y": -510},
    {"tower_y": -510, "head_x": 850, "head_y": 165, "target_head_y": 170, "target_tower_y": -320},
    {"tower_y": -320, "head_x": 850, "head_y": 165, "target_head_y": 170, "target_tower_y": 0},
]

# Credits scroll speed
CREDITS_SCROLL_SPEED = 100
CREDITS_END_Y = -720
ENDGAME_DISPLAY_TIME = 100

# Delay react tick speed
DELAY_REACT_TICK_SPEED = 1500

# AI Reaction delay countdown
POWERUP_TICK_SPEED = 100

# Level configurations (data-driven, replaces setupF1-F6)
LEVELS = [
    {
        "name": "Tutoriana",
        "enemy_sheet": "SHEETTutoriana.png",
        "enemy_frames": 18,
        "enemy_frame_duration": 100,
        "enemy_pad": "PAD_Tutoriana.png",
        "enemy_pad_animated": False,
        "background": "LV1_background.png",
        "bg_frames": 1,
        "bg_frame_duration": 0,
        "bg_animated": False,
        "ai_speed": 210,
        "ai_momentum_gain": 100,
        "ai_delay": 200,
        "has_enemy_helper": False,
        "enemy_helper_sprite": None,
        "enemy_helper_frames": 1,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 0,
        "enemy_helper_track_threshold": 0,
        "enemy_helper_track_speed": 0,
        "has_player_helper": False,
        "player_helper_sprite": None,
        "player_helper_frames": 1,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 0,
        "player_helper_track_threshold": 0,
        "player_helper_track_speed": 0,
        "power_up_type": "enemy_heal",
        "power_up_sprite": "POWERUP_Health.png",
        "power_up_frames": 2,
        "enemy_can_dash": False,
        "has_hold": False,
        "has_ole": False,
        "aggression_scaling": False,
        "bulk_hold_sprite": None,
    },
    {
        "name": "Dr. Rippon",
        "enemy_sheet": "SHEETDrRippon.png",
        "enemy_frames": 18,
        "enemy_frame_duration": 100,
        "enemy_pad": "PAD_DrRippon.png",
        "enemy_pad_animated": False,
        "background": "LV2_background.png",
        "bg_frames": 1,
        "bg_frame_duration": 0,
        "bg_animated": False,
        "ai_speed": 225,
        "ai_momentum_gain": 100,
        "ai_delay": 150,
        "has_enemy_helper": True,
        "enemy_helper_sprite": "PAD_DrHelper.png",
        "enemy_helper_frames": 2,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 300,
        "enemy_helper_track_threshold": -500,
        "enemy_helper_track_speed": 400,
        "has_player_helper": False,
        "player_helper_sprite": None,
        "player_helper_frames": 1,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 0,
        "player_helper_track_threshold": 0,
        "player_helper_track_speed": 0,
        "power_up_type": "player_heal",
        "power_up_sprite": "POWERUP_PlaceHolder.png",
        "power_up_frames": 1,
        "enemy_can_dash": False,
        "has_hold": False,
        "has_ole": False,
        "aggression_scaling": False,
        "bulk_hold_sprite": None,
    },
    {
        "name": "Cinos",
        "enemy_sheet": "SHEETSanic.png",
        "enemy_frames": 6,
        "enemy_frame_duration": 100,
        "enemy_pad": "PAD_Cinos.png",
        "enemy_pad_animated": False,
        "background": "LV3_background.png",
        "bg_frames": 2,
        "bg_frame_duration": 500,
        "bg_animated": True,
        "ai_speed": 250,
        "ai_momentum_gain": 400,
        "ai_delay": 100,
        "has_enemy_helper": False,
        "enemy_helper_sprite": None,
        "enemy_helper_frames": 1,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 0,
        "enemy_helper_track_threshold": 0,
        "enemy_helper_track_speed": 0,
        "has_player_helper": True,
        "player_helper_sprite": "PAD_PlayerHelper.png",
        "player_helper_frames": 2,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 300,
        "player_helper_track_threshold": 600,
        "player_helper_track_speed": 300,
        "power_up_type": "player_helper",
        "power_up_sprite": "POWERUP_PlaceHolder.png",
        "power_up_frames": 1,
        "enemy_can_dash": False,
        "has_hold": False,
        "has_ole": False,
        "aggression_scaling": False,
        "bulk_hold_sprite": None,
    },
    {
        "name": "Ronaldinho",
        "enemy_sheet": "SHEETRonaldinhoBahiano.png",
        "enemy_frames": 18,
        "enemy_frame_duration": 100,
        "enemy_pad": "PAD_Ronaldinho.png",
        "enemy_pad_animated": False,
        "background": "LV4_background.png",
        "bg_frames": 2,
        "bg_frame_duration": 300,
        "bg_animated": True,
        "ai_speed": 250,
        "ai_momentum_gain": 100,
        "ai_delay": 50,
        "has_enemy_helper": False,
        "enemy_helper_sprite": None,
        "enemy_helper_frames": 1,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 0,
        "enemy_helper_track_threshold": 0,
        "enemy_helper_track_speed": 0,
        "has_player_helper": False,
        "player_helper_sprite": None,
        "player_helper_frames": 1,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 0,
        "player_helper_track_threshold": 0,
        "player_helper_track_speed": 0,
        "power_up_type": "reflect",
        "power_up_sprite": "POWERUP_PlaceHolder.png",
        "power_up_frames": 1,
        "enemy_can_dash": True,
        "has_hold": False,
        "has_ole": True,
        "aggression_scaling": False,
        "bulk_hold_sprite": None,
    },
    {
        "name": "Bulk",
        "enemy_sheet": "SHEETBulk.png",
        "enemy_frames": 19,
        "enemy_frame_duration": 100,
        "enemy_pad": "PAD_Bulk.png",
        "enemy_pad_animated": False,
        "background": "LV5_background.png",
        "bg_frames": 1,
        "bg_frame_duration": 0,
        "bg_animated": False,
        "ai_speed": 230,
        "ai_momentum_gain": 100,
        "ai_delay": 20,
        "has_enemy_helper": False,
        "enemy_helper_sprite": None,
        "enemy_helper_frames": 1,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 0,
        "enemy_helper_track_threshold": 0,
        "enemy_helper_track_speed": 0,
        "has_player_helper": False,
        "player_helper_sprite": None,
        "player_helper_frames": 1,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 0,
        "player_helper_track_threshold": 0,
        "player_helper_track_speed": 0,
        "power_up_type": "reflect",
        "power_up_sprite": "POWERUP_PlaceHolder.png",
        "power_up_frames": 1,
        "enemy_can_dash": False,
        "has_hold": True,
        "has_ole": False,
        "aggression_scaling": False,
        "bulk_hold_sprite": "PAD_BulkHold.png",
    },
    {
        "name": "King Pong",
        "enemy_sheet": "SHEETKingPong.png",
        "enemy_frames": 4,
        "enemy_frame_duration": 50,
        "enemy_pad": "PAD_KingPong.png",
        "enemy_pad_animated": True,
        "enemy_pad_frames": 4,
        "enemy_pad_frame_duration": 100,
        "background": "LV6_background.png",
        "bg_frames": 1,
        "bg_frame_duration": 0,
        "bg_animated": False,
        "ai_speed": 100,
        "ai_momentum_gain": 100,
        "ai_delay": 1,
        "has_enemy_helper": False,
        "enemy_helper_sprite": None,
        "enemy_helper_frames": 1,
        "enemy_helper_frame_duration": 100,
        "enemy_helper_speed": 0,
        "enemy_helper_track_threshold": 0,
        "enemy_helper_track_speed": 0,
        "has_player_helper": False,
        "player_helper_sprite": None,
        "player_helper_frames": 1,
        "player_helper_frame_duration": 100,
        "player_helper_speed": 0,
        "player_helper_track_threshold": 0,
        "player_helper_track_speed": 0,
        "power_up_type": "freeze",
        "power_up_sprite": "POWERUP_PlaceHolder.png",
        "power_up_frames": 1,
        "enemy_can_dash": False,
        "has_hold": False,
        "has_ole": False,
        "aggression_scaling": True,
        "aggression_table": {0: 100, 1: 200, 2: 400, 3: 2000},
        "bulk_hold_sprite": None,
    },
]

# Aggression scaling for King Pong (maps num_hits to aggression value)
KING_PONG_AGGRESSION = {0: 100, 1: 200, 2: 400, 3: 2000}

# Menu background animation durations
MENU_BG_DURATIONS = {"easy": 975, "normal": 765, "hard": 500}

# Orb animation
ORB_FRAMES = 8
ORB_FRAME_DURATION = 100

# Main character
MAIN_CHAR_FRAMES = 18
MAIN_CHAR_FRAME_DURATION = 100

# Player pad offset from right edge
PLAYER_PAD_OFFSET_X = 10
ENEMY_PAD_X = 10

# Helper patrol bounds
HELPER_PATROL_MIN_Y = 150
