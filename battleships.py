#!/usr/bin/python2

import sys
import os
from random import randint

def print_board(player_board, opponent_board, hitmiss, score_dic, fleet_list):
    '''
    prints the boards to the screen including scores and sunk ships
    '''
    alphabet = ["A","B","C","D","E","F","G","H","I","J"]
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        os.system('clear')
    elif sys.plaform.startswith('win'):
        os.system('clr')
    print("Tracking Board")
    for i in range(11): # prints the tracking board for the opponent to terminal
        line=""
        for j in range(11):
            if (i==0) and (j!=0):
                line+=" "+alphabet[j-1]+"  "
            elif (j==0) and (i!=0):
                line+="{:>2} |".format(i)
            elif (i==0) and (j==0):
                line+="    "
            else:
                if opponent_board[i-1][j-1] not in ["*", "#"]:
                    line+="   |" # for an "invisible game"
                    # comment the above and uncomment the line below to test:
                    # line+=" "+opponent_board[i-1][j-1]+" |"
                else:
                    line+=" "+opponent_board[i-1][j-1]+" |"
        print(line)
        print("   -----------------------------------------")

    print("\nYour Board:")
    for i in range(11): # prints your own board to terminal
        line=""
        for j in range(11):
            if (i==0) and (j!=0):
                line+=" "+alphabet[j-1]+"  "
            elif (j==0) and (i!=0):
                line+="{:>2} |".format(i)
            elif (i==0) and (j==0):
                line+="    "
            else:
                line+=" "+player_board[i-1][j-1]+" |"
        print(line)
        print("   -----------------------------------------")
    if hitmiss == "MISS":
        print(hitmiss)
    elif hitmiss in ["A","B","S","D","M"]:
        print("HIT")
        fleet_list = sunk_ships(score_dic,fleet_list)
    else:
        print("")


def create_board():
    '''
    creates a board and fills it with water "~"
    '''
    grid = []
    for i in range(10):
        grid.append(["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"])
    return grid

def char_convert(inputchar):
    '''
    converts the grid letters to numbers
    '''
    letterconversion = {"A": 1,
                        "B": 2,
                        "C": 3,
                        "D": 4,
                        "E": 5,
                        "F": 6,
                        "G": 7,
                        "H": 8,
                        "I": 9,
                        "J": 10}
    return letterconversion[inputchar.upper()]

def place_ship(lengthship, shipcharacter, origin, orientation, gridboard):
    '''
    places a ship onto the board with the starting letter of the ship.
    lengthship applies to the length of the ship, shipcharacter is the first character indicating the ship,
    origin is the starting point, orientation indicates either down(vertical) or to the right(horizontal)
    '''

    x = char_convert(origin[0])-1 # converts the x coordinate to the corresponding number from dictionary
    y = int(origin[1:])-1

    for i in range(lengthship):
        gridboard[y][x]=shipcharacter
        if orientation.lower()=="h":
            x+=1
        elif orientation.lower()=="v":
            y+=1
        else:
            raise Error('Orientation not recognised')


def shiplength(ship):
    ships = {"Aircraft Carrier": 5,
             "Battleship": 4,
             "Submarine":3,
             "Destroyer":3,
             "Minesweeper":2}
    return ships[ship]

def test_placement(lengthship, origin, orientation, gridboard):
    '''
    to check if the placement is actually valid
    '''
    x = char_convert(origin[0])-1
    y = int(origin[1:])-1

    if (x+lengthship>10) and (orientation == "h"):
        return False
    elif (y+lengthship>10) and (orientation == "v"): # this checks if ship is in given grid boundaries
        return False
    else:
        for i in range(lengthship):
            if gridboard[y][x] in ["A", "B", "S", "D", "M"]:
                return False
            elif orientation.lower()=="h":
                x+=1
            elif orientation.lower()=="v":
                y+=1
            else:
                raise Error('Orientation not recognised')
        return True

def random_board():
    '''
    creates a random board with random coordinates and direction
    '''
    randomboard=create_board()
    for boat in ['Aircraft Carrier','Battleship','Submarine','Destroyer','Minesweeper']:
        l = shiplength(boat)
        coordinate = random_coord()
        direction = ["v","h"][randint(0,1)]
        #print(coordinate)
        while not test_placement(l, coordinate, direction, randomboard):
            coordinate = ["A","B","C","D","E","F","G","H","I","J"][randint(0,9)]+str(randint(1,10))
            direction = ["v","h"][randint(0,1)]
            #print(coordinate)
        place_ship(l, boat[0], coordinate, direction, randomboard)
    return randomboard

