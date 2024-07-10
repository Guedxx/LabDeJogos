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
from gamefunctions import *



def randomLocal(SpriteDePowerUp):
    
    SpriteDePowerUp.set_position(random.randint(40, 1200),random.randint(140, 630))
    
    
    
    

def powerupSprite(project_directory, int):
    
    if int == 0:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
    
    if int == 1:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
        
    randomLocal(PowerUpSprite)
    return PowerUpSprite
    