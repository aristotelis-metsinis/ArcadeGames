#
# Mini-project # 5: "Memory".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 5: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 26 Oct 2014
# Version: 10.0
#
# Implementation of card game: "Memory".
# 
# Two game "modes": play with "textual numbers" or 
# "images.
#

#---------------------------------------------------------
# Import the "simple gui" module.
import simplegui
# Import module, which contains functions that involve
# randomness.
import random
# Import module that contains additional mathematical
# operations.
import math

#---------------------------------------------------------
# Define and initialize global constants.

# Initialize global constants that will hold the "width"
# and "height" of the "canvas" ("deck of cards" - grid of 
# 16 "cards").
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 140
# "Memory" game of 16 "cards" (as global constant).
CARDS_NUMBER = 16
# Compute the "width" of a single cell of this grid;
# "placeholder" for a single "card" (cells distributed 
# evently).
CARD_PLACEHOLDER_WIDTH = (CANVAS_WIDTH // CARDS_NUMBER)

# Set general "draw" properties.
FONT_SIZE = 50 
FONT_FACE = 'sans-serif'
FONT_COLOR = 'White'
MARGIN_Y = 19
# Compute the (global constant) "vertical" position to 
# draw a "card", presenting a "textual number" and taking 
# into consideration the height of the "deck of cards" 
# plus a "margin".
CARD_VALUE_POINT_Y = (CANVAS_HEIGHT // 2) + MARGIN_Y 
# More general "draw" properties.
CARD_PLACEHOLDER_LINE_COLOR = 'Black'
CARD_PLACEHOLDER_FILL_COLOR = 'Green'
CARD_PLACEHOLDER_LINE_WIDTH = 2

# Initialize a "dictionary" as global constant, mapping 
# numbers from 0-7 (acting as "keys") to "urls" (acting
# as "values"). In practice, the business logic of the
# program models generally the "deck of cards" as a 
# "shuffled" list consisting of 16 numbers with each 
# number lying in the range [0,8) and appearing twice.
# The following "urls" (links to images) 
# are just being used at the "presentation" layer, 
# drawing the proper "image" instead of "number" (text).
IMAGES = {}
IMAGES[0] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/riemann.jpg')
IMAGES[1] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/aristotle.jpg')
IMAGES[2] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/euler.jpg')
IMAGES[3] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/gauss.jpg')
IMAGES[4] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/newton.jpg')
IMAGES[5] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/einstein.jpg')
IMAGES[6] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/hilbert.jpg')
IMAGES[7] = simplegui.load_image('http://aristotelis-metsinis.github.io/img/lagrange.jpg')

#---------------------------------------------------------
# Define and initialize global variables.

# Boolean flag: play the game with "images" (True) or
# with "textual numbers" (False).
play_with_images = False

#---------------------------------------------------------

def new_game():
    """
    Helper function that starts and restarts the
    game, initializing global variables; reshuffle the 
    "cards", reset the "turn" counter and restart the 
    game. All "cards" should start the game hidden.
    """
    
    # Initialize global variable that will hold the "deck
    # of cards"; we model the "deck of cards" as a list 
    # consisting of 16 numbers with each number lying in 
    # the range [0,8) and appearing twice. The list is
    # created by concatenating two lists with range [0,8) 
    # together. Although Player can play the game with
    # "textual numbers" or "images", the above mentioned 
    # technique is being used modeling the game in both
    # game "modes".    
    global deck_of_cards
    deck_of_cards = range(CARDS_NUMBER // 2) + range(CARDS_NUMBER // 2)
    # Shuffle the "deck".
    random.shuffle(deck_of_cards)
    # Remove comment if in DEBUG mode.
    #print deck_of_cards
    
    # Initialize global variable that will hold the a list,
    # with size equal to the size of the "deck of cards"
    # consisting of boolean values. The boolean value
    # at a certain list index indicates whether the "card"
    # is "exposed" (True) or not (False). Particularly,
    # the ith entry should be "True" if the ith card is 
    # face up and its value is visible or "False" if the 
    # ith card is face down and it's value is hidden. 
    global deck_of_cards_exposed
    deck_of_cards_exposed = [False] * CARDS_NUMBER
    
    # Initialize global variable that will hold the game
    # state (0,1 and 2), i.e. beginning of the game, single 
    # "exposed" unpaired "card" and end of a "turn" 
    # respectively (have a look at the comments of 
    # "mouseclick()" for a detailed description 
    # concerning this variable).
    global state
    state = 0  
    
    # Initialize global variable that will hold the number
    # of "turns" playing the game.
    global turn 
    turn = 0
    label.set_text("Turns = " + str(turn))
    
    # Initialize global variable that will hold a "helper"
    # list, keeping the index of the cards "exposed" in 
    # a single "turn". 
    global index_of_cards_exposed_in_a_turn 
    index_of_cards_exposed_in_a_turn = [-1, -1]
    
    return None

#---------------------------------------------------------

def mouseclick(pos):
    """ 
    Define "mouse click" event handler; implements game 
    "state" logic. It receives a parameter; pair of screen 
    coordinates, i.e. a tuple of two non-negative integers
    - the position of the mouse click.
    """
    
    # User clicks on a "card" of the "deck" (grid of 
    # evenly distributed cells - cards placeholders).
    # Compute the index of this "card", i.e. determine 
    # which card have been clicked on with the mouse.
    # Recall that the sequence of cards entirely fills 
    # the "canvas".
    clicked_card_index = int(math.floor(float(pos[0]) / CARD_PLACEHOLDER_WIDTH))
    
    # If user clicks on a card already "exposed"; ignore 
    # event and "return" function immediately.
    if deck_of_cards_exposed[clicked_card_index]:
        return None
    
    # The counter of "turns" playing the game will be
    # updated as a global variable.
    global turn

    # The following block implements the game logic for 
    # selecting two "cards" and determining if they match. 
    # State 0 corresponds to the start of the game. 
    # In state 0, if you click on a card, that card is 
    # exposed, and you switch to state 1. 
    # State 1 corresponds to a single exposed unpaired 
    # card.     
    # In state 1, if you click on an unexposed card, that 
    # card is exposed and you switch to state 2. 
    # State 2 corresponds to the end of a turn. 
    # In state 2, if you click on an unexposed card, that 
    # card is exposed and you switch to state 1.
    global state  
    if state == 0:
        # Set the "status" of the clicked "card"
        # as "exposed". 
        deck_of_cards_exposed[clicked_card_index] = True
        
        # Store the "index" of the "exposed" card.
        # This is the first card "exposed" in this "turn" 
        # of the game.
        index_of_cards_exposed_in_a_turn[0] = clicked_card_index
        
        # Update "turn" counter; incremented after the 
        # first "card" is flipped during a turn.
        turn += 1
        label.set_text("Turns = " + str(turn))
        
        # Switch to the next game "state".
        state = 1
    elif state == 1:
        # Set the "status" of the clicked "card"
        # as "exposed".        
        deck_of_cards_exposed[clicked_card_index] = True

        # Store the "index" of the "exposed" card.
        # This is the second card "exposed" in this "turn" 
        # of the game.        
        index_of_cards_exposed_in_a_turn[1] = clicked_card_index
        
        # Switch to the next game "state".
        state = 2
    else:
        # Set the "status" of the clicked "card"
        # as "exposed".                
        deck_of_cards_exposed[clicked_card_index] = True

        # Get the value of the cards exposed in the previous
        # "turn" of the game (taking advantage of the 
        # "indexes" stored). Then determine if the previous
        # two "exposed" cards are paired or unpaired.  
        # If unpaired then switch the "status" of these 
        # cards back to "unexposed"; i.e. flip them back 
        # over so that they are hidden before moving to 
        # state 1.
        if deck_of_cards[index_of_cards_exposed_in_a_turn[0]] != deck_of_cards[index_of_cards_exposed_in_a_turn[1]]:
            deck_of_cards_exposed[index_of_cards_exposed_in_a_turn[0]] = False
            deck_of_cards_exposed[index_of_cards_exposed_in_a_turn[1]] = False
        
        # Store the "index" of the "exposed" card.
        # This is the first card "exposed" in this "turn" 
        # of the game, i.e. replace the "index" of the 
        # first card "exposed" in the previous "turn" of
        # the game.
        index_of_cards_exposed_in_a_turn[0] = clicked_card_index
      
        # Update "turn" counter; incremented after the 
        # first "card" is flipped during a turn.
        turn += 1
        label.set_text("Turns = " + str(turn))
        
        # Switch to the next game "state".
        state = 1
                
    return None   

#---------------------------------------------------------

def draw(canvas):
    """
    Event handler that is responsible for all drawing.
    It receives the "canvas" object and draws the "deck of 
    cards" (grid) as a horizontal sequence of 16 evently 
    distributed cells - "card" placeholders. It also draws
    the "exposed" cards (if any) taking into consideration
    the "mode" of the game, i.e either drawing "textual
    numbers" or "images" in the "cells" of the "exposed" 
    cards (placeholders). "Cards" are logically 50 x 140 
    pixels in size based on the configurations set for 
    the purposes of this program.    
    """
    
    # Iterate through the "Memory deck" and draw all 16 
    # "card" placeholders.    
    for index in range(CARDS_NUMBER):
        # Store the position of the left and right border
        # of this cell (card placeholder).
        card_placeholder_left_x = CARD_PLACEHOLDER_WIDTH * index
        card_placeholder_right_x = CARD_PLACEHOLDER_WIDTH * (index + 1)
        
        # Check if the "card" of this cell has an "exposed"
        # (already) status.
        if deck_of_cards_exposed[index]:
            # Compute the position at the middle of this 
            # cell.
            card_placeholder_middle_x = (card_placeholder_right_x + card_placeholder_left_x) // 2 
            
            # Play the game with "textual numbers" instead
            # of "images".
            if not play_with_images:
                # Use the "index" of this "cell" as the 
                # "index" in the list of the "deck of 
                # cards" extracting the "card value".
                # Get the width of the "card value" text 
                # in pixels; useful in (later) computing 
                # the position to draw the "card value"
                # text - centered justified in the "cell" 
                # of each "card" (placeholder).
                card_value_textwidth_in_px = frame.get_canvas_textwidth(str(deck_of_cards[index]), 
                                                                        FONT_SIZE, FONT_FACE)   
                card_value_point_x = card_placeholder_middle_x - (card_value_textwidth_in_px // 2)     
                # Draw the "textual number" associated 
                # with each "card" on the "canvas".
                canvas.draw_text(str(deck_of_cards[index]), (card_value_point_x, CARD_VALUE_POINT_Y), 
                                 FONT_SIZE, FONT_COLOR, FONT_FACE)
            
            # Play the game with "images" in place of 
            # "textual numbers".
            else:
                # Use the "index" of this "cell" as the 
                # "index" in the list of the "deck of 
                # cards" extracting the "card value".
                # Later use this "card value" as the "key"
                # loading the corresponding "image".  
                image = IMAGES[deck_of_cards[index]]
                # Draw the "image" associated with each 
                # "card" on the "canvas".
                canvas.draw_image(image,
                             (image.get_width() // 2,image.get_height() // 2), 
                             (image.get_width(), image.get_height()),
                             (card_placeholder_middle_x, CANVAS_HEIGHT // 2),
                             (image.get_width(), image.get_height()))

        # "Card" of this cell is not "exposed" (already);
        # simply draw a cell ("card" placeholder).                 
        else:
            card_placeholder_points = [[card_placeholder_left_x, 0], 
                                       [card_placeholder_right_x, 0], 
                                       [card_placeholder_right_x, CANVAS_HEIGHT], 
                                       [card_placeholder_left_x, CANVAS_HEIGHT]]
            # Just draw a blank green rectangle.
            canvas.draw_polygon(card_placeholder_points, 
                                CARD_PLACEHOLDER_LINE_WIDTH, 
                                CARD_PLACEHOLDER_LINE_COLOR, 
                                CARD_PLACEHOLDER_FILL_COLOR)   	     
    
    return None

#---------------------------------------------------------

def switch_game_mode():
    """
    Button event handler that updates properly the boolean
    flag, which "keeps" the "mode" of the game. The game
    has two modes: play with "textual numbers" (False) 
    or "images" (True). Each time button is pressed the
    value of this variable changes from "True" to "False"
    and vice versa. The button text is updated 
    accordingly.    
    """
    
    # The boolean flag will be updated as a global 
    # variable. If already "True", will be "False" (and 
    # vice versa).    
    global play_with_images
    play_with_images = not play_with_images
        
    if play_with_images:
        # User will play this game with "images". Update
        # button text informing the user that he/she will
        # reset the on-going game and play the next 
        # game with "textual numbers".
        switch_game_mode_button.set_text("Reset and Play with numbers")
    else:
        # User will play this game with "textual numbers". 
        # Update button text informing the user that 
        # he/she will reset the on-going game and play 
        # the next game with "images".        
        switch_game_mode_button.set_text("Reset and Play with images")
   
    # Reset on-going game.    
    new_game()
    
    return None

#---------------------------------------------------------

# Create frame.
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, 
                               CANVAS_HEIGHT)

# Register event handlers for "control" elements and 
# frame buttons to "restart" and if necessary "switch" 
# the mode of the game. Once the game is over, you should 
# hit the "Reset" button to restart the game. 
frame.add_button("Reset", new_game)
frame.add_label("")
label = frame.add_label("Turns = 0")
frame.add_label("")
switch_game_mode_button = frame.add_button("Reset and Play with images", 
                                           switch_game_mode, 200)

# Register "event handler" that is responsible for the
# management of the mouse clicks on the "canvas".
frame.set_mouseclick_handler(mouseclick)

# Register the "event handler" that is responsible
# for all drawing.
frame.set_draw_handler(draw)

# Call "new_game()" ensuring that all variables are
# always initialized when the program starts running.
new_game()

# Start frame.
frame.start()

#---------------------------------------------------------