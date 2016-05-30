#
# Mini-project # 6: "Blackjack".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 6: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 2 Nov 2014
# Version: 13.0
#
# Implementation of card game: "Blackjack".
#
# "Cards" in "Blackjack" have the following values: an "ace"
# may be valued as either 1 or 11 (player's choice), "face"
# cards (kings, queens and jacks) are valued at 10 and the
# value of the remaining cards corresponds to their number.
#
# During a round of "Blackjack", the players plays against
# a "Dealer" with the goal of building a "Hand" (a 
# collection of "Cards") whose cards have a total value 
# that is higher than the value of the dealer's "Hand", but 
# not over 21. A round of "Blackjack" is also sometimes 
# referred to as a "Hand".
#
# The game logic for this simplified version of "Blackjack"
# is as follows: 
# * The "Player" and the "Dealer" are each dealt two "Cards"
# initially with one of the dealer's cards being dealt 
# faced down (his hole card). 
# * The "Player" may then ask for the "Dealer" to 
# repeatedly "hit" his "Hand" by dealing him another "Card".
# * If, at any point, the value of the player's "Hand" 
# exceeds 21, the "Player" is "busted" and loses 
# immediately. 
# * At any point prior to busting, the "Player" may "stand"
# and the "Dealer" will then hit his "Hand" until the 
# value of his "Hand" is 17 or more. For the "Dealer", "aces" 
# count as 11 unless it causes the dealer's "Hand" to bust.
# * If the "Dealer" busts, the "Player" wins. Otherwise, 
# the "Player" and "Dealer" then compare the values of 
# their "Hands" and the "Hand" with the higher value wins. The 
# "Dealer" wins ties in this version.
#

#---------------------------------------------------------
# Import the "simple gui" module.
import simplegui
# Import module, which contains functions that involve
# randomness.
import random

#---------------------------------------------------------
# Define and initialize global constants.

# Moad "Card" sprite: 936 x 384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# Define globals for "Cards".
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Initialize global constant that will hold the "title"
# of the game.
GAME_TITLE = "Blackjack"

# Initialize global constants that will hold the "width"
# and "height" of the "canvas" ("deck of cards").
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# Initialize global constants that will hold general 
# "draw" properties.
X_MARGIN = 10
Y_MARGIN = 20
Y_MARGIN_PLUS = 30
FONT_SIZE = 25
TITLE_FONT_SIZE = 50
FONT_COLOR = 'White'
TITLE_FONT_COLOR = 'Orange'
OUTCOME_FONT_COLOR = 'Yellow'
FONT_FACE = 'sans-serif'
CANVAS_BACKGROUND = "Green"
BUTTON_WIDTH = 200

# Define game messages.
INVALID_CARD = "Invalid card: "
HAND_CONTAINS = "Hand contains "
DECK_CONTAINS = "Deck contains "
HIT_OR_STAND = "Player, hit or stand ?"
NEW_DEAL = "Player, new deal ?"
PLAYER_WINS = "Player, you win."
PLAYER_LOSES = "Player, you lose." 
PLAYER_BUSTED = "Player, you have busted."
DEALER_BUSTED = "Dealer busted."
EARLY_DEAL_1  = "Deal during the middle of"
EARLY_DEAL_2 = "the round."

# Player wins or loses these points.
SCORE_POINTS = 1

#---------------------------------------------------------
# Define and initialize global variables.

# Initialize global variable that will keep track of 
# whether the player's "Hand" is still being played.
in_play = False
# Used for drawing text messages on the "canvas".
outcome = outcome_plus = outcome_plus_plus = ""
# These messages should prompt the "Player" to take some
# required action.
action = ""
# Initialize global variable that will keep track of
# wins and losses for Blackjack's session (wins minus 
# losses).
score = 0

#---------------------------------------------------------

