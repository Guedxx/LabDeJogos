# O seguinte código apresenta o corpo principal do jogo "King Pong"
# feito para o projeto de Laboratório de Jogos.


from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
import os
from time import sleep

#Cria o diretório do arquivo principal. Garante compatibilidade com MAC e LINUX
project_directory = os.path.dirname(__file__)

# Informações e Criação da Janela
Screen_H, Screen_W = 720, 1280
janela = Window(Screen_W,Screen_H)
janela.set_title('King Pong')


# Mouse e Teclado
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

#Dificuldade (no shit)
dificuldade = 0



#Telas Iniciais do Game
def gameINIT():

    #Tela "A Game Lab Project"
    tittleScreen_1 = GameImage(os.path.join(project_directory, "Sprites", "aGameLabProject.png"))

    #Tela "Made By"
    tittleScreen_2 = GameImage(os.path.join(project_directory, "Sprites", "madeBy.png"))

    while True:

        #LCountDown da priemira tela
        time = 15
        while time > 0:
            time -= 10 * janela.delta_time()
            tittleScreen_1.draw()
            janela.update()

        #CountDown da segunda tela
        time = 15
        while time > 0:
            time -= 10 * janela.delta_time()
            tittleScreen_2.draw()
            janela.update()

        
        menu()                          #Inicia o Menu

# Menu Principal
def menu():

    # Inicializa Imagens usadas no Menu

    # Imagem que aparece junto com o "Press Space to Begin"
    Fundo = GameImage(os.path.join(project_directory, "Sprites", "menuScreen.png"))

    # Imagem conjunta do botão "Play", "Diff" e "Quit"
    Menus = GameImage(os.path.join(project_directory, "Sprites", "menuSelector.png"))

    # Imagem do pixel de seleção do menu principal
    Indicador = GameImage(os.path.join(project_directory, "Sprites", "Indicador.png"))


    while True:     # Mini Loop que pede para o jogador apertar espaço

        Fundo.draw()

        janela.draw_text(text="- Press Space to Begin -", x= Screen_W/2 + 200,
            y= Screen_H/2 + 100, size= 30, color=(255,255,255), font_name="Arial")
        
        if teclado.key_pressed("SPACE"):
            break

        janela.update()

    while True:

        #Começo do Loop do Menu 
        janela.set_background_color([0,0,0]) 
        Menus.draw()


        #As seguintes linhas são em relação aos clicks do mouse 
                
        if mouse.is_over_area([455, 280], [760, 340]):          #Botão de Play
            Indicador.set_position(400, 300)
            Indicador.draw()
            if mouse.is_button_pressed(1):
                play()
                
        if mouse.is_over_area([455, 380], [760, 440]):          #Botão de Dificuldades
            Indicador.set_position(400, 400)
            Indicador.draw()
            if mouse.is_button_pressed(1):
                dificuldades()
                
        if mouse.is_over_area([455, 480], [760, 540]):          #Botão de Sair
            Indicador.set_position(400, 500)
            Indicador.draw()

            if mouse.is_button_pressed(1):
                janela.close()



        
        janela.update()

def play():

    print('nada')
        

def dificuldades():
    print("nada")

def ranking():
    print("nada")



print(os.getcwd())
gameINIT()