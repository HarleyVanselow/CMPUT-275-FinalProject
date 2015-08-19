__author__ = 'Harley'
import pygame, unit
from unit.basic_unit import BasicUnit
from unit.fortress import FORTRESS_HEIGHT, FORTRESS_WIDTH
from constants import *


class melee(BasicUnit):
    sprite = pygame.image.load("media/art/melee.png")
    def __init__(self,*args,**kwargs):
        # These variables will be overwritten by the super init
        self.side = None
        self.screen_y = None
        self.screen_x = None

        # Get init values sent to baseclass
        super().__init__(**kwargs)

        # Unit specific values
        self.health = 10
        self.attack_damage = .02
        self.range = UNIT_WIDTH/2
        self.image = self.sprite
        self.speed = 5
        self.val = MELEE_PRICE
        side = self.side




        # Set up screen positioning and unit rect dimensions
        if side == 1:
            self.screen_x = SCREEN_WIDTH - UNIT_WIDTH

        # Set constants for all units
        self.screen_y  = SCREEN_HEIGHT- UNIT_HEIGHT
        self.size = (UNIT_WIDTH, UNIT_HEIGHT)
        # Define unit rect for drawing
        self.rect = pygame.Rect(self.screen_x,self.screen_y,UNIT_WIDTH,UNIT_HEIGHT)
        self.type = 'melee'
        self.adjust_image()


unit.unit_type["melee"] = melee