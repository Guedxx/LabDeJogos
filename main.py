from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *

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
    tittleScreen_1 = GameImage("/home/guedes/Documents/VsCodeCodes/Python/Games/King Pong/Sprites/aGameLabProject.png")

    #Tela "Made By"
    tittleScreen_2 = GameImage("/home/guedes/Documents/VsCodeCodes/Python/Games/King Pong/Sprites/madeBy.png")

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

    Fundo = GameImage('/home/guedes/Documents/VsCodeCodes/Python/Games/King Pong/Sprites/menuScreen.png')
    Menus = GameImage('/home/guedes/Documents/VsCodeCodes/Python/Games/King Pong/Sprites/menuSelector.png')
    Indicador = GameImage('/home/guedes/Documents/VsCodeCodes/Python/Games/King Pong/Sprites/Indicador.png')
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

    if dificuldade == 0:
        SpeedNave = 275
        DelayTiro = 0.5

    

    nave = GameImage("/home/guedes/Documents/VsCodeCodes/Python/Games/Space-Invaders/Sprites/nave.png")
    nave.set_position(Screen_W / 2, Screen_H - nave.height - 10 )
    while True:

        #Pinta Janela
        janela.set_background_color([0, 0, 0])


        cooldown = DelayTiro
        cooldown -= 0.1 * janela.delta_time()
        tiros = []



        if teclado.key_pressed("space") and cooldown <= 0:
            tiro = Sprite("/home/guedes/Documents/VsCodeCodes/Python/Games/Space-Invaders/Sprites/tiro.png")
            tiro.set_position(nave.x + 24, nave.y)
            tiros.append(tiro)

            cooldown = DelayTiro

        
        for tiro in tiros:
            tiro.draw()
            tiro.x += 250 * janela.delta_time()

            if tiro.x < 0:
                del tiro



        #Movimentação Nave
        if teclado.key_pressed("D"):
            nave.x += SpeedNave * janela.delta_time()
        if teclado.key_pressed("A"):
            nave.x -= SpeedNave * janela.delta_time()
        if nave.x <= 0:
            nave.x = 0 
        if nave.x + nave.width >= Screen_W:
            nave.x = Screen_W - nave.width

        nave.draw()
        janela.update()
        


def dificuldades():
    print("nada")

def ranking():
    print("nada")




gameINIT()