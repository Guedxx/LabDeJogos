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
from setup import *

#Cria o diretório do arquivo principal. Garante compatibilidade com MAC e LINUX
project_directory = os.path.dirname(__file__)

# Informações e Criação da Janela
Screen_H, Screen_W = 720, 1280
janela = Window(Screen_W,Screen_H)
janela.set_title('King Pong')

# Mouse e Teclado
mouse = Window.get_mouse()
teclado = Window.get_keyboard()


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
            time -= 10 * janela.delta_time()
            tittleScreen_1.draw()
            janela.update()

        #CountDown da segunda tela
        time = 15
        while time > 0:

            time -= 10 * janela.delta_time()
            tittleScreen_2.draw()
            janela.update()

        menu() #Inicia o Menu

# Menu Principal
def menu():

    dificuldade_menu = 0
    cooldown_dificuldade = 0

    # Inicializa Imagens usadas no Menu
    # Imagem que aparece junto com o "Press Space to Begin"
    Fundo_INIT = GameImage(os.path.join(project_directory, "Sprites", "MENU_menuInitScreen.png"))

    #Fundos
    Fundo_EASY = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_easy.png"),4)
    Fundo_EASY.set_sequence_time(0,2,975)
    Fundo_EASY.play()
    Fundo_NORMAL = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_normal.png"),4)
    Fundo_NORMAL.set_sequence_time(0,2,765)
    Fundo_NORMAL.play()
    Fundo_HARD = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_hard.png"),4)
    Fundo_HARD.set_sequence_time(0,2,500)
    Fundo_HARD.play()

    # Imagem conjunta do botão "Play", "Diff" e "Quit" que entra na animação
    side_bar_normal = GameImage(os.path.join(project_directory, "Sprites", "MENU_side_normal.png"))
    side_bar_normal.set_position(-780, 0)

    # Imagem do pixel de seleção do menu principal
    Indicador = GameImage(os.path.join(project_directory, "Sprites", "MENU_Indicador.png"))

    #Bonequinho Animado :D
    lil_man = Animation((os.path.join(project_directory, "Sprites", "MENU_Char.png")), 4)
    lil_man.set_position(220, 420)
    lil_man.set_sequence_time(0,2,200)
    lil_man.play()
    
    #Musica que toca
    menu_music = Sound(os.path.join(project_directory, "Sounds", "menu.ogg"))
    menu_music.play()

    #Sons Menu
        #Mouse hover area TODO
        #Mouse Click TODO

    # Mini Loop que pede para o jogador apertar espaço
    while True:     
        
        if teclado.key_pressed("SPACE"):
            break

        janela.set_background_color([0,0,0])
        Fundo_INIT.draw()
        lil_man.draw()
        lil_man.update()
        janela.update()

    while True:

        #Animação que traz o menu pelo lado
        desacelerador = 0
        while side_bar_normal.x < 0:
            desacelerador += 40 * janela.delta_time()
            side_bar_normal.x += (700 - desacelerador) * janela.delta_time()
            side_bar_normal.draw()
            janela.update()


        #Começo do Loop do Menu 
        janela.set_background_color([0,0,0]) 

        if dificuldade_menu == -1: #Dificuldade easy
            Fundo_EASY.draw()
            Fundo_EASY.update()
            side_bar = GameImage(os.path.join(project_directory, "Sprites", "MENU_side_easy.png"))
        if dificuldade_menu == 0: #Dificuldade normal
            Fundo_NORMAL.draw()
            Fundo_NORMAL.update()
            side_bar = GameImage(os.path.join(project_directory, "Sprites", "MENU_side_normal.png"))
        if dificuldade_menu == 1: #Dificuldade hard
            Fundo_HARD.draw()
            Fundo_HARD.update()
            side_bar = GameImage(os.path.join(project_directory, "Sprites", "MENU_side_hard.png"))
        
            

        #As seguintes linhas são em relação aos clicks do mouse 
                
        if mouse.is_over_area([95, 380], [250, 412]):          #Botão de Play
            
            if mouse.is_button_pressed(1):
                menu_music.pause()
                play()
                
        cooldown_dificuldade -= 60 * janela.delta_time()
        if mouse.is_over_area([95, 470], [280, 500]):          #Botão de Dificuldades
            
            if mouse.is_button_pressed(1) and cooldown_dificuldade <= 0:
                if dificuldade_menu < 1:
                    dificuldade_menu += 1
                elif dificuldade_menu == 1:
                    dificuldade_menu = -1
                cooldown_dificuldade = 30
                
                
                
        if mouse.is_over_area([95, 550], [222, 577]):          #Botão de Sair
            Indicador.set_position(400, 500)
            Indicador.draw()

            if mouse.is_button_pressed(1):
                menu_music.pause()
                janela.close()
        

        side_bar.draw()
        janela.update()

