#
# Mini-project # 4: "Pong".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 4: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 19 Oct 2014
# Version: 11.0
#
# Implementation of the classic arcade game "Pong".
#

#---------------------------------------------------------
# Import the "simple gui" module.
import simplegui
# Import module, which contains functions that involve 
# randomness.
import random

#---------------------------------------------------------
# Define and initialize global constants.

# Initialize global constants that will hold the "width"
# and "height" of the "canvas" ("Pong" table).
WIDTH = 600
HEIGHT = 400 
# Initialize global constant that will hold the "radius" 
# of the ball.
BALL_RADIUS = 20
# Initialize global constants that will hold the "width"
# and "height" of the "paddles".
PAD_WIDTH = 8
PAD_HEIGHT = 80
# as well as compute the "half" of those values.
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
# Initialize global constants that will determine the 
# (horizontal) "direction" of the ball at the beginning 
# of a new game.
LEFT = False
RIGHT = True
# Initialize global constants that will hold the "beginning"
# and the "end" limits of "speed" ranges concerning the 
# horizontal and vertical "velocities", which will be 
# generated as random numbers within those boundaries 
# (pixels per update; 1/60 seconds) and according to the 
# guidelines of this project.
BALL_VEL_x_RANGE_START = 120
BALL_VEL_x_RANGE_STOP = 240
BALL_VEL_y_RANGE_START = 60
BALL_VEL_y_RANGE_STOP = 180
# Initialize global constant that will hold the "acceleration"
# of the (horizontal) ball "velocity".
# Increase the difficulty of the game, by increasing the 
# "velocity" of the ball by 10% each time it strikes a 
# "paddle".
BALL_VELOCITY_ACCELERATION = 1.1
# "Gutter" points.
# Whenever ball touches "gutter", "Player" gets "points".
POINTS = 1
# In this version of "Pong", the left and right "paddles"
# move up and down respectively at a constant "velocity".       
VERTICAL_VELOCITY = 4
# Motion keys.
# If the "w" or "s" key is pressed, move up or down left 
# "paddle". If the "up arrow" or "down arrow" key is 
# pressed, move up or down right "paddle".
MOTION_KEYS = ["w", "s", "up", "down"]
# Each new game should start after these seconds from the 
# time the "frame" opens or the time the "previous" game 
# ends.
NEW_GAME_DELAY = 3
# Set general "draw" properties.
COLOR = 'White'
FONT_FACE = 'sans-serif'
FONT_SIZE = 50
LINE_WIDTH = 1

#---------------------------------------------------------
# Define and initialize global variables.

# Initialize global variable that will hold the horizontal 
# and vertical "position" as well as "velocity" for the 
# ball. Note: "velocity" = pixels per update; 1/60 seconds).
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(BALL_VEL_x_RANGE_START, BALL_VEL_x_RANGE_STOP) // 60, 
            random.randrange(BALL_VEL_y_RANGE_START, BALL_VEL_y_RANGE_STOP) // 60]
# Initialize global variables that will hold the vertical 
# "positions" of the two "paddles", i.e. the vertical
# distance of the left and right "paddles" (centre of the
# "paddles") from the top of the "canvas" (table).
paddle1_pos = HEIGHT / 2
paddle2_pos = paddle1_pos
# Initialize global variables that will hold the vertical 
# "velocities" of the "paddles".
paddle1_vel = 0
paddle2_vel = 0
# Initialize global variables that will hold the scores
# for each "Player".
score1 = 0
score2 = 0
# Initialize global variable that will keep
# track of the time in "seconds". 
seconds = 0

#---------------------------------------------------------

def spawn_ball(direction):
    """
    Initialize ball "position" and "velocity" for new ball 
    in the middle of the table. If "direction" is "RIGHT", 
    the ball's "velocity" is upper right, else upper left.
    """
    
    # These are vectors stored as (global) "[x,y]" lists; 
    # ball "position" and "velocity".
    global ball_pos, ball_vel   
    
    # Set ball "position" at the middle of the table.    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # Randomization to the "velocity". The exact values for 
    # the horizontal and vertical components of this 
    # "velocity" should be generated using "random.randrange()".
    # This function returns a random integer "n" such that 
    # "start <= n < stop". For the horizontal and vertical 
    # "velocities", we generate a random number within the 
    # suggested "speed" limits (pixels per update; 
    # 1/60 seconds).
    ball_vel[0] = random.randrange(BALL_VEL_x_RANGE_START, BALL_VEL_x_RANGE_STOP) // 60
    ball_vel[1] = random.randrange(BALL_VEL_y_RANGE_START, BALL_VEL_y_RANGE_STOP) // 60
    
    # The velocity of the ball should be upwards and towards 
    # the right.
    if direction == RIGHT:
        ball_vel = [ball_vel[0], -ball_vel[1]]
    # The velocity of the ball should be upwards and towards 
    # the left.
    else:
        ball_vel = [-ball_vel[0], -ball_vel[1]]
    
    return None

