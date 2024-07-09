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



def confirmExit(project_directory,janela, teclado, mouse):
    AreYouSure = GameImage(os.path.join(project_directory, "Sprites", "PAUSEsure.png"))
    Yes = GameImage(os.path.join(project_directory, "Sprites", "PAUSEsureYes.png"))
    No = GameImage(os.path.join(project_directory, "Sprites", "PAUSEsureNo.png"))
    
    while True:
        AreYouSure.draw()
        
        if mouse.is_over_area([734, 472], [852, 532]): # Botao NO
            No.draw()
            
            if mouse.is_button_pressed(1):
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                return 0
            
        if mouse.is_over_area([387, 472], [561, 532]): # Botao Yes
            Yes.draw()
            
            if mouse.is_button_pressed(1):
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                return 1

        
        janela.update()




def pause(project_directory ,janela,teclado, mouse):
    
    Pause = GameImage(os.path.join(project_directory, "Sprites", "PAUSEneutro.png"))
    Return = GameImage(os.path.join(project_directory, "Sprites", "PAUSEreturn.png"))
    Menu = GameImage(os.path.join(project_directory, "Sprites", "PAUSEmenu.png"))
    Quit = GameImage(os.path.join(project_directory, "Sprites", "PAUSEquit.png"))
    
    
    while True:
        Pause.draw()
        
        if mouse.is_over_area([490, 275], [800, 340]): # Botao return
            Return.draw()
            
            if mouse.is_button_pressed(1):
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
            
                return 
        
        if mouse.is_over_area([523, 408], [753, 470]): # Botao menu
            Menu.draw()
            
            if mouse.is_button_pressed(1):
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                saida = confirmExit(project_directory,janela,teclado,mouse)
                if saida == 1:
                    menu(project_directory, janela, teclado, mouse)
                
        
        
        if mouse.is_over_area([530, 530], [740, 580]): # Botao quit
            Quit.draw()
            
            if mouse.is_button_pressed(1):
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                saida = confirmExit(project_directory,janela,teclado,mouse)
                if saida == 1:
                        exit()
            
    
        janela.update()