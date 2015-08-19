__author__ = 'Harley'
import pygame, unit
from unit.basic_unit import BasicUnit
from unit.melee import *
from constants import *

class archer(melee):
    sprite = pygame.image.load("media/art/archer_new.png")

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        self.range = 3*UNIT_WIDTH
        self.type = 'archer'
        self.image = self.sprite
        self.health = 5
        self.val = ARCHER_PRICE
        self.speed = 3
        self.adjust_image()
unit.unit_type["archer"] = archer