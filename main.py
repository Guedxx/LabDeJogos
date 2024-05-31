# O seguinte código apresenta o corpo principal do jogo "King Pong"
# feito para o projeto de Laboratório de Jogos.


from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.sound import *
import os

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
    tittleScreen_1 = GameImage(os.path.join(project_directory, "Sprites", "INIT_aGameLabProject.png"))
    #Tela "Made By"
    tittleScreen_2 = GameImage(os.path.join(project_directory, "Sprites", "INIT_madeBy.png"))

    while True:

        #CountDown da priemira tela
        time = 15
        while time > 0:
            if teclado.key_pressed("SPACE"):
                break
            time -= 10 * janela.delta_time()
            tittleScreen_1.draw()
            janela.update()

        #CountDown da segunda tela
        time = 15
        while time > 0:
            if teclado.key_pressed("SPACE"):
                break
            time -= 10 * janela.delta_time()
            tittleScreen_2.draw()
            janela.update()

        menu() #Inicia o Menu

# Menu Principal
def menu():

    # Inicializa Imagens usadas no Menu
    # Imagem que aparece junto com o "Press Space to Begin"
    Fundo = GameImage(os.path.join(project_directory, "Sprites", "MENU_menuInitScreen.png"))

    # Imagem conjunta do botão "Play", "Diff" e "Quit"
    Menus = GameImage(os.path.join(project_directory, "Sprites", "MENU_menuSelector.png"))

    # Imagem do pixel de seleção do menu principal
    Indicador = GameImage(os.path.join(project_directory, "Sprites", "MENU_Indicador.png"))

    #Bonequinho Animado :D
    lil_man = Animation((os.path.join(project_directory, "Sprites", "MENU_Char.png")), 2)
    lil_man.set_position(220, 420)
    lil_man.set_sequence_time(0,1,1000)
    lil_man.play()
    
    #Musica que toca
    menu_music = Sound(os.path.join(project_directory, "Sounds", "menu.ogg"))
    menu_music.play()



    while True:     # Mini Loop que pede para o jogador apertar espaço
        
        if teclado.key_pressed("SPACE"):
            break

        Fundo.draw()
        lil_man.draw()

        lil_man.update()
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
                menu_music.pause()
                play()
                
        if mouse.is_over_area([455, 380], [760, 440]):          #Botão de Dificuldades
            Indicador.set_position(400, 400)
            Indicador.draw()
            if mouse.is_button_pressed(1):
                menu_music.pause()
                dificuldades()
                
        if mouse.is_over_area([455, 480], [760, 540]):          #Botão de Sair
            Indicador.set_position(400, 500)
            Indicador.draw()

            if mouse.is_button_pressed(1):
                menu_music.pause()
                janela.close()



        
        janela.update()

def play():
    
    # Início da gameplay
    backgnd = GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png"))
    hotbar = GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png"))
    

    # Animação do player
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)

    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png")) # TODO Criar Sprite do PAD
    player_pad.set_position(Screen_W -  player_pad.width - 10, Screen_H/2 - player_pad.height/2)

    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)

    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    
    # Animação da Tutoriana
    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETTutoriana.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)

    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Tutoriana.png")) # TODO Criar Sprite do PAD
    tutoriana_pad .set_position(10, Screen_H/2 - tutoriana_pad.height/2)

    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)

    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    # Sprite da Orb
    Orb = Sprite(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)

    # Inicia as animações
    player.play()
    tutoriana.play()
    
    DashCoolDown = 30
    DashCoolDownPlayer = DashCoolDown
    DashCoolDownEnemy = DashCoolDown

    DashReload = 600
    DashReloadPlayer = DashReload
    DashReloadEnemy = DashReload
    DashNumberPlayer = 3
    DashNumberEnemy = 3
    FirstDashPlayer = False
    FirstDashEnemy = False

    Momentum_player = 0
    MomentumDirection_player = 0

    while True:
        # Desenhar Sprites e GameImages
        backgnd.draw()
        hotbar.draw()
        Orb.draw()

        player_hearts.draw()
        player_dash.draw()
        player_pad.draw()
        player.draw()

        tutoriana_hearts.draw()
        tutoriana_dash.draw()
        tutoriana_pad.draw()
        tutoriana.draw()


        #Codigo referente ao player

        #Contadores Dash
        DashCoolDownPlayer-= 1
        if FirstDashPlayer == True:
            DashReloadPlayer -= 1
        if DashNumberPlayer == 3:
            FirstDashPlayer = False

        if DashReloadPlayer <= 0 and DashNumberPlayer < 3:
            DashNumberPlayer += 1
            DashReloadPlayer  = DashReload
            player_dash.x -= 80

        #Momentum_player Calculations
        if Momentum_player >= 0:
            Momentum_player -= 75 * janela.delta_time()
            if Momentum_player < 0:
                Momentum_player = 0

        if MomentumDirection_player == 1:
            player_pad.y -= Momentum_player * janela.delta_time()
        elif MomentumDirection_player == -1:
            player_pad.y += Momentum_player * janela.delta_time()
            
        #Movements
        if teclado.key_pressed("W"):

            player_pad.y -= (200 * janela.delta_time()) + (Momentum_player * janela.delta_time())

            if Momentum_player < 100 and player_pad.y > player.height:
                Momentum_player += 100 * janela.delta_time()
            MomentumDirection_player = 1

            #Da um Dash
            if teclado.key_pressed("SPACE") and DashCoolDownPlayer < 0 and DashNumberPlayer > 0: 
                FirstDashPlayer = True
                player_pad.y -= (100 * janela.delta_time())
                Momentum_player += 5000* janela.delta_time()
                player_dash.x += 80 #Move o contador de dashs para subtrair uma barrinha 
                DashCoolDownPlayer = DashCoolDown
                DashNumberPlayer -= 1


        #Tudo que o de cima faz mas condireando a descida
        elif teclado.key_pressed("S"):

            player_pad.y += (200 * janela.delta_time()) + Momentum_player * janela.delta_time()

            if Momentum_player < 100  and player_pad.y + player_pad.height < Screen_H :
                Momentum_player += 100 * janela.delta_time()
            MomentumDirection_player = -1

            if teclado.key_pressed("SPACE") and DashCoolDownPlayer < 0 and DashNumberPlayer > 0:
                FirstDashPlayer = True
                player_pad.y += (1000 * janela.delta_time())
                Momentum_player += 5000* janela.delta_time()
                player_dash.x += 80 
                DashCoolDownPlayer = DashCoolDown
                DashNumberPlayer -= 1
        

        #Colide Walls Check
        if player_pad.y < player.height:
            player_pad.y = player.height 
            MomentumDirection_player = -1
            if Momentum_player < 100:
                Momentum_player += Momentum_player * janela.delta_time()

        elif player_pad.y + player_pad.height > Screen_H:
            player_pad.y = Screen_H - player_pad.height
            MomentumDirection_player = 1 
            if Momentum_player < 100:
                Momentum_player += Momentum_player * janela.delta_time()

        #Update das Animations
        player.update()
        tutoriana.update()
        janela.update()
        
        

def dificuldades():
    raise NotImplementedError

def ranking():
    raise NotImplementedError


gameINIT()

print("Fechou")