from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
import os

project_directory = os.path.dirname(__file__)

# Janelas
Screen_H, Screen_W = 720, 1280
janela = Window(Screen_W,Screen_H)
janela.set_title('King Pong')




# Mouse e Teclado
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

#Dificuldade
dificuldade = 0

#Telas Iniciais do Game
def gameINIT():
    #Tela "A Game Lab Project"
    image_path_GLP = os.path.join(project_directory, "Sprites", "aGameLabProject.png")
    tittleScreen_1 = GameImage(image_path_GLP)

    #Tela "Made By"
    image_path_MB = os.path.join(project_directory, "Sprites", "madeBy.png")
    tittleScreen_2 = GameImage(image_path_MB)

    while True:

        #Loop da priemira tela
        time = 15
        while time > 0:
            time -= 10 * janela.delta_time()
            tittleScreen_1.draw()
            janela.update()

        #Loop da Segunda tela
        time = 15
        while time > 0:
            time -= 10 * janela.delta_time()
            tittleScreen_2.draw()
            janela.update()

        #Inicia o Menu
        menu()

def menu():

    #Inicializa Imagens usadas no Menu

    image_path_fundo = os.path.join(project_directory, "Sprites", "menuScreen.png")
    Fundo = GameImage(image_path_fundo)

    image_path_Menus = os.path.join(project_directory, "Sprites", "menuSelector.png")
    Menus = GameImage(image_path_Menus)
    
    image_path_Indicador = os.path.join(project_directory, "Sprites", "Indicador.png")
    Indicador = GameImage(image_path_Indicador)



    Started = False


    while True:

        while Started == False:

            Fundo.draw()
            janela.draw_text(text="- Press Space to Begin -", x= Screen_W/2 + 200,
                              y= Screen_H/2 + 100, size= 30, color=(255,255,255), font_name="Arial")
            if teclado.key_pressed("SPACE"):
                Started = True

            janela.update()


        janela.set_background_color([0,0,0])
        Menus.draw()


        #As seguintes linhas são em relação aos clicks do mouse 
        
                #Botão de Play
        if mouse.is_over_area([455, 280], [760, 340]):
            Indicador.set_position(400, 300)
            Indicador.draw()
            
            if mouse.is_button_pressed(1):
                play()
            
                #Botão de Dificuldades
        if mouse.is_over_area([455, 380], [760, 440]):
            Indicador.set_position(400, 400)
            Indicador.draw()
            
            if mouse.is_button_pressed(1):
                dificuldades()
            

                #Botão de Sair
        if mouse.is_over_area([455, 480], [760, 540]):
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