#---------------------------------------------------------

def new_game():
    """
    Initialize a new game by reseting the vertical "positions"
    and "velocities" of the "paddles" as well as the "score"
    of each "Player". Call "spawn_ball()" to initialize  
    "position" and "velocity" for new ball. Start also a 
    timer, which will "postpone" the beginning of a new 
    game by the configured ammount of time.    
    """
    
    # These are (global) numbers; vertical "position" of 
    # each "paddle".
    global paddle1_pos, paddle2_pos 
    # These are (global) numbers; vertical "velocity" of 
    # each "paddle".
    global paddle1_vel, paddle2_vel  
    # These are (global) numbers; "score" of each 
    # "Player".
    global score1, score2  

    # Reset vertical positions of the two "paddles" 
    # (as global variables).
    paddle1_pos = HEIGHT / 2
    paddle2_pos = paddle1_pos
    
    # Reset vertical "velocities" of the two "paddles" 
    # (as global variables).
    paddle1_vel = 0
    paddle2_vel = 0
    
    # Reset "Player" scores (as global variables).
    score1 = 0
    score2 = 0

    # Check if "Timer" is Running; if not, start the "Timer".
    if not timer.is_running():
        timer.start()
    
    # Start a game of "Pong".
    spawn_ball(RIGHT)
    
    return None

#---------------------------------------------------------

