__author__ = 'Harley'
import sys, pygame
from constants import *

from gui import GUI
RESOLUTION = pygame.Rect(0, 0,SCREEN_WIDTH , SCREEN_HEIGHT)
pygame.init()

# Main_bgui is an instance of the gui class. Initializes screen size
main_gui = GUI(RESOLUTION,"media/art/back_new.jpg")
main_gui.load_background()

clock = pygame.time.Clock()

# Set starting units:
main_gui.activate_fortress(0)
main_gui.activate_fortress(1)
# The game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        # End if q is pressed
        if (event.type == pygame.KEYDOWN and
        (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            pygame.display.quit()
            sys.exit()
        # a key spawns a melee unit on the left side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_a and main_gui.team_0_cash>=MELEE_PRICE):
            main_gui.activate_melee(0)
        # j key spawns a melee unit on the right side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_j and main_gui.team_1_cash>=MELEE_PRICE):
            main_gui.activate_melee(1)
        # s key spawns a archer unit on the left side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_s and main_gui.team_0_cash>=ARCHER_PRICE):
            main_gui.activate_archer(0)
        # k key spawns a archer unit on the right side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_k and main_gui.team_1_cash>=ARCHER_PRICE):
            main_gui.activate_archer(1)
        # d key spawns a heavy unit on the left side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_d and main_gui.team_0_cash>=HEAVY_PRICE):
            main_gui.activate_heavy(0)
        # l key spawns a heavy unit on the right side
        if (event.type == pygame.KEYDOWN and
        event.key == pygame.K_l and main_gui.team_1_cash>=HEAVY_PRICE):
            main_gui.activate_heavy(1)
        # f key activates unit balancer, charges team 0 the cost
        if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_f and main_gui.team_0_cash>=SWAP_PRICE):
            main_gui.special(0)
        # h key activates unit balancer, charges team 1 the cost
        if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_h and main_gui.team_1_cash>=SWAP_PRICE):
            main_gui.special(1)
    pygame.display.flip()
    main_gui.update_units()
    main_gui.draw_units()
    main_gui.update_HUD()
    clock.tick(60)


