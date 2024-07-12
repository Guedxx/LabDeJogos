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
    

def game_over(project_directory:str,janela:Window, teclado:Keyboard, mouse:Mouse):
    
    Torre = GameImage(os.path.join(project_directory, "Sprites", "ANIMATIONGameOver.png"))
    Torre.set_position(2,0)
    FallMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverChar.png"), 8)
    FallMan.set_sequence_time(0,8,50)
    FallMan.set_position(750, 100)
    
    SleepyMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverEepy.png"), 6)
    SleepyMan.set_sequence_time(0,6,300)
    SleepyMan.set_position(540, 579)
    SleepyMan.hide()
    
    WalkingMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverWalking.png"),4)
    WalkingMan.set_sequence_time(0,4,150)
    WalkingMan.hide()
    WalkingMan.set_position(540, 578)
    TentouAgain = False
    
    GameOver = Sprite(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverText.png"))
    Yes = Sprite(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverTextYes.png"))
    No =  Sprite(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverTextNo.png"))
    
    explosion = Sound(os.path.join(project_directory, "Sounds", "ANIMATIONexplosion.ogg"))
    explosion.play()
    
    
    #Animation
    contador_quicadas = 0
    fallAcel = 1200
    fallAceltorre = 800
    jogadaAcel = 400
    while True:
        
        
        
        Torre.draw()
        FallMan.draw()
        FallMan.update()
        SleepyMan.draw()
        
        
        #Desce a imagem de fundo
        if(Torre.y >= -765):
            Torre.y -= fallAceltorre * janela.delta_time()
            fallAceltorre += 100 * janela.delta_time()
        if(Torre.y <= -765):
            Torre.y = -765

        #Joga boneco para o lado 
        if(FallMan.x >= 540):
            FallMan.x -= (200 + jogadaAcel)* janela.delta_time()
            jogadaAcel -= 100 * janela.delta_time()
        
        #Cuida da aceleraçao do boneco quando a torre para de descer
        if(Torre.y <= -765 and FallMan.y < 570):
            FallMan.y += fallAcel * janela.delta_time()
            fallAcel += 400 * janela.delta_time()    
            
        if Torre.y <= -765 and FallMan.y >= 570 and contador_quicadas <= 5:
            FallMan.y += fallAcel * janela.delta_time()
            
            if FallMan.y > 570: #Bateu no chão
                
                hitSound = Sound(os.path.join(project_directory, "Sounds", "ANIMATIONHurt.ogg"))
                hitSound.play()
                
                TempX = FallMan.x
                TempY = FallMan.y
                
                FallMan = Animation(os.path.join(project_directory, "Sprites", "ANIMATIONGameOverChar.png"), 8)
                FallMan.set_sequence_time(0,8,50 * contador_quicadas)
                FallMan.set_position(TempX, TempY)
                
                contador_quicadas += 1
                
                FallMan.hide()
                SleepyMan.unhide()
                FallMan.y = 570
                fallAcel *= -1
                fallAcel /= 2
                fallAcel += 20
                   
            else:
                FallMan.unhide()
                SleepyMan.hide()
        
                 
        #Parou de quicar
        if contador_quicadas >= 5:
            SleepyMan.unhide()
            GameOver.draw()

            # Desistir
            if mouse.is_over_area([192, 333], [355, 391]):
                Yes.draw()
                
                if mouse.is_button_pressed(1):
                    mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                    mouse_click.play()
                    return 0
            
            # Tentar de novo
            if mouse.is_over_area([457, 333], [548, 391]):
                No.draw()
                if mouse.is_button_pressed(1):
                    mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                    mouse_click.play()
                    SleepyMan.x = -100
                    GameOver.hide()
                    Yes.hide()
                    No.hide()
                    WalkingMan.unhide()
                    TentouAgain = True

        if TentouAgain == True:
            WalkingMan.x += 200 * janela.delta_time()
            if WalkingMan.x >= 1100:
                return 1
                
            
            
            
        WalkingMan.draw()
        WalkingMan.update()
        SleepyMan.update()
        janela.update()
    
def zerou(project_directory:str,janela:Window,teclado:Keyboard, mouse:Mouse ):
    pass  