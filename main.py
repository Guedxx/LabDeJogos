"""
O seguinte código apresenta o corpo principal do jogo "King Pong"
Feito para o projeto de Laboratório de Jogos no semestre 2024.1 do curso de ciência da computação UFF Niterói
Autores: Rafael de Lima Pereira (Github: @RafaelLime) e Pedro Guedes Guimarães (Github: @Guedxx)
Data da produção: 05/04/2024 - 12/07/2024



"""

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
from animations import *
from gamefunctions import *
from powerUps import *
from enemysIA import *

#Cria o diretório do arquivo principal. Garante compatibilidade com MAC e LINUX
project_directory = os.path.dirname(__file__)

# Informações e Criação da Janela
Screen_H, Screen_W = 720, 1280
janela = Window(Screen_W,Screen_H)
janela.set_title('King Pong')

# Mouse e Teclado
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

def play(fase:int) -> int:
    
    # Início da gameplay
    if fase == 0:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, DelayReact = setupF1(project_directory, Screen_W, Screen_H)
    elif fase == 1:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, ajudante, ajudanteSpeed, DelayReact = setupF2(project_directory, Screen_W, Screen_H)
    elif fase == 2:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, ajudante, ajudanteSpeed, TempodeDeAtividadeBase, tempoDeAtividade, DelayReact = setupF3(project_directory, Screen_W, Screen_H)
    elif fase == 3:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, DelayReact = setupF4(project_directory, Screen_W, Screen_H)
    elif fase == 4:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, DelayReact = setupF5(project_directory, Screen_W, Screen_H)
    elif fase == 5:
        backgnd, hotbar, player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, DelayReact = setupF6(project_directory, Screen_W, Screen_H)

    #Def Power Up da vez
    PowerUp = powerupSprite(project_directory, fase)

    # Velocidade da orb
    velx_base = 300
    vely_base = 300
    velx = velx_base
    vely = vely_base
    
    #Player
    velPlayer = 200

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

    #Vidas
    vida_player = 3
    vida_tutoriana = 3
    
    #Infos Power Ups
    PodeDesenhar = False
    PoweUpCoolDown = 600
    PoweUpCoolDownLoop = PoweUpCoolDown
 
    powerUpAtivo = False
    TempodeDeAtividadeBase = 600
    tempoDeAtividade = TempodeDeAtividadeBase
    
    DelayReactLoop = DelayReact
    
    

    while True:
        # Desenhar Sprites e GameImages
        drawAll(backgnd, hotbar, Orb, player_hearts, player_dash, player_pad, player, tutoriana_hearts, tutoriana_dash, tutoriana_pad, tutoriana)


        #Codigos referentes ao tutorial

        

        if teclado.key_pressed("E"):
            passou_fase(project_directory,janela,fase)
            return 1
        
        if teclado.key_pressed("F"):
            game_over(project_directory,janela, teclado, mouse)
            return 0

        if teclado.key_pressed("ESC"):
            if pause(project_directory,janela,teclado,mouse) == 0:
                return 0
            

        # Código da Orb

        #Colisão Paredes 
        if Orb.x + Orb.width >= Screen_W: # Ponto para Tutoriana
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "hit_sound.ogg"))
            sound_hit.play()
            Orb.x = Screen_W - Orb.width - 2
            player_hearts.x += 80 # -1 coração para o player
            vida_player -= 1
            velx = -(velx/2)
            vely = (vely/2)

        if Orb.x <= 0: #Ponto Player
            sound_hit = Sound(os.path.join(project_directory, "Sounds", "hit_sound.ogg"))
            sound_hit.play()
            Orb.x = 2
            tutoriana_hearts.x -= 80 # -1 coração para Tutoriana 
            vida_tutoriana -= 1

            if vida_tutoriana == 0:
                passou_fase(project_directory,janela,fase)
                return 1


            velx = -(velx - 30)
            vely = (vely - 15)

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
            
            if MomentumDirection_player == 1 and vely > 0:
                velx -= Momentum_player
                vely -= Momentum_player 
                vely *= -1
            if MomentumDirection_player == -1 and vely < 0:
                velx -= Momentum_player  
                vely -= Momentum_player 
                vely *= -1


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
                
            if MomentumDirection_enemy == 1 and vely > 0:
                velx -= Momentum_enemy
                vely -= Momentum_enemy
                vely *= -1
            if MomentumDirection_enemy == -1 and vely < 0:
                velx -= Momentum_enemy 
                vely -= Momentum_enemy
                vely *= -1
            
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
        if Momentum_player > 0:
            Momentum_player -= 75 * janela.delta_time()
            if Momentum_player < 0:
                Momentum_player = 0

        if MomentumDirection_player == 1:
            player_pad.y -= Momentum_player * janela.delta_time()
        elif MomentumDirection_player == -1:
            player_pad.y += Momentum_player * janela.delta_time()
            
        #Movements
        if teclado.key_pressed("W"):

            player_pad.y -= (velPlayer * janela.delta_time()) + (Momentum_player * janela.delta_time())

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

            player_pad.y += (velPlayer * janela.delta_time()) + Momentum_player * janela.delta_time()

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


        # CODIGOS REFERENTES AO INIMIGO
        
        #Momentum Enemy Calculations
        if Momentum_enemy > 0:
            Momentum_enemy -= 75 * janela.delta_time()
            if Momentum_enemy <= 0:
                Momentum_enemy = 0
                MomentumDirection_enemy = 0

        if MomentumDirection_enemy == 1:
            tutoriana_pad.y -= Momentum_enemy * janela.delta_time()
        elif MomentumDirection_enemy == -1:
            tutoriana_pad.y += Momentum_enemy * janela.delta_time()
        if MomentumDirection_enemy == 0:
            pass
        #Colide Walls
        if tutoriana_pad.y < player.height:
            tutoriana_pad.y = player.height
            Momentum_enemy = 0
            MomentumDirection_enemy = 0
        if tutoriana_pad.y + tutoriana_pad.height > Screen_H:
            tutoriana_pad.y = Screen_H - tutoriana_pad.height
            Momentum_enemy = 0
            MomentumDirection_enemy = 0
            
            
        DelayReactLoop -= 1500 * janela.delta_time() #Contabiliza o tempo de reação das IAS
        if fase == 0:   
            MomentumDirection_enemy, Momentum_enemy, DelayReactLoop= IA_tutoriana(tutoriana_pad, Orb, velx, janela, Momentum_enemy, DelayReactLoop, DelayReact, MomentumDirection_enemy)
        if fase == 1:   
            MomentumDirection_enemy, Momentum_enemy, DelayReactLoop  = IA_DrRippon(tutoriana_pad, Orb, velx, janela, Momentum_enemy, DelayReactLoop, DelayReact, MomentumDirection_enemy)


        if MomentumDirection_enemy == 1:
            tutoriana_pad.y -= (Momentum_enemy * janela.delta_time())
        if MomentumDirection_enemy == -1:
            tutoriana_pad.y += (Momentum_enemy * janela.delta_time())
        ##############################################################3

        #Codigo referene aos power ups
        
        PoweUpCoolDownLoop -= 100 * janela.delta_time()
        
        if random.randint(0,100) == 1 and PoweUpCoolDownLoop <= 0:
                if fase == 0:
                    PowerUp = powerupSprite(project_directory, fase)
                else:
                    PowerUp = powerupSprite(project_directory, fase - 1)
                PodeDesenhar = True
                PoweUpCoolDownLoop = PoweUpCoolDown
                     
                     
        if PodeDesenhar == True:
                PowerUp.draw()
                      
        #PowerUps Player       
        if fase != 0:
            if Orb.collided(PowerUp):
                PowerUpSound = Sound(os.path.join(project_directory, "Sounds", "powerUp.ogg"))
                PowerUpSound.play()
                
                if fase == 1:                   #Cura o Player com o PowerUp da Tutoriana
                    PowerUp.x = -50
                    if vida_player < 3:
                        vida_player += 1
                        player_hearts.x -= 80
                
                if fase == 2:                   #Ativa o ajudando do Player
                    PowerUp.x = -50
                    powerUpAtivo = True
                    tempoDeAtividade = TempodeDeAtividadeBase
                
                if fase == 3:                   #Ativa Speed do player
                    PowerUp.x = -50
                    powerUpAtivo = True
                    tempoDeAtividade = TempodeDeAtividadeBase
                
                if fase == 4:                   #Ativa Speed do player
                    PowerUp.x = -50
                    vely *= -1
             
          
        #Codigo refente ao ajudante do player          
        if powerUpAtivo == True and fase == 2:
            tempoDeAtividade -= 100 * janela.delta_time()
            if tempoDeAtividade > 0:
                ajudante.draw()
                ajudante.update()
                ajudante.y += ajudanteSpeed * janela.delta_time()
                
                if ajudante.y <= 150:
                    ajudanteSpeed *= -1
                    ajudante.y = 150
                    
                if ajudante.y + ajudante.height >= 720:
                    ajudanteSpeed *= -1
                    ajudante.y = 720 - ajudante.height
                    
                if Orb.collided(ajudante):
                    sound_hit = Sound(os.path.join(project_directory, "Sounds", "paddle_sound.ogg"))
                    sound_hit.play()
                    if abs(Orb.x + Orb.width - ajudante.x) < 20:
                        velx *= -1
                        Orb.x = ajudante.x - Orb.width
                    elif abs(Orb.y + Orb.height - ajudante.y) < 20 and vely > 0:
                        vely *= -1 
                        Orb.y = ajudante.y - Orb.height
                    elif abs(Orb.y - (ajudante.y + ajudante.height)) < 20 and vely < 0:
                        vely *= -1 
                        Orb.y = ajudante.y + ajudante.height       
                    
                            
            if tempoDeAtividade <= 0:
                powerUpAtivo = False
           
        #Codigo refente ao speed do player                   
        if powerUpAtivo == True and fase == 3:
            tempoDeAtividade -= 100 * janela.delta_time()
            velPlayer = 400
            
            if tempoDeAtividade <= 0:
                powerUpAtivo = False

        #Tutoriana
        if fase == 0:
            if Orb.collided(PowerUp):
                PowerUpSound = Sound(os.path.join(project_directory, "Sounds", "powerUp.ogg"))
                PowerUpSound.play()
                PowerUp.x = -50
                if vida_tutoriana < 3:
                    vida_tutoriana += 1
                    tutoriana_hearts.x += 80
                    
        #Dr Rippon
        if fase == 1:
            ajudante.draw()
            ajudante.update()
            
            ajudante.y += ajudanteSpeed * janela.delta_time()
            
            if ajudante.y <= tutoriana.height:
                ajudanteSpeed *= -1
                ajudante.y = tutoriana.height
            if ajudante.y + ajudante.height >= Screen_H:
                ajudanteSpeed *= -1
                ajudante.y = Screen_H - ajudante.height
            
            if Orb.collided(ajudante):
                sound_hit = Sound(os.path.join(project_directory, "Sounds", "paddle_sound.ogg"))
                sound_hit.play()
                if abs(Orb.x - (ajudante.x + ajudante.width)) < 20:
                    velx *= -1
                    Orb.x = ajudante.x + ajudante.width
                elif abs(Orb.y + Orb.height - ajudante.y) < 20 and vely > 0:
                    vely *= -1 
                    Orb.y = ajudante.y - Orb.height
                elif abs(Orb.y - (ajudante.y + ajudante.height)) < 20 and vely < 0:
                    vely *= -1 
                    Orb.y = ajudante.y + ajudante.height
                
            
        #GAME OVER
        if vida_player == 0:
            game_over(project_directory,janela, teclado, mouse)
            return 0

        #Update das Animations
        updateAll(janela, Orb, tutoriana, player)

while True:
    if gameINIT(project_directory, janela):
        lev = 0
        while True:
            stage = play(lev)
            lev += 1
            if lev == 6 or stage == 0:
                break
        
        if lev == 6:
            print("Your're the King Pong!")
        elif stage == 0:
            continue
        else:
            game_over(project_directory, janela, teclado, mouse)