def random_coord():
    '''
    creates a random coordinate
    '''
    return ["A","B","C","D","E","F","G","H","I","J"][randint(0,9)]+str(randint(1,10))

def shoot(coordinate, opponentboard):
    '''
    shooting at the opponent board, takes in coordinate you want to shoot and which board is being shut
    '''
    x = char_convert(coordinate[0])-1
    y = int(coordinate[1:])-1

    if opponentboard[y][x] == "~": #symbol for water
        opponentboard[y][x] = "#" #symbol for a miss
        return True, "MISS"
    elif opponentboard[y][x] not in ["~", "#", "*"]:
        ship = opponentboard[y][x]
        opponentboard[y][x] = "*" #symbol for a hit
        return True, ship
    else:
        return False, 0 # for completeness

def sunk_ships(dictionary_score, fleet_list):
    '''
    Takes in the dictionary score of player to determine which ships are sunk, also changes the afloat fleet
    to False when ship is sunk
    '''
    if (dictionary_score["A"] == 5) and (fleet_list[0]) :
        print("Aircraft Carrier sunk")
        fleet_list[0] = False
    elif (dictionary_score["B"] == 4) and (fleet_list[1]):
        print("Battleship sunk")
        fleet_list[1] = False
    elif (dictionary_score["S"] == 3) and (fleet_list[2]):
        print("Submarine sunk")
        fleet_list[2] = False
    elif (dictionary_score["D"] == 3) and (fleet_list[3]):
        print("Destroyer sunk")
        fleet_list[3] = False
    elif (dictionary_score["M"] == 2) and (fleet_list[4]):
        print("Minesweeper sunk")
        fleet_list[4] = False
    return fleet_list

def main():
    fleet_list_player = [True, True, True, True, True] #all player boats are afloat on water ~
    fleet_list_opponent = [True, True, True, True, True] #all opponent boats are afloat on water ~
    score_dic_player = {"A":0, "B":0, "S":0, "D":0, "M":0} #starting score for player
    score_dic_opponent = {"A":0, "B":0, "S":0, "D":0, "M":0} #starting score for opponent

    if raw_input('Do you want a random board? (Y/n) if not you can place your own ships').lower() == "n":
        player_board = create_board()
        for boat in ['Aircraft Carrier','Battleship','Submarine','Destroyer','Minesweeper']:
            print("Yo, fam... where do you want to place ur "+boat)
            coordinate = raw_input()
            print("Vertically (v) or horizontally (h)?")
            direction = raw_input()
            while not test_placement(shiplength(boat), coordinate, direction, player_board):
                print("Sorry, can't place that here!")
                print("So, where do you wanna place your "+boat+"?")
                coordinate = raw_input()
                print("Vertically (v) or horizontally (h)?")
                direction = raw_input()
            place_ship(shiplength(boat), boat[0], coordinate, direction, player_board)
            print(boat+" placed")
            print_board(player_board, create_board(), "", score_dic_player, fleet_list_player)
    else:
        player_board = random_board()

    opponent_board = random_board()

    # while both player scores are under 17, the game is going
    while (sum(score_dic_player.values()) < 17) and (sum(score_dic_opponent.values()) < 17):
        print_board(player_board, opponent_board, "", score_dic_player, fleet_list_player)

        print("Please enter a coordinate you want to shoot on the opponent board!")
        coordinate = raw_input()
        while coordinate == "":
            print("invalid Coordinate, try again")
            coordinate = raw_input()
        while (coordinate[0] not in ["A","B","C","D","E","F","G","H","I","J"],) and (int(coordinate[1:]) not in range(1,11)):
            print("invalid Coordinate, try again")
            coordinate = raw_input()

        # player shooting
        valid, value = shoot(coordinate, opponent_board)
        while not valid:
            print("You have tried to shoot here already! Please enter another coordinate value")
            coordinate = raw_input()
            valid, value = shoot(coordinate, opponent_board)
        if value in score_dic_player.keys():
            score_dic_player[value] += 1
        else:
            print(value)
        print_board(player_board, opponent_board, value, score_dic_player, fleet_list_player)
        raw_input("Player turn over, press Enter for Computer Turn")

        # opponent shooting
        valid, value = shoot(random_coord(), player_board)
        while not valid:
            valid, value = shoot(random_coord(), player_board)
        if value in score_dic_opponent.keys():
            score_dic_opponent[value] += 1
        else:
            print(value)
        print_board(player_board, opponent_board, value, score_dic_opponent, fleet_list_opponent)
        raw_input("Opponent turn over, press Enter for your Turn")

    # when while statement not true anymore and one player has shot everything, the game stops.
    print("GAME OVER")

if __name__ == "__main__":
    main()