class Card:
    """
    Define "Card" class.
    """

    #-----------------------------------------------------

    def __init__(self, suit, rank):
        """
        Create and initialize a "Card" object of a 
        specific "suit" and "rank".
        """
        
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            
            global outcome
            outcome = INVALID_CARD, suit, rank

    #-----------------------------------------------------            

    def __str__(self):
        """ 
        Return a string representation of a "Card" object 
        in a human-readable form.
        """        
        
        return self.suit + self.rank

    #-----------------------------------------------------
    
    def get_suit(self):
        """
        Return "Card's" suit.
        """
        
        return self.suit

    #-----------------------------------------------------
    
    def get_rank(self):
        """
        Return "Card's" rank.
        """
        
        return self.rank

    #-----------------------------------------------------
    
    def draw(self, canvas, pos):
        """
        Draw a "Card" object on the "canvas" at the 
        specific "pos" (position of the upper left corner).
        """        
        
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, 
                          CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], 
                           pos[1] + CARD_CENTER[1]], 
                          CARD_SIZE)
        return None
        
#---------------------------------------------------------

class Hand:
    """
    Define "Hand" class.
    """
    
    #-----------------------------------------------------
    
    def __init__(self):
        """
        Create and initialize the "Hand" object to have
        an empty list of "Card" objects.
        """
         
        self.hand = []

    #-----------------------------------------------------
    
    def __str__(self):
        """ 
        Return a string representation of a "Hand" object 
        in a human-readable form.
        """
        
        string_representation = HAND_CONTAINS
        for card in self.hand:
            string_representation += str(card) + " "    	        
        
        return string_representation

    #-----------------------------------------------------
    
    def add_card(self, card):
        """ 
        Append a "Card" object to a "Hand" object (list of 
        "Card" objects).
        """
        
        self.hand.append(card)
        
        return None

    #-----------------------------------------------------
    
    def get_value(self):
        """
        Compute the value of the "Hand" object.
        Use the provided "VALUE" dictionary to look up the
        value of a single "Card" to compute the value of a
        "Hand". Count "aces" as 1, if the "Hand" has an 
        "ace", then add 10 to "Hand" value if it doesn't 
        bust. Note: in practice never count two "aces" as 
        "11".
        """
               
        value = 0
        ace = False

        for card in self.hand:
            value += VALUES[card.get_rank()]
            
            if (card.get_rank() == 'A'):
                ace = True
        
        if not ace:
            return value
        else:
            if (value + 10) <= 21:
                return (value + 10)
            else:
                return value
            
    #-----------------------------------------------------
    
    def draw(self, canvas, pos):
        """
        Draw a "Hand" object on the "canvas" by using 
        the "draw" method for "Cards".
        """
                      
        # Draw a "Hand" as a horizontal sequence of "Cards" 
        # where the parameter "pos" is the position of the
        # upper left corner of the leftmost "Card".  
        # Note: assume generally that only the first five 
        # "Cards" of a player's "Hand" need to be visible 
        # on the "canvas".
        for card in self.hand:
            card.draw(canvas, pos)            
            pos[0] += CARD_SIZE[0] + X_MARGIN
        
        return None	

#---------------------------------------------------------

class Deck:
    """
    Define "Deck" class.
    """

    #-----------------------------------------------------
    
    def __init__(self):
        """ 
        Create and initialize a "Deck" object as list of 
        "Cards" generated by a "list" comprehension method
        and using the "Card" initializer to create the 
        "Cards".
        """
        
        self.deck = [Card(suit,rank) for suit in SUITS for rank in RANKS]
        
    #-----------------------------------------------------
    
    def shuffle(self):
        """ 
        Shuffle the "Deck".
        """
        
        random.shuffle(self.deck)
        
        return None
    
    #-----------------------------------------------------
    
    def deal_card(self):
        """
        Deal a "Card" object from the "Deck".
        """
        
        return self.deck.pop()

    #-----------------------------------------------------
        
    def __str__(self):
        """        
        Return a string representation of a "Deck" object 
        in a human-readable form.        
        """
        
        string_representation = DECK_CONTAINS        
        for card in self.deck:
            string_representation += str(card) + " "    	        
        
        return string_representation

