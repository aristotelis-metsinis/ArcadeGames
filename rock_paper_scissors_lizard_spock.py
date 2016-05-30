#
# Mini-project # 1: "Rock-paper-scissors-lizard-Spock".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 1: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 28 Sep 2014
# Version: 6.0
#
# "Rock-paper-scissors-lizard-Spock" (RPSLS) is a variant of 
# "Rock-paper-scissors" that allows five choices. Each choice wins 
# against two other choices, loses against two other choices and 
# ties against itself.
#
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
#
# Each choice wins against the preceding two choices and loses against 
# the following two choices (if "rock" and "scissors" are thought of as 
# being adjacent using "modular arithmetic").
#

#---------------------------------------------------------
# Import module that contains functions, which involve 
# randomness.
import random

#---------------------------------------------------------

def name_to_number(name):
    """
    Helper function that converts the string "name" into 
    a "number" between "0" and "4" in the way described below. 
        
    0 - rock
    1 - Spock
    2 - paper
    3 - lizard
    4 - scissors		
    """
       
    # Define a variable that will hold the computed "number"
    # and initialise it. Normally, after the execution of this
    # function, "number" should have one of the following 
    # values: 0,1,2,3,4 depending on player's choice, or "-1" 
    # case of an invalid input.    
    number = -1
    
    # A sequence of "if/elif/else" clauses should be used
    # checking for conditions of the form 
    # name == '<player_choice>' to distinguish the cases. 
    # A final "else" clause catches cases when "name" 
    # does not match any of the five correct input strings.     
    if ( name == 'rock' ):
        number = 0
    elif ( name == 'Spock' ):
        number = 1
    elif ( name == 'paper' ):
        number = 2
    elif ( name == 'lizard' ):
        number = 3
    elif ( name == 'scissors' ):
        number = 4
    else:
        number = -1        
        
    # Return the computed "number".
    return number

#---------------------------------------------------------

def number_to_name(number):
    """
    Helper function that converts a "number" in the range 
    "0" to "4" into its corresponding (string) "name" 
    in the way described below. 
        
    0 - rock
    1 - Spock
    2 - paper
    3 - lizard
    4 - scissors		
    """
       
    # Define a variable that will hold the "name"
    # and initialise it. Normally, after the execution of 
    # this function, "name" should have one of the 
    # following values: "rock", "Spock", "paper", "lizard", "scissors" 
    # depending on the input "number", or "" in case of 
    # a "number" not in the correct range.    
    name = ""
    
    # A sequence of "if/elif/else" clauses should be used
    # checking for conditions of the form 
    # number == <input_value> to distinguish the cases. 
    # A final "else" clause catches cases when "number" is 
    # not in the correct range.              
    if ( number == 0 ):
        name = "rock"
    elif ( number == 1 ):
        name = "Spock"
    elif ( number == 2 ):
        name = "paper"
    elif ( number == 3 ):
        name = "lizard"
    elif ( number == 4 ):
        name = "scissors"
    else:
        name = ""        
        
    # Return "name".
    return name

#---------------------------------------------------------

def rpsls(player_choice): 
    """
    Main function that takes as input the string "player_choice", 
    which normally should be one of "rock", "paper", "scissors", 
    "lizard", or "Spock". The function then simulates playing a 
    round of "Rock-paper-scissors-lizard-Spock" by generating its 
    own random choice from these alternatives and then determining 
    the winner using a simple rule (as described in the comments 
    found at the top of this program).        
    """
    
    # Print-out a blank line to separate consecutive games.
    print ""
    # Print-out appropriate message describing player's choice.
    print "Player chooses " + player_choice
    
    # Compute the number "player_number" between "0" and "4" 
    # corresponding to player's choice by calling the 
    # helper function "name_to_number() using "player_choice".
    player_number = name_to_number( player_choice )
    
    # Confirm that player's choice is valid (i.e. within the [0,4] 
    # range); if not print proper "error" message.
    if (player_number >= 0) and (player_number <= 4):
        # Generate computer's guess by computing a random number 
        # "comp_number" between "0" and "4" that corresponds to 
        # computer's guess using function "random.randrange()" that
        # returns a random integer "n" such that "start <= n < stop".
        comp_number = random.randrange(0,5)
        
        # Confirm that computers's choice is valid (i.e. within the 
        # [0,4] range); if not print proper "error" message.
        if (comp_number >= 0) and (comp_number <= 4):
            
            # Print-out appropriate message for that guess by 
            # computing the name "comp_name" corresponding to 
            # computer's number using the function "number_to_name()"          
            comp_name = number_to_name(comp_number)            
            print "Computer chooses " + comp_name
            
            # Determine the winner by computing the 
            # difference between "player_number" and "comp_number"   
            # taken modulo five and using "if/elif/else" statement
            # whose conditions test the various possible values of this
            # difference. Then print an appropriate message 
            # concerning the winner.    
            diff = ( player_number - comp_number ) % 5
            
            # "diff" is either "1" or "2" then "player" wins.
            if (diff == 1) or (diff  == 2):
                print "Player wins!"
            # else if "diff" is either "3" or "4" then "computer" wins.                
            elif (diff == 3) or (diff  == 4):
                print "Computer wins!"
            # else "tie" betwen "player" and "computer".
            else:
                print "Player and computer tie!"                            
        else: 
            print "Error: invalid computer's choice!"
    else: 
        print "Error: invalid player's choice!"
    
    return None

#--------------------------------------------------------- 

# Test code by calling the main function "rpsls()" repeatedly in the program 
# with different player choices as its input arguments, generating different 
# computer guesses and different winners each time.
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
