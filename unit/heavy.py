__author__ = 'Harley'
import pygame, unit
from unit.basic_unit import BasicUnit
from unit.melee import *
from constants import *
# The heavy class has the special property of ignoring unit collision, friendly or enemy.
# The heavy will still stop at the enemy base, or enemy heavy and deal damage as it moves
class heavy(melee):
    sprite = pygame.image.load("media/art/heavy.png")

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        self.type = 'heavy'
        self.image = self.sprite
        self.health =50
        self.speed =1
        self.attack_damage = .05
        self.val = HEAVY_PRICE
        HEAVY_HEIGHT = UNIT_HEIGHT+100
        HEAVY_WIDTH = UNIT_WIDTH+100

        # Set up screen positioning and unit rect dimensions
        if self.side == 1:
            self.screen_x = SCREEN_WIDTH - HEAVY_WIDTH

        # Set constants for all units
        self.screen_y  = SCREEN_HEIGHT- HEAVY_HEIGHT
        self.size = (HEAVY_WIDTH, HEAVY_HEIGHT)
        # Define unit rect for drawing
        self.rect = pygame.Rect(self.screen_x,self.screen_y,HEAVY_WIDTH,HEAVY_HEIGHT)
        self.type = 'heavy'
        self.adjust_image()
    # Allowed to move through anything other than enemy fortresses and heavies
    def can_move(self,unit_list):
        """
        Is there a unit in front of me?
        Returns a boolean
        """
        rect_list = []
        for units in unit_list:
            # Needs to be like this, don't know why. Should be able to just do if ('fortress or heavy'), but if not( everything else) must be used.
            #if not((units.type == 'fortress' and units.side == self.side) or (units.type == 'melee') or (units.type == 'archer')):
            if (units.type == 'fortress' and units.side != self.side) or (units.type == 'heavy'):
                rect_list.append(units.rect)

        if len(self.rect.collidelistall(rect_list))>1:
            return False

        else:
            return True

unit.unit_type["heavy"] = heavy