#---------------------------------------------------------
    
def deal():
    """
    Event handler for "Deal" button that shuffles the 
    "Deck" and "deals" the two "Cards" to both the "Dealer" 
    and the "Player". 
    """
    
    # Update messages, score and the player's "Hand" status
    # as global variables.
    global outcome, outcome_plus, outcome_plus_plus, in_play, score, action 
    outcome = outcome_plus = outcome_plus_plus = ""
    action = HIT_OR_STAND
    
    # If the "Deal" button is clicked during the middle of 
    # a round the program reports that the "Player" lost 
    # the round and updates the "score" appropriately.
    if in_play:
        outcome = PLAYER_LOSES                        
        outcome_plus = EARLY_DEAL_1
        outcome_plus_plus = EARLY_DEAL_2
        score -= SCORE_POINTS
    else:
        in_play = True
    
    # Create and shuffle the "Deck" (stored as a global 
    # variable). Avoids the situation where the "Deck" 
    # becomes empty during play.
    global deck_of_cards
    deck_of_cards = Deck()
    deck_of_cards.shuffle()
      
    # Create new "Player" and "Dealer" Hands (stored as 
    # global variables). 
    global player, dealer
    player = Hand()
    dealer = Hand()
    
    # Add two "Cards" to each "Hand". To transfer a "Card" 
    # from the "Deck" to a "Hand", the "deal_card()" 
    # method of the "Deck" class and the "add_card()" 
    # method of "Hand" class are being used in 
    # combination. 
    player.add_card(deck_of_cards.deal_card())
    dealer.add_card(deck_of_cards.deal_card())
    player.add_card(deck_of_cards.deal_card())
    dealer.add_card(deck_of_cards.deal_card())
        
    # Print resulting "Hands" to the console with an 
    # appropriate message indicating which "Hand" is which.
    # Remove comments if in DEBUG mode.
    #print "Player: " + str(player)
    #print "Dealer: " + str(dealer)    
          
    return None

#---------------------------------------------------------

def hit():
    """
    Event handler for "Hit" button. If the value of the 
    "Hand" is less than or equal to 21, clicking this 
    button adds an extra card to player's "Hand". 
    If the value exceeds 21 after being hit, "You have 
    busted" is get printed.   
    """
    
    # Update messages, score and the player's "Hand" status
    # as global variables.
    global outcome, outcome_plus, outcome_plus_plus, in_play, score, action  
    
    # If the "Hand" is in play, hit the "player".    
    if in_play:
        outcome = outcome_plus = outcome_plus_plus = ""
        player.add_card(deck_of_cards.deal_card())
    else:
        return None
   
    # If busted, update messages, score and the player's 
    # "Hand" status.
    if player.get_value() > 21:
        outcome = PLAYER_BUSTED
        outcome_plus = outcome_plus_plus = ""
        action = NEW_DEAL                
        score -= SCORE_POINTS
        in_play = False
        
    return None

#---------------------------------------------------------

