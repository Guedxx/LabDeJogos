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
    
    SpriteDePowerUp.set_position(random.randint(40, 1200),random.randint(150, 630))
    
    
    
 

def powerupSprite(project_directory, int):
    
    if int == 0:
        PowerUpSprite = Animation(os.path.join(project_directory, "Sprites", "POWERUP_Health.png"),2)
        PowerUpSprite.set_sequence_time(0,2,100)
    if int == 1:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
    if int == 2:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
    if int == 3:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
    if int == 4:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
    if int == 4:
        PowerUpSprite = GameImage(os.path.join(project_directory, "Sprites", "POWERUP_PlaceHolder.png"))
        
        
    randomLocal(PowerUpSprite)
    return PowerUpSprite
