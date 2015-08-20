__author__ = 'Harley'
import sys, pygame, unit
from unit import *
from pygame.sprite import LayeredUpdates, Group
from constants import *
from partition import*
# Initialize fonts for use in rendering unit health, prices, and current cash
pygame.font.init()
# Each font is initialized here. The size of the text can be adjusted by altering the second
# argument
healthfont = pygame.font.Font(None,30)
moneyfont = pygame.font.Font(None,50)
pricefont = pygame.font.Font(None,30)

# class spriteHUD(pygame.sprite.Sprite):
#     def __init__(self,image,rect):
#         self.image = image
#         self.rect = rect

class GUI():
    # These variables dictate how much cash the player has to spend. The starting
    # cash is set here.
    team_0_cash = 500
    team_1_cash = 500
    def __init__(self,screen_rect,filestr):
        """
        Initialize the display.
        screen_rect: the bounds of the screen
        filestr: the background image filestring, to be used for loading the background image
        """

        # Set up the screen
        self.screen = pygame.display.set_mode((screen_rect.w, screen_rect.h))
        # Allow screen_rect to be used throughout an instance of GUI
        self.screen_rect = screen_rect
        # Load background image
        self.background = pygame.image.load(filestr).convert()
        # Load HUD image
        self.HUD = pygame.image.load("media/art/HUD.png").convert()
        # Define size of HUD bar
        self.bar_rect=pygame.Rect(0,0,screen_rect.w,70)
        # living_units will store all active sprites present throughout the game
        self.living_units = pygame.sprite.LayeredUpdates()


    def load_background(self):
        #Scale image to match screensize given
        self.background =pygame.transform.scale(self.background,(self.screen_rect.w,self.screen_rect.h))
        #Place image on screen drawing from the top left
        self.screen.blit(self.background, [0,0])
        # Draw the HUD overtop the background
        self.draw_HUD()

    # Each activate_(x) function initializes a new instance of the specific class, passing
    # in the "side" attribute. This new instance is then passed to can_spawn to see if it is currently
    # allowed.
    def activate_melee(self,team):
        new_melee = unit.unit_type['melee'](
                 side = team
                 )
        self.can_spawn(new_melee)
    def activate_archer(self,team):
        new_archer = unit.unit_type['archer'](
                 side = team
                 )
        self.can_spawn(new_archer)
    def activate_fortress(self,team):
        new_fortress = unit.unit_type['fortress'](
            side = team
        )
        self.living_units.add(new_fortress)
    def activate_heavy(self,team):
        new_heavy = unit.unit_type['heavy'](
                 side = team,
                 )
        self.can_spawn(new_heavy)

    def can_spawn(self,unit):
        """
        Decides if a unit can be spawned or not.
        unit is the unit sprite that the player is attempting to spawn. If the unit
        can spawn can_spawn appends it to the living_units group, activating.
        Returns nothing.
        """
        # Generate a temporary unit list, a subset of living_units.
        temp_unit_list = []
        # Friendly fortresses are ignored for spawn collision detection
        for units in self.living_units.sprites():
            if not (units.type == 'fortress' and unit.side == units.side):
                temp_unit_list.append(units)
        # If no conflicts are detected, allow the unit to spawn and deduct the unit price from
        # the spawning player's money
        if not len(unit.rect.collidelistall(temp_unit_list))>0:
            if unit.type == 'melee' and unit.side:
                self.team_1_cash -= MELEE_PRICE
                self.living_units.add(unit,layer=2) # Melee sprites are drawn on the top layer
            if unit.type == 'melee' and not unit.side:
                self.team_0_cash -= MELEE_PRICE
                self.living_units.add(unit,layer=2)
            if unit.type == 'archer' and not unit.side:
                self.team_0_cash -= ARCHER_PRICE # Archer sprites are drawn on the top layer
                self.living_units.add(unit,layer=2)
            if unit.type == 'archer' and unit.side:
                self.team_1_cash -= ARCHER_PRICE
                self.living_units.add(unit,layer=2)
            if unit.type == 'heavy' and not unit.side:
                self.team_0_cash -= HEAVY_PRICE # Heavies are drawn on the middle layer
                self.living_units.add(unit,layer=1)
            if unit.type == 'heavy' and unit.side:
                self.team_1_cash -= HEAVY_PRICE
                self.living_units.add(unit,layer=1)

    # special is called when either player purchases the "swap" effect.
    # special evenly redistributes the units currently on the field such that
    # both players have the same or approximately the same cash value of units active
    def special(self,team):
        # A temp container is filled with all units in living_units, excluding fortresses, and units within fortresses.
        temp_container=[]
        for unit in self.living_units.sprites():
            if unit.type!='fortress' and unit.rect.left>=FORTRESS_WIDTH and unit.rect.right<=SCREEN_WIDTH-FORTRESS_WIDTH:
                temp_container.append(unit)

        # temp_cost holds all the values of the units in temp_container
        temp_cost=[]
        for unit in temp_container:
            temp_cost.append(unit.val)
        print(temp_cost)
        # The set of costs is then passed into even_partition, which returns 2 sets of unit values approximately equal.
        set1,set2=even_partition(temp_cost)
        print(set1,set2)
        # For each unit considered, find where its value exists in the two sets returned.
        # When its value is found, assign that unit to a team, and remove the value from the set.
        
        for unit in temp_container:
            flip=False
            if unit.val in set1:
                if unit.side==1:flip=True
                if flip:unit.adjust_image()
                unit.side=0
                unit.adjust_image()
                set1.remove(unit.val)

            elif unit.val in set2:
                if unit.side==0:flip=True
                unit.side=1
                if flip:unit.adjust_image()
                set2.remove(unit.val)

        # With the swap successful, deduct the price of the swap from the player who called it's account.
        if team: self.team_1_cash -= SWAP_PRICE
        if team==0: self.team_0_cash -= SWAP_PRICE

    def update_units(self):
        """
        Update units will iterate through each currently active unit, and try to move, and attack.
        If any unit is found to be at <=0 health, update_units removes that dead unit from the game.
        update_units also detects when either fortress dies, and ends the game, announcing in the console
        which player won.
        """
        # Clear all old sprites for redraw and update
        self.living_units.clear(self.screen,self.background)
        # For each active sprite attempt to move and attempt to attack.
        # Finally, check for sprite death. If a sprite dies, award its bounty to the
        # enemy team
        for sprites in self.living_units.sprites():
            # Attempt to move
            sprites.move(self.living_units)
            # Attempt to attack
            sprites.attack(self.living_units)
            # If a sprite dies, kill it and award bounty
            if sprites.die():
                sprites.kill()
                if sprites.side:
                    self.team_0_cash += sprites.val
                else:
                    self.team_1_cash += sprites.val
                # If a fortress dies, the game is over.
                if sprites.type == 'fortress':
                    print('Side {} wins!'.format(sprites.side^1))
                    quit()

    def render_info(self,info,font,team=None):
        """
        Generalized function that takes in an info variable, a font, and an optional team flag.
        render_info returns an image of the info passed rendered in the font passed, with possible
        customization based on the team passed, along with a rect to draw it on.
        """
        # If the info belongs to no team, color the text black
        if team == None:
            color = (0,0,0)
        # If the info belongs to team 1, color the text red
        if team:
            #team 1 color
            color = (255,0,0)
        # If the info belongs to team 0, color the text blue
        elif team == 0:
            #team 2 color
            color = (0,0,255)
        # Render the text
        info_text = font.render(str(int(info)),1, color)
        # Retrieve the rect needed to draw the text on.
        info_rect = info_text.get_rect()
        return info_text,info_rect
    def draw_units(self):
        """
        For every active unit in the game, redraw their self.image property as dictated by their self.rect.
        Additionally, each unit's current health is drawn on with a grey health bar backing.
        """
        for sprites in self.living_units.sprites():
            # Define the size of the rect used to draw the grey backing for the health text.
            # The rect size is decided by the width of the unit.
            health_back_rect = pygame.Rect(0,0,sprites.rect.w,healthfont.size(str(int(sprites.health)))[1])
            # Fill the top of the image with a grey bar.
            sprites.image.fill((200,200,200),health_back_rect)
            # Blit on the health text for the unit, as rendered by render_info
            sprites.image.blit(self.render_info(sprites.health,healthfont,sprites.side)[0], self.render_info(sprites.health,healthfont,sprites.side)[1])
        # Draw everything, now that it's updated.
        self.living_units.draw(self.screen)
    def draw_HUD(self):
        #Draw prices
        self.screen.blit(self.HUD,[0,0])
        self.screen.blit(self.render_info(MELEE_PRICE,pricefont)[0], (220,45))
        self.screen.blit(self.render_info(ARCHER_PRICE,pricefont)[0], (328,45))
        self.screen.blit(self.render_info(HEAVY_PRICE,pricefont)[0], (436,45))
        self.screen.blit(self.render_info(SWAP_PRICE,pricefont)[0], (537,45))
        self.screen.blit(self.render_info(SWAP_PRICE,pricefont)[0], (660,45))
        self.screen.blit(self.render_info(MELEE_PRICE,pricefont)[0], (768,45))
        self.screen.blit(self.render_info(ARCHER_PRICE,pricefont)[0], (876,45))
        self.screen.blit(self.render_info(HEAVY_PRICE,pricefont)[0], (983,45))
    def update_HUD(self):
        # Draw HUD background, refreshing just the corners
        #self.HUD_sprite.draw()
        self.screen.blit(self.HUD,[0,0],pygame.Rect(0,0,210,100))
        self.screen.blit(self.HUD,[1100,0],pygame.Rect(1100,0,210,100))
        #Draw money totals
        self.screen.blit(self.render_info(self.team_0_cash,moneyfont)[0], (95, 22))
        self.screen.blit(self.render_info(self.team_1_cash,moneyfont)[0], (1125,22))
