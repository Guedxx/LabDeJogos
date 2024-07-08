from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.sound import *
import os
import random
from setup import *
from ingame import *


def passou_fase(project_directory,janela, N_Fase):

    
    Torre = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONTower.png"))
    PlayerHead = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONPlayerHead.png"))
    Enemy_Felled = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONEnemyFelled.png"),3)
    Enemy_Felled.set_sequence_time(0,2,500)
    Enemy_Felled.play()

    if N_Fase == 0:
        Torre.set_position(0, -720)
        PlayerHead.set_position(850, 555)
        nivel_a_chegar = 360
        nivel_a_chegar_torre = -720

    if N_Fase == 1:
        Torre.set_position(0, -720)
        PlayerHead.set_position(850, 360)
        nivel_a_chegar = 165
        nivel_a_chegar_torre = -720
    
    if N_Fase == 2:
        Torre.set_position(0, -720)
        PlayerHead.set_position(850, 165)
        nivel_a_chegar = 170
        nivel_a_chegar_torre = -510
    
    if N_Fase == 3:
        Torre.set_position(0, -510)
        PlayerHead.set_position(850, 165)
        nivel_a_chegar = 170
        nivel_a_chegar_torre = -320
    
    if N_Fase == 4:
        Torre.set_position(0, -320)
        PlayerHead.set_position(850, 165)
        nivel_a_chegar = 170
        nivel_a_chegar_torre = -0


    #ENEMMY FELLEDDD!!!!!!!!!
    time = 20
    while time >= 0:
        Enemy_Felled.draw()
        Enemy_Felled.update()
        janela.update()
        time -= 10 * janela.delta_time()


    aceleration = 100
    while True:

        if aceleration >= 0:
            aceleration -= 10 * janela.delta_time()
        if PlayerHead.y > nivel_a_chegar:
            PlayerHead.y -= (10 + aceleration)* janela.delta_time()
        if Torre.y < nivel_a_chegar_torre:
            Torre.y += (10 + aceleration) *janela.delta_time()
        


        Torre.draw()
        PlayerHead.draw()
        janela.update()
        