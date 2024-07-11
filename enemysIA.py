from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.sound import *
import os

def IA_tutoriana(tutoriana_pad, Orb, velx, janela, Momentum_enemy , DelayReactLoop):
    
    MomentumDirection_enemy = 0

    if DelayReactLoop <= 0:
        #Sobe em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 < Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = -1

        #Desce em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 > Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = 1

    if MomentumDirection_enemy == -1:
        tutoriana_pad.y += (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) # Subir
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()
    
    if MomentumDirection_enemy == 1:
        tutoriana_pad.y -= (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) #Descer
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()

    return MomentumDirection_enemy


def IA_DrRippon(tutoriana_pad, Orb, velx, janela, Momentum_enemy, DelayReact):

    pass