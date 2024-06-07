from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.animation import *
import os

def setupF1(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)
    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETTutoriana.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Tutoriana.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)

    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)

    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)
    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb