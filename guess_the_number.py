#
# Mini-project # 2: "Guess the number".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 2: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 5 Oct 2014
# Version: 6.0
#
# Two-player game: the first player thinks of a "secret" 
# number in some known "range", while the second player 
# attempts to "guess" the number. After each "guess", the 
# first player answers either "Higher", "Lower" or 
# "Correct" depending on whether the "secret" number is 
# higher, lower or equal to the guess. Player is restricted 
# to a limited number of guesses.
# In this project, an interactive program has been built 
# where the "computer" takes the role of the first 
# player. A "user" plays as the second player, 
# interacting with the program using an "input" field and 
# several buttons. Computer's responses will be printed 
# in the console. 
#

#---------------------------------------------------------
# Import the "simple gui" module.
import simplegui
# Import module that contains functions, which involve
# randomness.
import random
# Import module that contains additional mathematical 
# operations.
import math

#---------------------------------------------------------
# Initialize global variables.

# Initialize global variable that will hold the upper 
# limit of the "range" of numbers of the game in progress.
# Note: when program starts, the game should immediately 
# begin in range [0, 100).
num_range = 100
# Initialize global variable that will hold the input 
# "guess" of the game in progress.
guess_number = -1
# Initialize global variable that will hold the random 
# number in the "range" of numbers of the game in progress.
secret_number = 0
# Initialize global variable that will hold the "remaining
# guesses" of the game in progress.
remaining_guesses = 0

#---------------------------------------------------------
 
def new_game():
    """ 
    Helper function that starts and restarts the 
    game. 
    """
    
    # Initialize global variable "secret_number" 
    # to be a random number in the range [0, <num_range>). 
    # Function "random.randrange()" returns a random 
    # integer "n" such that "start <= n < stop".
    global secret_number
    secret_number = random.randrange(0, num_range)
    
    # Player is restricted to a limited number of guesses.
    # Compute global variable "remaining_guesses" based upon
    # the desired "num_range" of the game in progress; 
    # once the player has used up those guesses, they lose.
    # Note: a "binary search" strategy for playing 
    # the game, approximately halves the range of possible 
    # "secret" numbers after each guess. So any "secret" 
    # number in the range [low, high) can always be found in 
    # at most "n" guesses, where "n" is the smallest integer 
    # such that "2 ^ n >= high - low + 1".
    global remaining_guesses
    remaining_guesses = math.log(num_range - 0 + 1) / math.log(2)
    remaining_guesses = int(math.ceil(remaining_guesses))

    # Print-out a blank line to separate consecutive games.
    print ""
    
    # Print-out proper message announcing the beginning of
    # a new game, the desired "range" of numbers and the
    # number of "remaining guesses".    
    print "New game. Range is from 0 to " + str(num_range)
    print "Number of remaining guesses is " + str(remaining_guesses)    
     
    # Enable this if in "Debug" mode.    
    #print "Secret number is " + str(secret_number)    
    
    return None

#---------------------------------------------------------

def range100():
    """ 
    Event handler for "button" that changes the "range" 
    to [0,100) and starts a new game. Whenever Player clicks 
    this "range" button, the current game stops and a 
    new game with the selected range begins.
    """        
        
    # Set the desired range for the "secret" number (as a 
    # global variable).
    global num_range
    num_range = 100  
     
    # Call "new_game()" to reset the "secret" number in the 
    # desired range.
    new_game()
        
    return None

#---------------------------------------------------------

def range1000():
    """ 
    Event handler for "button" that changes the "range" 
    to [0,1000) and starts a new game. Whenever Player clicks 
    this "range" button, the current game stops and a 
    new game with the selected range begins.
    """        
        
    # Set the desired range for the "secret" number (as a 
    # global variable).
    global num_range
    num_range = 1000  
     
    # Call "new_game()" to reset the "secret" number in the 
    # desired range.
    new_game()
        
    return None

#---------------------------------------------------------

