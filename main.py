# O seguinte código apresenta o corpo principal do jogo "King Pong"
# feito para o projeto de Laboratório de Jogos.

from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.sound import *
import os
import random

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
    
    #Sons Usados
    sound_damage = Sound(os.path.join(project_directory, "Sounds", "hit_sound.ogg"))
    sound_hit_pad = Sound(os.path.join(project_directory, "Sounds", "paddle_sound.ogg"))
    sound_hit_wall = Sound(os.path.join(project_directory, "Sounds", "wall_sound.ogg"))


    # Animação do player
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)

    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)

    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)

    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    
    # Animação da Tutoriana
    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETTutoriana.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)

    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Tutoriana.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)

    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)

    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    # Sprite da Orb
    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    

    # Velocidade da orb
    velx_base = 100
    vely_base = 100
    velx = velx_base
    vely = vely_base

    # Inicia as animações
    player.play()
    tutoriana.play()
    Orb.play()
    
    #Infos Dashs
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
    Momentum_enemy = 0
    MomentumDirection_enemy = 0

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

        # Código da Orb

        #Colisão Paredes 
        if Orb.x + Orb.width >= Screen_W: # Ponto para Tutoriana
            sound_damage.play()
            Orb.x = Screen_W - Orb.width - 2
            player_hearts.x += 80 # -1 coração para o player
            velx /= 2
            vely /= 2

        if Orb.x <= 0: #Ponto Player
            sound_damage.play()
            Orb.x = 2
            tutoriana_hearts.x -= 80 # -1 coração para Tutoriana 
            velx /= 2
            vely /= 2

        if Orb.y >= Screen_H - Orb.height: #Parede de Baixo
            sound_hit_wall.play()
            Orb.y = Screen_H - Orb.height
            vely *= -1
        if Orb.y <= tutoriana.height: #Parede de Cima
            sound_hit_wall.play() 
            Orb.y = tutoriana.height
            vely *= -1
        
        #Colisão Pads
        if Orb.collided(player_pad):
            sound_hit_pad.play()
            if abs(Orb.x + Orb.width - player_pad.x) < 10:
                velx *= -1
                Orb.x = player_pad.x - Orb.width
            elif abs(Orb.y + Orb.height - player_pad.y) < 10 and vely > 0:
                vely *= -1 
            elif abs(Orb.y - (player_pad.y + player_pad.height)) < 10 and vely < 0:
                vely *= -1 

        if Orb.collided(tutoriana_pad):
            sound_hit_pad.play()
            if abs(Orb.x - (tutoriana_pad.x + tutoriana_pad.width)) < 10:
                velx *= -1
                Orb.x = tutoriana_pad.x + tutoriana_pad.width
            elif abs(Orb.y + Orb.height - tutoriana_pad.y) < 10 and vely > 0:
                vely *= -1 
            elif abs(Orb.y - (tutoriana_pad.y + tutoriana_pad.height)) < 10 and vely < 0:
                vely *= -1 
            
        #Movimentação
        Orb.x += velx * janela.delta_time()
        Orb.y += vely * janela.delta_time()

        #Aumento de velocidades
        if velx > 0:
            velx += 10 * janela.delta_time()
        else:
            velx -= 10 * janela.delta_time()
        
        if vely > 0:
            vely += 5 * janela.delta_time()
        else:
            vely -= 5 * janela.delta_time()

        vel_animation -= 200 * janela.delta_time()
        Orb.set_total_duration(vel_animation)

        #Codigo referente ao player --------

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



        #IA Tutoriana  v0.1

        #Momentum Tutoriana Calculations
        if Momentum_enemy >= 0:
            Momentum_enemy -= 75 * janela.delta_time()
            if Momentum_enemy < 0:
                Momentum_enemy = 0

        if MomentumDirection_enemy == 1:
            tutoriana_pad.y -= Momentum_enemy * janela.delta_time()
        elif MomentumDirection_enemy == -1:
            tutoriana_pad.y += Momentum_enemy * janela.delta_time()

        #Sobe em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 < Orb.y + Orb.height /2 and velx < 0:

            tutoriana_pad.y += (200 * janela.delta_time()) + (Momentum_enemy * janela.delta_time())

            MomentumDirection_enemy = -1

            if Momentum_enemy < 100 and tutoriana_pad.y > player.height:
                Momentum_enemy += 100 * janela.delta_time()
                

        #Desce em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 > Orb.y + Orb.height /2 and velx < 0:

            tutoriana_pad.y -= (200 * janela.delta_time()) + (Momentum_enemy * janela.delta_time())

            MomentumDirection_enemy = 1

            if Momentum_enemy < 100 and tutoriana_pad.y > player.height:
                Momentum_enemy += 100 * janela.delta_time()
        
        #Colide Walls
        if tutoriana_pad.y < player.height:
            tutoriana_pad.y = player.height
        if tutoriana_pad.y + tutoriana_pad.height > Screen_H:
            tutoriana_pad.y = Screen_H - tutoriana_pad.height

        #Update das Animations
        Orb.update()
        player.update()
        tutoriana.update()
        janela.update()
        
        
def dificuldades():
    raise NotImplementedError

def ranking():
    raise NotImplementedError


gameINIT()

print("Fechou")