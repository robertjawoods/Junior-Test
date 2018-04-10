# Required Functionality:
# List leaderboard
# Record matches
# Add players

import sys
import os.path
import logging
import ranking
import player 
import match 
import leaderboard

# Configure logging for easier debugging 
logger = logging.getLogger("elo_ranking_interface")
logging.basicConfig(level=logging.INFO)

leaderboard = leaderboard.Leaderboard() 

def print_menu():

    print("########## MENU ###########")
    print("# 1. Display League Table #")
    print("# 2. Record Match Result  #")
    print("# 3. Add New Player       #")
    print("# 3. List Match History  #")
    print("# 5. Exit                 #")
    print("###########################\n")

    selection = 0

    while selection not in range(1, 5):
        try:
            selection = int(input("Please enter a selection:"))

            if selection not in range(1, 5):
                print ("Please select a valid option to continue")
        except: 
            print("Please enter a digit to continue.")
    
    menu_selection_made(selection)

        
def print_leaderboard_rankings():
    print("Not implemented")

def record_new_match():
    print("Not implemented")

def add_new_player():
    elo = 0
    
    addAnother = None
    
    while addAnother is not "N":
        response = None

        playerName = input("Please enter a name for the new player: ")
        while response not in ["Y", "N"]:
            response = input("Would you like to enter a starting ELO? N uses the default value of 1200 (Y/N): ")

            if response is "Y":
                while elo == 0:
                    try:
                        elo = float(input("Please enter the starting ELO for this player: "))
                    except:
                        print("Please enter a valid value for the starting ELO")
            elif response is "N":
                elo = 1200

        newPlayer = player.Player(playerName, elo)

        leaderboard.add_player(newPlayer)

        addAnother = input("Would you like to add another player? (Y/N): ")

def menu_selection_made(selection):
    menuOptions[selection]()

    # Clear the console screen for a clearer interface 
    os.system("cls")

    print_menu()

def initialise():
    try: 
        os.path.isfile("leaderboard.txt")
    except:
        logger.info("Unable to find log file")
        return None

    # An interesting alternative for a switch block, probably not the best way to do things
    # but an if/elif/else block doesn't feel like the most elegant way to solve it
    menuOptions = {
        1 : print_leaderboard_rankings,
        2 : record_new_match, 
        3 : add_new_player,
        5 : sys.exit
    }

    return menuOptions

#############################################################################

menuOptions = initialise()
print_menu()