def stand():
    """
    Event handler for "Stand" button. If the "Player" has 
    busted, remind the "Player" that they have busted. 
    Otherwise, repeatedly hit the "Dealer" until his 
    "Hand" has value 17 or more. If the "Dealer" busts, let 
    the "Player" know. Otherwise, compare the value of the 
    player's and dealer's "Hands". If the value of the 
    player's "Hand" is less than or equal to the dealer's 
    "Hand", the "Dealer" wins. Otherwise the "Player" has
    won. Note: the "Dealer" wins ties in this game version.
    """
    
    # Update message, score and the player's "Hand" status
    # as global variables.
    global outcome, outcome_plus, outcome_plus_plus, in_play, score, action 
    
    # If the "Player" has busted, remind the "Player" that 
    # they have busted.
    if player.get_value() > 21:
        outcome = PLAYER_BUSTED
        outcome_plus = outcome_plus_plus = ""
        action = NEW_DEAL
    elif in_play:
    # If the "Hand" is in play, repeatedly hit "Dealer" 
    # until his "Hand" has value 17 or more.    
        while dealer.get_value() < 17:
            dealer.add_card(deck_of_cards.deal_card())

        # If busted, update messages, score and the 
        # player's "Hand" status.   
        if dealer.get_value() > 21:
            outcome = PLAYER_WINS
            outcome_plus = DEALER_BUSTED
            outcome_plus_plus = ""
            action = NEW_DEAL                        
            score += SCORE_POINTS  
            in_play = False
        # Else compare the value of the 
        # player's and dealer's "Hands". If the value of 
        # the player's "Hand" is less than or equal to 
        # the dealer's "Hand", the "dealer" wins. 
        # Otherwise the "player" has won. Again,
        # update messages, score and the player's "Hand" 
        # status. 
        else:   
            in_play = False
            action = NEW_DEAL
            outcome_plus = outcome_plus_plus = ""
            if player.get_value() > dealer.get_value():
                outcome = PLAYER_WINS                                
                score += SCORE_POINTS                
            else:
                outcome = PLAYER_LOSES                                
                score -= SCORE_POINTS
                                
    return None
                
#---------------------------------------------------------

