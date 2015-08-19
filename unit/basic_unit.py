__author__ = 'Harley'
import pygame, unit
from pygame.sprite import Sprite, Group
from pygame.locals import *
from constants import *

class BasicUnit(pygame.sprite.Sprite):
    """
    The BasicUnit class describes all units in the game. It contains all methods that
    must be usable by any unit.
    Functions in BaseClass:
    die: detects if a unit has died or not
    can_attack: returns what unit, if any, a unit can attack.
    adjust_image: scale and flip the original sprite of an image based on unit size and team
    can_move: Checks if a unit should be able to move forward or not
    move: attempts to move a unit forward, checking with can_move if that is possible
    attack: deals damage to unit specified by can_attack
    """

    def __init__(self,
                 side,
                 ):
        Sprite.__init__(self)
        # These unit properties are the same for all units
        self.screen_x = 0
        self.screen_y = SCREEN_WIDTH
        self.side = side

        # These are all the properties a unit may have.
        self.speed = None # Determines how fast the unit moves per game cycle, in pixels. Must be an integer.
        self.health = None # Determines the hitpoints of the unit
        self.range = None # Determines from how far away from an enemy the unit may start attacking.
        self.image = None # Determines what is drawn when .draw is called. Based off the sprite in the subclasses.
        self.val = None # Sets how much a unit returns as bounty upon its death. Typically set to the unit price.
        self.attack_damage = None # How much damage each attack of the unit does.
        self.type = None # A string describing the unit type
    def die(self):
        if self.health<1:
            return True
        else:
            return False

    def can_attack(self,unit_list):
        """
        Can the unit attack something? Depends on range, location of
        nearby enemies.
        The enemies dictionary is used to keep track of which rect corresponds to which
        unit. This allows the use of collidedict, which checks for collision between the self rect,
        and all the values in the dictionary, returning the key to the colliding rect (the unit).
        """

        enemies = {}
        for unit in unit_list:
            if unit.side != self.side:
                enemies[unit] = unit.rect

        # range_rect is current unit's range
        if self.side == 0: # If side ==0, the range extends to the right of the unit
            range_rect = pygame.Rect(self.rect.left, self.rect.y,self.range +self.rect.w,self.rect.h)
            target = range_rect.collidedict(enemies)
        if self.side == 1: # If side == 1, the range extends to the left of the unit.
            range_rect = pygame.Rect(self.rect.left - self.range, self.rect.y, self.range+self.rect.w, self.rect.h)
            target = range_rect.collidedict(enemies)
        if target is not None:
            return target[0]
        else:
            return False
    def adjust_image(self):
        # Convert image for speed in drawing
        self.image.convert()
        # Transform the image provided to ensure it occupies the size dictated by sprites.size
        self.image = pygame.transform.scale(self.image,self.size)
        if self.side:
            self.image = pygame.transform.flip(self.image,True,False)

    def can_move(self,unit_list):
        """
        Is there a unit in front of me?
        First adds the rects of all active game objects to rect_list. This always excludes the fortress
        on the same side as the unit trying to move. collidelistall is then called, which returns a set of all
        collisions between the current unit and any rect in the set. If any collision is detected, can_move
        returns false. Otherwise, it returns true
        Returns a boolean
        """
        rect_list = []
        for units in unit_list.sprites():
            if not (units.type == 'fortress' and units.side == self.side):
                rect_list.append(units.rect)

        if len(self.rect.collidelistall(rect_list))>1:
            return False

        else:
            return True

    def move(self, unit_list):
        """
        Tries to move the self object forward or backward, depending on the team.
        move first moves the object, then calls can_move. If can_move does not detect a collision
        resulting from the move, move allows the move to happen. Otherwise, the change in position
        is undone.
        """
        if self.side:
            self.rect.x -=self.speed
        else:
            self.rect.x += self.speed
        if not self.can_move(unit_list):
            if self.side:
                self.rect.x +=self.speed
            else:
                self.rect.x -= self.speed

    def attack(self,unit_list):
        """
        Calls can_attack to determine what (if any) enemy is in range to attack.
        If can_attack returns false, no attack is executed.
        Otherwise, can_attack returns a target unit. This target unit then has its health reduced
        by the attack damage of the attacking unit. The image is then refreshed so a new health
        can be be draw on.
        """
        can_attack = self.can_attack(unit_list)
        if can_attack== False:
            return
        else:
            can_attack.health -= self.attack_damage