def play():
    
    # Início da gameplay
    backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb = setupF1(project_directory, Screen_W, Screen_H)
    

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

    #Infos Momentum
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
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "hit_sound.ogg"))
            sound_hit.play()
            Orb.x = Screen_W - Orb.width - 2
            player_hearts.x += 80 # -1 coração para o player
            velx = -(velx/2)
            vely = (vely/2)

        if Orb.x <= 0: #Ponto Player
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "hit_sound.ogg"))
            sound_hit.play()
            Orb.x = 2
            tutoriana_hearts.x -= 80 # -1 coração para Tutoriana 
            velx = -(velx/2)
            vely = (vely/2)

        if Orb.y >= Screen_H - Orb.height: #Parede de Baixo
            sound_wall = Sound(os.path.join(project_directory, "Sounds", "wall_sound.ogg"))
            sound_wall.play()
            Orb.y = Screen_H - Orb.height
            vely *= -1
        if Orb.y <= tutoriana.height: #Parede de Cima
            sound_wall = Sound(os.path.join(project_directory, "Sounds", "wall_sound.ogg"))
            sound_wall.play()
            Orb.y = tutoriana.height
            vely *= -1
        
        #Colisão Pads
        if Orb.collided(player_pad):
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "paddle_sound.ogg"))
            sound_hit.play()
            if abs(Orb.x + Orb.width - player_pad.x) < 20:
                velx *= -1
                Orb.x = player_pad.x - Orb.width
            elif abs(Orb.y + Orb.height - player_pad.y) < 20 and vely > 0:
                vely *= -1 
                Orb.y = player_pad.y - Orb.height
            elif abs(Orb.y - (player_pad.y + player_pad.height)) < 20 and vely < 0:
                vely *= -1 
                Orb.y = player_pad.y + player_pad.height

        if Orb.collided(tutoriana_pad):
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "paddle_sound.ogg"))
            sound_hit.play()
            if abs(Orb.x - (tutoriana_pad.x + tutoriana_pad.width)) < 20:
                velx *= -1
                Orb.x = tutoriana_pad.x + tutoriana_pad.width
            elif abs(Orb.y + Orb.height - tutoriana_pad.y) < 20 and vely > 0:
                vely *= -1 
                Orb.y = tutoriana_pad.y - Orb.height
            elif abs(Orb.y - (tutoriana_pad.y + tutoriana_pad.height)) < 20 and vely < 0:
                vely *= -1 
                Orb.y = tutoriana_pad.y + tutoriana_pad.height
            
        #Movimentação
        Orb.x += velx * janela.delta_time()
        Orb.y += vely * janela.delta_time()

        #Aumento de velocidades
        if  550 > velx > 0:
            velx += 10 * janela.delta_time()
        elif 550 < velx < 0:
            velx -= 10 * janela.delta_time()
        
        if  550 > vely > 0:
            vely += 5 * janela.delta_time()
        elif 550 < vely < 0:
            vely -= 5 * janela.delta_time()


        #vel_animation -= 200 * janela.delta_time()
        #Orb.set_total_duration(vel_animation)

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
        

def ranking():
    raise NotImplementedError


gameINIT()

print("Fechou")