def draw_handler(canvas):
    """
    Event handler that is responsible for all drawing. It
    receives "canvas" object and draws the "Pong" table, 
    the "moving" ball and the scores of each "Player".
    It is also responsible for testing whether the ball 
    touches/collides with the "gutters" or the "paddles".
    """

    # These are (global) numbers; vertical "position" of 
    # each "paddle".
    global paddle1_pos, paddle2_pos 
    # These are (global) numbers; "score" of each "Player".
    global score1, score2      
    # These are vectors stored as (global) "[x,y]" lists; 
    # ball "position" and "velocity".
    global ball_pos, ball_vel  
    # This is (global) number; keeps track of the time in 
    # "seconds".    
    global seconds
         
    # Draw middle line and "gutters" of "Pong" table.
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], LINE_WIDTH, COLOR)
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], LINE_WIDTH, COLOR)
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], LINE_WIDTH, COLOR)
        
    # "Postpone" the beginning of new game if "Timer" is 
    # already running by "reseting" ball "position" at the
    # middle of the table.
    if timer.is_running(): 
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        # Print message about the remaining time until the 
        # beginning of the new game by referencing the 
        # global "seconds" counter.
        canvas.draw_text("new game will start in " + 
                         str(NEW_GAME_DELAY - seconds) + 
                         " seconds" + 
                         ("." * (NEW_GAME_DELAY - seconds)), 
                         [WIDTH // 12, 3 * HEIGHT // 4], 3 * FONT_SIZE // 10, COLOR, FONT_FACE)            
    else:
        # "Timer" has expired; update ball "position" for 
        # the new game. 
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    
    # Test whether the ball touches/collides with the left 
    # "gutter" (offset from the left edge of the "canvas" 
    # by the width of the "paddle").
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        # Check whether the ball is actually striking left
        # "paddle" when it touches left "gutter". If so, 
        # reflect the ball back into play; ball's "velocity"
        # increased by the "acceleration" configured.
        if ((paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] = -ball_vel[0] * BALL_VELOCITY_ACCELERATION
        else:
            # Ball touched "gutter". Respawn the ball in 
            # the center of the table headed towards the 
            # opposite "gutter" and of course update score
            # of "Player" 2 (right) by the "points" 
            # configured.            
            score2 += POINTS
            
            # Start a game of "Pong". Start also a "Timer" 
            # to "postpone" the beginning of the new game.
            if not timer.is_running():
                timer.start()                       
                spawn_ball(RIGHT)      
                
    # Test whether the ball touches/collides with the right 
    # "gutter" (offset from the right edge of the "canvas" 
    # by the width of the "paddle").
    elif ball_pos[0] >= ((WIDTH - 1) - BALL_RADIUS - PAD_WIDTH):
        # Check whether the ball is actually striking right
        # "paddle" when it touches right "gutter". If so, 
        # reflect the ball back into play; ball's "velocity"
        # increased by the "acceleration" configured.
        if ((paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] = -ball_vel[0] * BALL_VELOCITY_ACCELERATION       
        else:
            # Ball touched "gutter". Respawn the ball in 
            # the center of the table headed towards the 
            # opposite "gutter" and of course update score
            # of "Player" 1 (left) by the "points" 
            # configured.                        
            score1 += POINTS

            # Start a game of "Pong". Start also a "Timer"
            # to "postpone" the beginning of the new game.           
            if not timer.is_running():
                timer.start()  
                spawn_ball(LEFT)                   
                
    # Collide and reflect off of top side of the "canvas".
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]               
    # Collide and reflect off of bottom side of the "canvas".
    elif ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]  
        
    # Draw a ball moving across the "Pong" table.
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2 * LINE_WIDTH, COLOR, COLOR)
    
    # Update paddle's vertical "position", by 
    # referencing the two global variables that contain the 
    # vertical "velocities" of the "paddle". Keep "paddle" 
    # on the screen by calling the proper "helper" function.
    if keep_paddle_on_screen(paddle1_pos, paddle1_vel):
        paddle1_pos += paddle1_vel
    if keep_paddle_on_screen(paddle2_pos, paddle2_vel):
        paddle2_pos += paddle2_vel        
    
    # Draw left and right "paddles" in their respective 
    # "gutters".      
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], 
                        [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                        [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                        [0, paddle1_pos + HALF_PAD_HEIGHT]],
                        LINE_WIDTH, COLOR, COLOR)             
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                        [WIDTH , paddle2_pos - HALF_PAD_HEIGHT], 
                        [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                        [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]],                                       
                        LINE_WIDTH, COLOR, COLOR)
        
    # Draw scores;
    # but first get the width of the "score" text in pixels 
    # for each "Player"; useful in (later) computing the 
    # position to draw the "score" text - centered justified 
    # on the "canvas field" of each player.
    score_textwidth_in_px = frame.get_canvas_textwidth(str(score1), FONT_SIZE, FONT_FACE)   
    score_point_x = (WIDTH // 4) - (score_textwidth_in_px // 2)
    score_point_y = (HEIGHT // 4) 
    canvas.draw_text(str(score1), [score_point_x, score_point_y], FONT_SIZE, COLOR, FONT_FACE)    
    
    score_textwidth_in_px = frame.get_canvas_textwidth(str(score2), FONT_SIZE, FONT_FACE)   
    score_point_x = (3 * WIDTH // 4) - (score_textwidth_in_px // 2)
    score_point_y = (HEIGHT // 4) 
    canvas.draw_text(str(score2), [score_point_x, score_point_y], FONT_SIZE, COLOR, FONT_FACE)    
    
    return None

#---------------------------------------------------------

def keep_paddle_on_screen(paddle_pos, paddle_vel):
    """
    Helper function that restrict "paddle" to stay entirely 
    on the "canvas" by testing whether the current update 
    for a paddle's "position" will move part of the "paddle" 
    off of the screen. If it does, don't allow the update by 
    returning a "False" boolean value; else return "True". 
    Function accepts current paddle's "vertical position" 
    and "vertical velocity".    
    """   
    
    # Compute updated (future) position of the "paddle".
    paddle_pos_updated = paddle_pos + paddle_vel
    
    # "Paddle" will be "off" (False) or "on" (True) screen.
    if (HALF_PAD_HEIGHT <= paddle_pos_updated <= (HEIGHT - HALF_PAD_HEIGHT)):    
        return True
    else: 
        return False
    
#---------------------------------------------------------

def keydown_handler(key):   
    """
    Event key handler. Update the values of the two vertical 
    "velocities" using this "key" handler.
    If key is pressed, "paddle" will start to move up or 
    down at a constant "velocity". When key is released, 
    "paddle" will stop moving.
    """    
    
    # These are (global) numbers; vertical "velocity" of 
    # each "paddle".
    global paddle1_vel, paddle2_vel      
        
    # The "w" and "s" keys should control the vertical 
    # "velocity" of the left "paddle" while the "Up arrow" 
    # and "Down arrow" key should control the "velocity" of 
    # the right "paddle".
    if key == simplegui.KEY_MAP[MOTION_KEYS[0]]:
        # If the "w" key is pressed, move up left 
        # "paddle".
        paddle1_vel -= VERTICAL_VELOCITY
    if key == simplegui.KEY_MAP[MOTION_KEYS[1]]:
        # If the "s" key is pressed, move down left 
        # "paddle".
        paddle1_vel += VERTICAL_VELOCITY 
    if key == simplegui.KEY_MAP[MOTION_KEYS[2]]:
        # If the "Up arrow" key is pressed, move up right 
        # "paddle".
        paddle2_vel -= VERTICAL_VELOCITY
    if key == simplegui.KEY_MAP[MOTION_KEYS[3]]:
        # If the "Down arrow" key is pressed, move down 
        # right "paddle".
        paddle2_vel += VERTICAL_VELOCITY 
    # else motionless if none of the above keys is pressed. 
     
    return None

#---------------------------------------------------------

def keyup_handler(key): 
    """
    Event key handler. Update the values of the two vertical 
    "velocities" using this "key" handler.
    If key is pressed, "paddle" will start to move up or 
    down at a constant "velocity". When key is released, 
    "paddle" will stop moving.
    """        
    
    # These are (global) numbers; vertical "velocity" of 
    # each "paddle".
    global paddle1_vel, paddle2_vel    

    # The "w" and "s" keys should control the vertical 
    # "velocity" of the left "paddle" while the "Up arrow" 
    # and "Down arrow" key should control the "velocity" of 
    # the right "paddle".
    if key == simplegui.KEY_MAP[MOTION_KEYS[0]]:
        # If the "w" key is released, stop moving up left 
        # "paddle".
        paddle1_vel = 0
    if key == simplegui.KEY_MAP[MOTION_KEYS[1]]:
        # If the "s" key is released, stop moving down left 
        # "paddle".
        paddle1_vel = 0 
    if key == simplegui.KEY_MAP[MOTION_KEYS[2]]:
        # If the "Up arrow" key is released, stop moving up
        # right "paddle".
        paddle2_vel = 0 
    if key == simplegui.KEY_MAP[MOTION_KEYS[3]]:
        # If the "Down arrow" key is released, stop moving 
        # down right "paddle".
        paddle2_vel = 0
    
    return None

#---------------------------------------------------------
# 
def button_restart_hander():
    """
    Event button handler. Call "new_game()" to reset the 
    "paddles", "score" and relaunch the ball. Reset also 
    a "Timer", which will "postpone" the beginning of a 
    new game by the configured ammount of time.       
    """
    
    # This is (global) number; keeps track of the time in 
    # "seconds".    
    global seconds    

    # Check if "Timer" is Running; if yes, stop the "Timer" 
    # and reset global "seconds" counter.
    if timer.is_running():
        seconds = 0
        timer.stop()
    
    # Reset the "paddles", "score", relaunch the ball and 
    # start the "Timer".    
    new_game()
    
    return None

#---------------------------------------------------------

def timer_handler():
    """
    Event handler for "Timer" with 1 sec interval, which
    increments or resets a global "time" counter.    
    """
   
    # Increment "seconds" (as global variable)
    # by one each time "Timer" calls this "event handler";
    # i.e. once per 1 second.
    global seconds
    seconds += 1
    
    # In case where "seconds" counter gets greater than the 
    # number of seconds configured as the "delay"
    # between two successive games, reset counter and stop
    # the "Timer".
    if seconds > NEW_GAME_DELAY:
        seconds = 0
        timer.stop()
          
    return None
 
#---------------------------------------------------------

# Create frame.
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

# Create a "Timer" by repeatedly calling the proper 
# "event handler" every 1 second.
timer = simplegui.create_timer(1000, timer_handler)

# Register the "event handler" that is responsible
# for all drawing.
frame.set_draw_handler(draw_handler)

# Register "event handlers" for "control" elements.
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.add_button("Restart", button_restart_hander, 200)

# Get a game going (almost) immediately.
new_game()

# Start frame.
frame.start()

#---------------------------------------------------------