def input_guess(guess):
    """ 
    Event hanlder for the "input" field; used to enter 
    "guesses". It takes the input string "guess", converts
    it to an integer, and prints out a message of the form 
    "Guess was <guess>". It also compares the entered number 
    to "secret_number" and prints out appropriate message.
    Finally, it may begin a new game if Player has either 
    won or run out of guesses.
    """

    # Initialize boolean variable; if player either wins or 
    # runs out of guesses, reset variable to "True";
    # i.e. start a new game.
    start_new_game = False
    
    # Store input "guess" into "guess_number" (as a 
    # global variable) and print-out proper message.
    # Note: no need to validate that the "input" number is 
    # in the correct "range" for the purposes of this project; 
    # that responsibility falls on the player.
    global guess_number
    guess_number = int(guess)
    print ""
    print "Guess was " + guess
    
    # Recompute "remaining_guesses" (as a global variable) and
    # print-out proper message.    
    global remaining_guesses
    remaining_guesses = remaining_guesses - 1 
    print "Number of remaining guesses is " + str(remaining_guesses)  
    
    # Once player has used up all guesses, a new game  
    # begins "immediately" after this try.
    if (remaining_guesses == 0):
        start_new_game = True   

    # Compare the entered number to "secret_number"
    # and print out an appropriate message such as 
    # "Higher", "Lower", or "Correct", etc.              
    if (secret_number < guess_number): 
        if (remaining_guesses > 0):
            print "Lower!"
        else:
            print "You ran out of guesses. The number was " + str(secret_number)                                
    elif (secret_number > guess_number):
        if (remaining_guesses > 0):
            print "Higher!"
        else:
            print "You ran out of guesses. The number was " + str(secret_number)
    else:
        print "Correct!"
        # Player has won this game; start a new one
        # "immediately" after this try.
        start_new_game = True
           
    # Player has either won or run out of guesses; 
    # a new game with the same "range" as the last one  
    # immediately begins by calling "new_game()".
    if (start_new_game):
        new_game()
    
    return None

#---------------------------------------------------------

# Create frame.
frame = simplegui.create_frame("Guess the number", 200, 200)

# Register event handlers for control elements and start 
# frame buttons to restart the game allowing the player to 
# choose two different ranges for the "secret" number.
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)                 
                 
# Start frame.
frame.start()
    
# Call "new_game()" ensuring that "secret_number" variable 
# is always initialized when the program starts running.
new_game()

##########################################################

# Test code by calling the function "input_guess()" 
# repeatedly in the program with different player choices 
# as its input arguments. Uncomment each sequence of calls
# and check whether the output in the console matches that
# provided in the comments below.
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-gtn_testing_template.py

#---------------------------------------------------------
#---------------------------------------------------------
# Test # 1.

#secret_number = 74	
#input_guess("50")
#input_guess("75")
#input_guess("62")
#input_guess("68")
#input_guess("71")
#input_guess("73")
#input_guess("74")

#---------------------------------------------------------
# Output from test # 1.

#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Higher!
#
#Guess was 75
#Number of remaining guesses is 5
#Lower!
#
#Guess was 62
#Number of remaining guesses is 4
#Higher!
#
#Guess was 68
#Number of remaining guesses is 3
#Higher!
#
#Guess was 71
#Number of remaining guesses is 2
#Higher!
#
#Guess was 73
#Number of remaining guesses is 1
#Higher!
#
#Guess was 74
#Number of remaining guesses is 0
#Correct!
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7

#---------------------------------------------------------
#---------------------------------------------------------
# Test # 2.

#range1000()
#secret_number = 375	
#input_guess("500")
#input_guess("250")
#input_guess("375")

#---------------------------------------------------------
# Output from test # 2.

#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10
#
#Guess was 500
#Number of remaining guesses is 9
#Lower!
#
#Guess was 250
#Number of remaining guesses is 8
#Higher!
#
#Guess was 375
#Number of remaining guesses is 7
#Correct!
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10

#---------------------------------------------------------
#---------------------------------------------------------
# Test # 3.

#secret_number = 28	
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")

#---------------------------------------------------------
# Output from test # 3.

#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Lower!
#
#Guess was 50
#Number of remaining guesses is 5
#Lower!
#
#Guess was 50
#Number of remaining guesses is 4
#Lower!
#
#Guess was 50
#Number of remaining guesses is 3
#Lower!
#
#Guess was 50
#Number of remaining guesses is 2
#Lower!
#
#Guess was 50
#Number of remaining guesses is 1
#Lower!
#
#Guess was 50
#Number of remaining guesses is 0
#You ran out of guesses.  The number was 28
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7

##########################################################