def draw(canvas):
    """
    Event handler that is responsible for all drawing.
    It receives the "canvas" object and draws message(s)
    to the "Player", the "title" and the "score" of the game
    as well as draws the resulting "Hands" with  
    appropriate titles indicating which "Hand" is which.    
    """  
        
    canvas.draw_text(outcome, 
                     (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 5), 
                     FONT_SIZE, OUTCOME_FONT_COLOR, FONT_FACE)

    canvas.draw_text(outcome_plus,
                     (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 4),
                     FONT_SIZE, OUTCOME_FONT_COLOR, FONT_FACE)

    canvas.draw_text(outcome_plus_plus,
                     (CANVAS_WIDTH // 2, (CANVAS_HEIGHT // 4) + Y_MARGIN_PLUS),
                     FONT_SIZE, OUTCOME_FONT_COLOR, FONT_FACE)
    
    canvas.draw_text(GAME_TITLE, 
                     (CANVAS_WIDTH // 10, CANVAS_HEIGHT // 10), 
                     TITLE_FONT_SIZE, TITLE_FONT_COLOR, FONT_FACE)

    canvas.draw_text("Score: " + str(score), 
                     (CANVAS_WIDTH // 10 , CANVAS_HEIGHT // 5), 
                     FONT_SIZE, FONT_COLOR, FONT_FACE)
    
    canvas.draw_text("Dealer", 
                     (CANVAS_WIDTH // 10 , CANVAS_HEIGHT // 3), 
                     FONT_SIZE, FONT_COLOR, FONT_FACE)

    dealer.draw(canvas, [CANVAS_WIDTH // 10, CANVAS_HEIGHT // 3 + Y_MARGIN]) 
    
    canvas.draw_text("Player", 
                     (CANVAS_WIDTH // 10 , CANVAS_HEIGHT // 3 + 3 * Y_MARGIN + CARD_SIZE[1]), 
                     FONT_SIZE, FONT_COLOR, FONT_FACE)
      
    player.draw(canvas, [CANVAS_WIDTH // 10, CANVAS_HEIGHT // 3 + 4 * Y_MARGIN + CARD_SIZE[1]])    

    canvas.draw_text(action, 
                     (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 3 + 3 * Y_MARGIN + CARD_SIZE[1]),  
                     FONT_SIZE, TITLE_FONT_COLOR, FONT_FACE)
     
    # If the round is still in play, an image of the back 
    # of a "Card" should be drawn over the dealer's first
    # (hole) "Card" to hide it. Once the round is over, 
    # the dealer's hole "Card" should be displayed.        
    if in_play:
        card_loc = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, 
                          CARD_SIZE, 
                          [CANVAS_WIDTH // 10 + CARD_CENTER[0], 
                           CANVAS_HEIGHT // 3 + Y_MARGIN + CARD_CENTER[1]], 
                          CARD_SIZE)        
    
    return None    
    
#---------------------------------------------------------

# Create and initialize frame.
frame = simplegui.create_frame("Blackjack", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background(CANVAS_BACKGROUND)

# Register event handlers for "control" elements and
# frame buttons. 
# Create and shuffle a new "Deck" (or restock and shuffle 
# an existing deck) each time the "Deal" button is clicked.
# This change avoids the situation where the "Deck" becomes 
# empty during play.
frame.add_button("Deal", deal, BUTTON_WIDTH)
frame.add_label("")
frame.add_button("Hit",  hit, BUTTON_WIDTH)
frame.add_label("")
frame.add_button("Stand", stand, BUTTON_WIDTH)

# Register the "event handler" that is responsible
# for all drawing.
frame.set_draw_handler(draw)


# Get things rolling.
# A "Hand" is automatically dealt to the "Player" and 
# "Dealer" when the program starts via a call to the 
# "deal()" function during initialization.
deal()

# Start frame.
frame.start()

##########################################################
# Testing templates for classes.
#
# Uncomment each sequence of calls and check whether the
# output to the console matches that provided in the
# comments below.

#---------------------------------------------------------
#---------------------------------------------------------

# 1. Testing template for the "Card" class.
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-card_template.py

#c1 = Card("S", "A")
#print c1
#print c1.get_suit(), c1.get_rank()
#print type(c1)

#c2 = Card("C", "2")
#print c2
#print c2.get_suit(), c2.get_rank()
#print type(c2)

#c3 = Card("D", "T")
#print c3
#print c3.get_suit(), c3.get_rank()
#print type(c3)

#---------------------------------------------------------
# Output to console.

#SA
#S A
#<class '__main__.Card'>
#C2
#C 2
#<class '__main__.Card'>
#DT
#D T
#<class '__main__.Card'>

#---------------------------------------------------------
#---------------------------------------------------------

# 2. Testing template for the "Hand" class.
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-hand_template.py

#c1 = Card("S", "A")
#c2 = Card("C", "2")
#c3 = Card("D", "T")
#print c1, c2, c3
#print type(c1), type(c2), type(c3)

#test_hand = Hand()
#print test_hand

#test_hand.add_card(c1)
#print test_hand

#test_hand.add_card(c2)
#print test_hand

#test_hand.add_card(c3)
#print test_hand

#print type(test_hand)

#---------------------------------------------------------
# Output to console.
# Note that the string representation of a "Hand" will 
# vary based on how the "__str__" method has been 
# implemented.

#SA C2 DT
#<class '__main__.Card'> <class '__main__.Card'> <class '__main__.Card'>
#Hand contains 
#Hand contains SA 
#Hand contains SA C2 
#Hand contains SA C2 DT 
#<class '__main__.Hand'>

#---------------------------------------------------------
#---------------------------------------------------------

# 3. Testing template for the "Deck" class.
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-deck_template.py

#test_deck = Deck()
#print test_deck
#print type(test_deck)

#c1 = test_deck.deal_card()
#print c1
#print type(c1)
#print test_deck

#c2 = test_deck.deal_card()
#print c2
#print type(c2)
#print test_deck

#test_deck = Deck()
#print test_deck
#test_deck.shuffle()
#print test_deck
#print type(test_deck)

#c3 = test_deck.deal_card()
#print c3
#print type(c3)
#print test_deck

#---------------------------------------------------------
# Output to console.
# Output of string method for decks depends on the 
# implementation of "__str__" method.
# Note the output of shuffling is randomized so the exact
# order of "Cards" need not match.

#Deck contains CA C2 C3 C4 C5 C6 C7 C8 C9 CT CJ CQ CK SA S2 S3 S4 S5 S6 S7 S8 S9 ST SJ SQ SK HA H2 H3 H4 H5 H6 H7 H8 H9 HT HJ HQ HK DA D2 D3 D4 D5 D6 D7 D8 D9 DT DJ DQ DK 
#<class '__main__.Deck'>
#DK
#<class '__main__.Card'>
#Deck contains CA C2 C3 C4 C5 C6 C7 C8 C9 CT CJ CQ CK SA S2 S3 S4 S5 S6 S7 S8 S9 ST SJ SQ SK HA H2 H3 H4 H5 H6 H7 H8 H9 HT HJ HQ HK DA D2 D3 D4 D5 D6 D7 D8 D9 DT DJ DQ 
#DQ
#<class '__main__.Card'>
#Deck contains CA C2 C3 C4 C5 C6 C7 C8 C9 CT CJ CQ CK SA S2 S3 S4 S5 S6 S7 S8 S9 ST SJ SQ SK HA H2 H3 H4 H5 H6 H7 H8 H9 HT HJ HQ HK DA D2 D3 D4 D5 D6 D7 D8 D9 DT DJ 
#Deck contains CA C2 C3 C4 C5 C6 C7 C8 C9 CT CJ CQ CK SA S2 S3 S4 S5 S6 S7 S8 S9 ST SJ SQ SK HA H2 H3 H4 H5 H6 H7 H8 H9 HT HJ HQ HK DA D2 D3 D4 D5 D6 D7 D8 D9 DT DJ DQ DK 
#Deck contains CT H6 C4 H9 D6 HJ D2 S5 D8 H2 ST H4 HQ HK S8 D3 CJ D5 DK DQ DA S9 S6 S2 DJ C8 SJ C9 D4 C7 SK CK S3 CA SA S4 CQ S7 HA H3 C5 D9 DT H7 HT C2 SQ H8 C6 D7 C3 H5 
#<class '__main__.Deck'>
#H5
#<class '__main__.Card'>
#Deck contains CT H6 C4 H9 D6 HJ D2 S5 D8 H2 ST H4 HQ HK S8 D3 CJ D5 DK DQ DA S9 S6 S2 DJ C8 SJ C9 D4 C7 SK CK S3 CA SA S4 CQ S7 HA H3 C5 D9 DT H7 HT C2 SQ H8 C6 D7 C3 

#---------------------------------------------------------
#---------------------------------------------------------

# 4. Testing template for the "get_value" method for 
# "Hands".
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-getvalue_template.py

#c1 = Card("S", "A")
#c2 = Card("C", "2")
#c3 = Card("D", "T")
#c4 = Card("S", "K")
#c5 = Card("C", "7")
#c6 = Card("D", "A")

#test_hand = Hand()
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c2)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c5)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c3)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c4)
#print test_hand
#print test_hand.get_value()

#test_hand = Hand()
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c1)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c6)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c4)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c5)
#print test_hand
#print test_hand.get_value()

#test_hand.add_card(c3)
#print test_hand
#print test_hand.get_value()

#---------------------------------------------------------
# Output to console.
# Note that the string representation of a "Hand" may vary
# based on the implementation of the "__str__" method.

#Hand contains 
#0
#Hand contains C2 
#2
#Hand contains C2 C7 
#9
#Hand contains C2 C7 DT 
#19
#Hand contains C2 C7 DT SK 
#29
#Hand contains 
#0
#Hand contains SA 
#11
#Hand contains SA DA 
#12
#Hand contains SA DA SK 
#12
#Hand contains SA DA SK C7 
#19
#Hand contains SA DA SK C7 DT 
#29

##########################################################
