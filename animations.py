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


def passou_fase(project_directory:str,janela:Window, N_Fase:int) -> None:

    
    Torre = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONTower.png"))
    PlayerHead = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONPlayerHead.png"))
    Enemy_Felled = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONEnemyFelled.png"),3)
    Fundo = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONEnemyFelled.png"),3)
    Fundo.set_sequence_time(1,1,50000)
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
    time = 30
    while time > 0:

        if aceleration >= 0:
            aceleration -= 10 * janela.delta_time()
        if PlayerHead.y > nivel_a_chegar:
            PlayerHead.y -= (10 + aceleration)* janela.delta_time()
        if Torre.y < nivel_a_chegar_torre:
            Torre.y += (10 + aceleration) *janela.delta_time()
        time -= 10*janela.delta_time()

        Fundo.draw()
        Torre.draw()
        PlayerHead.draw()
        janela.update()
    return
    

    
        
def game_over(project_directory,janela):
    
    Torre = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONGameOver.png"))
    FallMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverChar.png"), 8)
    FallMan.set_sequence_time(0,8,200)
    FallMan.set_position(750, 100)
    
    SleepyMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverEepy.png"), 6)
    SleepyMan.set_sequence_time(0,6,300)
    SleepyMan.set_position(540, 550)
    
    
    #Animation
    fallAcel = 1200
    fallAceltorre = 800
    jogadaAcel = 400
    while True:

        SleepyMan.hide()
        
        #Desce a imagem de fundo
        if(Torre.y >= -720):
            Torre.y -= fallAceltorre * janela.delta_time()
            fallAceltorre += 100 * janela.delta_time()

        #Joga boneco para o lado 
        if(FallMan.x >= 540):
            FallMan.x -= (200 + jogadaAcel)* janela.delta_time()
        
        #Cuida da aceleraçao do boneco quando a torre para de descer
        if(Torre.y <= -720 and FallMan.y < 585):
            FallMan.y += fallAcel * janela.delta_time()
            fallAcel += 400 * janela.delta_time()    
            
        if (Torre.y <= -720 and FallMan.y >= 585):
            FallMan.y += fallAcel * janela.delta_time()
            
            if FallMan.y > 585:
                FallMan.hide()
                SleepyMan.unhide()
                FallMan.y = 590
                fallAcel *= -1
                fallAcel /= 2
                fallAcel += 20
            else:
                FallMan.unhide()
                SleepyMan.hide()
                

            
    
            
    
        
        Torre.draw()
        FallMan.draw()
        FallMan.update()
        SleepyMan.draw()
        SleepyMan.update()
        janela.update()
    
    