CMPUT 275 Project:
Age of War in Space Rip-off
Harley Vanselow, ID: 1388813
Aaron Philips, ID: 1408127


Our project is a two player game, inspired by the flash browser game “Age of War”. The object of the game is for one of the two players to destroy the opposing base. This is achieved by spawning units with the keys indicated in the HUD( A, S, D, F and H, J, K, L). Each unit spawn has a certain cost, indicated below the unit icon, which is deducted from a player’s cash total after the player successfully spawns the unit. 


File system:
* root:
   * The root folder contains all the primary game files, as well as the unit and media subfolders.
   * main.py:
      * Contains main game loop. To run the game, main.py should be run as the target file using python 3.2. Pygame must be installed. Calls an instance of gui.
   * gui.py:
      *  Has the gui class which contains all methods used to draw the game content to the screen, as well as methods for activating units based on keyboard input received in main.py. gui.py also handles when the swap ability is called from main
                
   * constants.py:
      * Has all the constants required for gameplay. These include the screen width and height, unit width and height, and unit price


   * partition.py:
      * Has an implementation of the partition problem solver. this file has a function the takes in a list of integers and outputs two sublists made from the elements (each element in the original list is accounted for once, in either of the two sublists) of the original list such that the sublists are as close to have an equal sum ( of elements in each sub list). Used to even teams by cost. The runtime analysis , (based on nested loops and constant operations within) yields O(n*m) where n is the number of elements in the list, and m is the number of sums (from adding elements in the sublist) that can be arranged from selecting elements into sublists. sums are keys in the inner dictionary and thus are not recounted in each inner dictionary.




* unit:
   * This folder contains all files required for the use of all unit classes.
      * An __init__.py file that stores strings for the names of unit types
      * basic_unit.py file with the BasicUnit class. This is the bedrock sprite class for all units. All the final actually used and spawned inherit from this class. All the final unit classes define their type with a string at the bottom for example: unit.unit_type["melee"] = melee
      * melee.py file with melee class, next level of complexity for a unit sprite, but also a finished unit sprite class itself. inherits from BasicUnit updates attributes in BasicUnit init (using super) and adds the a ‘range rect’ for detecting when a unit can damage another. 
      * archer.py file class archer inherits from melee, changes some attributes and increases size of range rect
      * heavy.py file class heavy in herits from melee as well. Has the special ability to ignore unit collision with enemies, unless they heavies as well or bases.
* media/art:
   * this folder contains the images for the sprites. The final ones used in the game were custom made, using the Spore game editor and a free imaging editing tool paint.net