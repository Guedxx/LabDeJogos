from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.sound import *
import os

def IA_tutoriana(tutoriana_pad, Orb, velx, janela, Momentum_enemy , DelayReactLoop, DelayReact, MomentumDirection_enemy):
    if DelayReactLoop <= 0:
        #Sobe em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 < Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = -1
            DelayReactLoop = DelayReact
            
        #Desce em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 > Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = 1
            DelayReactLoop = DelayReact
            
    if MomentumDirection_enemy == -1 and velx < 0:

        tutoriana_pad.y += (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) # Subir
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()
    
    if MomentumDirection_enemy == 1 and velx < 0:
        tutoriana_pad.y -= (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) #Descer
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()
    
    if MomentumDirection_enemy == 0:
        pass

    return MomentumDirection_enemy, Momentum_enemy, DelayReactLoop


def IA_DrRippon(tutoriana_pad, Orb, velx, janela, Momentum_enemy , DelayReactLoop, DelayReact, MomentumDirection_enemy):
    if DelayReactLoop <= 0:
        #Sobe em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 < Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = -1
            DelayReactLoop = DelayReact
            
        #Desce em relaçâo ao orb
        if tutoriana_pad.y + tutoriana_pad.height/2 > Orb.y + Orb.height /2 and velx < 0:
            MomentumDirection_enemy = 1
            DelayReactLoop = DelayReact
            
    if MomentumDirection_enemy == -1 and velx < 0:

        tutoriana_pad.y += (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) # Subir
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()
    
    if MomentumDirection_enemy == 1 and velx < 0:
        tutoriana_pad.y -= (210 * janela.delta_time()) + (Momentum_enemy * janela.delta_time()) #Descer
        if Momentum_enemy < 100 and tutoriana_pad.y > 150:
                Momentum_enemy += 100 * janela.delta_time()
    
    if MomentumDirection_enemy == 0:
        pass

    return MomentumDirection_enemy, Momentum_enemy, DelayReactLoop

