# Required Functionality:
# List leaderboard
# Record matches
# Add players

import logging
import os.path
import sys

import leaderboard
import match
import player
import ranking

leaderboard = leaderboard.Leaderboard() 

def print_menu():

    print("########## MENU ###########")
    print("# 1. Display League Table #")
    print("# 2. Record Match Result  #")
    print("# 3. Add New Player       #")
    print("# 4. List Match History   #")
    print("# 5. Exit                 #")
    print("###########################\n")

    selection = 0

    while selection not in range(1, 5):
        try:
            selection = int(input("Please enter a selection: "))

            if selection not in range(1, 5):
                print ("Please select a valid option to continue")
        except: 
            print("Please enter a digit to continue.")
    
    menu_selection_made(selection)
        
def print_leaderboard_rankings():
    print(leaderboard)

   # print_menu()

def record_new_match():
    p1Name = None
    p2Name = None  
    p1Score = None
    p2Score = None
            
    p1Name = input("Please enter the name of the first player (case sensitive): ")

    player1 = leaderboard.get_player_by_name(p1Name)

    while player1 is None: 
        print ("Unable to find player. Please ensure the name is correct.")
    
        p1Name = input("Please enter the name of the first player (case sensitive): ")

        player1 = leaderboard.get_player_by_name(p1Name)

    p2Name = input("Please enter the name of the second player (case sensitive): ")

    player2 = leaderboard.get_player_by_name(p2Name)

    while player2 is None or p2Name == p1Name: 
        
        if player2 == None:
            print ("Unable to find player. Please ensure the name is correct.")
        else:
            print ("Please enter a second player. Matches cannot be played against oneself.")

        p2Name = input("Please enter the name of the second player (case sensitive): ")

        player2 = leaderboard.get_player_by_name(p1Name)

    while p1Score is None:
        try: 
            p1Score = int(input("Please enter the score for player 1: "))
        except:
            print("Please ensure the score is a digit")

    while p2Score is None:
        try: 
            p2Score = int(input("Please enter the score for player 2: "))
        except:
            print("Please ensure the score is a digit")

    leaderboard.recordMatch(p1Name, p1Score, p2Name, p2Score)

    print_menu()

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

    input("Press enter to continue ")

    print_menu()

def print_match_history():
    playerName = input("Please enter the name of the player you would like to view the match history for (case sensitive): ")

    player = leaderboard.get_player_by_name(playerName)

    while player == None: 
        print("Unable to find player. Please ensure the player exists and the name is typed correctly")

        playerName = input("Please enter the name of the player you would like to view the match history for (case sensitive): ")

        player = leaderboard.get_player_by_name(playerName)

    player.get_match_history()

def initialise():
    # An interesting alternative for a switch block, probably not the best way to do things
    # but an if/elif/else block doesn't feel like the most elegant way to solve it
    menuOptions = {
        1 : print_leaderboard_rankings,
        2 : record_new_match, 
        3 : add_new_player,
        4 : print_match_history,
        5 : sys.exit
    }

    return menuOptions

#############################################################################

menuOptions = initialise()
print_menu()
