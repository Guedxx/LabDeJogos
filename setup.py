from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.animation import *
from PPlay.sound import *
from PPlay.keyboard import *
from PPlay.mouse import *
import os


def gameINIT(project_directory, janela):

    #Tela "A Game Lab Project"
    tittleScreen_1, tittleScreen_2 = GameImage(os.path.join(project_directory, "Sprites", "INIT_aGameLabProject.png")), GameImage(os.path.join(project_directory, "Sprites", "INIT_madeBy.png"))
    #Tela "Made By"
    GameImage(os.path.join(project_directory, "Sprites", "INIT_madeBy.png"))

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

        menu(project_directory, janela, Window.get_keyboard(), Window.get_mouse()) #Inicia o Menu
        return 1

# Menu do jogo
def menu(project_directory, janela, teclado, mouse):

    dificuldade_menu = 0
    cooldown_dificuldade = 0

    # Inicializa Imagens usadas no Menu
    Logo = Fundo_EASY = GameImage(os.path.join(project_directory, "Sprites", "INIT_LOGO.png"))

    #Fundos
    Fundo_EASY = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_easy.png"),3)
    Fundo_EASY.set_sequence_time(0,3,975)
    Fundo_EASY.play()
    Fundo_NORMAL = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_normal.png"),3)
    Fundo_NORMAL.set_sequence_time(0,3,765)
    Fundo_NORMAL.play()
    Fundo_HARD = Animation(os.path.join(project_directory, "Sprites", "MENU_bg_hard.png"),3)
    Fundo_HARD.set_sequence_time(0,3,500)
    Fundo_HARD.play()

    # Imagem conjunta do botão "Play", "Diff" e "Quit" que entra na animação
    side_bar_normal = GameImage(os.path.join(project_directory, "Sprites", "MENU_side_normal.png"))
    side_bar_normal.set_position(-780, 0)

    # Imagem do pixel de seleção do menu principal
    Indicador = GameImage(os.path.join(project_directory, "Sprites", "MENU_Indicador.png"))

    #Bonequinho Animado :D
    lil_man = Animation((os.path.join(project_directory, "Sprites", "MENU_Char.png")), 4)
    lil_man.set_position(220, 445)
    lil_man.set_sequence_time(0,2,200)
    lil_man.play()
    
    #Musica que toca
    menu_music = Sound(os.path.join(project_directory, "Sounds", "menu.ogg"))
    menu_music.play()

    #Sons Menu
        #Mouse hover area TODO
        #Mouse Click

    # Mini Loop que pede para o jogador apertar espaço
    while True:     
        
        if teclado.key_pressed("SPACE"):
            break

        janela.set_background_color([0,0,0])
        
        Fundo_NORMAL.draw()
        Fundo_NORMAL.update()
        Logo.draw()
        lil_man.draw()
        lil_man.update()
        janela.update()

        #Loop musica
        if menu_music.is_playing() == False:
            menu_music = Sound(os.path.join(project_directory, "Sounds", "menu.ogg"))
            menu_music.play()


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

        #Loop musica menu
        if menu_music.is_playing() == False:
            menu_music = Sound(os.path.join(project_directory, "Sounds", "menu.ogg"))
            menu_music.play()

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
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                menu_music.pause()
                return 1
                
        cooldown_dificuldade -= 60 * janela.delta_time()
        if mouse.is_over_area([95, 470], [280, 500]):          #Botão de Dificuldades
            
            if mouse.is_button_pressed(1) and cooldown_dificuldade <= 0:
                mouse_click = Sound(os.path.join(project_directory, "Sounds", "MENUSelect.ogg"))
                mouse_click.play()
                if dificuldade_menu < 1:
                    dificuldade_menu += 1
                elif dificuldade_menu == 1:
                    dificuldade_menu = -1
                cooldown_dificuldade = 30
                
                
                
        if mouse.is_over_area([95, 550], [222, 577]):          #Botão de Sair
            Indicador.set_position(400, 500)
            Indicador.draw()

            if mouse.is_button_pressed(1):
    
                mouse_click.play()
                menu_music.pause()
                janela.close()
        

        side_bar.draw()
        janela.update()

# Tutoriana
def setupF1(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETTutoriana.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Tutoriana.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb

# Dr Rippon
def setupF2(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETDrRippon.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_DrRippon.png")) 
    tutoriana_pad.set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    
    ajudante = Animation(os.path.join(project_directory, "Sprites", "PAD_DrHelper.png"), 2)
    ajudante.set_sequence_time(0,2,100)
    ajudante.set_position(10, player.height + 5)
    ajudanteSpeed = 300 

    
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, ajudante, ajudanteSpeed

# Cinos
def setupF3(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETSanic.png"),6)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,6,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Cinos.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    
    ajudante = Animation(os.path.join(project_directory, "Sprites", "PAD_PlayerHelper.png"), 2)
    ajudante.set_sequence_time(0,2,100)
    ajudante.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    ajudanteSpeed = 300 
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb, ajudante, ajudanteSpeed

# Ronaldinho
def setupF4(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETRonaldinhoBahiano.png"),18)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,18,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Ronaldinho.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb

# Bulk
def setupF5(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETBulk.png"),19)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,19,100)
    tutoriana_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Bulk.png")) 
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb

# King Pong
def setupF6(project_directory, Screen_W, Screen_H):
    player = Animation(os.path.join(project_directory, "Sprites", "SHEETMainChar.png"),18)
    player.set_position(Screen_W - player.width,0)
    player.set_sequence_time(0,18,100)
    player_pad = Sprite(os.path.join(project_directory, "Sprites", "PAD_Player.png"))
    player_pad.set_position(Screen_W -  player_pad.width - 10, ((Screen_H  + player.height)/2) - player_pad.height/2)
    player_hearts = Sprite(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    player_hearts.set_position(890, 20)
    player_dash = Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    player_dash .set_position(890, 90)

    tutoriana = Animation(os.path.join(project_directory, "Sprites", "SHEETKingPong.png"),4)
    tutoriana.set_position(0,0)
    tutoriana.set_sequence_time(0,4,50)
    tutoriana_pad = Animation(os.path.join(project_directory, "Sprites", "PAD_KingPong.png"),2) 
    tutoriana_pad.set_sequence_time(0,2,100)
    tutoriana_pad .set_position(10, ((Screen_H  + player.height)/2) - tutoriana_pad.height/2)
    tutoriana_hearts = GameImage(os.path.join(project_directory, "Sprites", "HEARTS.png"))
    tutoriana_hearts.set_position(160, 20)
    tutoriana_dash= Sprite(os.path.join(project_directory, "Sprites", "DASHBAR.png"))
    tutoriana_dash.set_position(160, 90)

    Orb = Animation(os.path.join(project_directory, "Sprites", "SHEETORB.png"), 8)
    Orb.set_position(Screen_W/2, (Screen_H  )/2)
    vel_animation = 100
    Orb.set_sequence_time(0,8, vel_animation)
    return GameImage(os.path.join(project_directory, "Sprites", "LV1_background.png")), GameImage(os.path.join(project_directory, "Sprites", "HOTBAR.png")), player, player_pad, player_hearts, player_dash, tutoriana, tutoriana_pad, tutoriana_hearts, tutoriana_dash, Orb