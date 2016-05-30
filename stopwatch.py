#
# Mini-project # 3: "Stopwatch".
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 3: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 12 Oct 2014
# Version: 4.0
#
# A simple digital "stopwatch" that keeps track of the "time" 
# in "tenths of a second". The "stopwatch" contains "Start", 
# "Stop" and "Reset" buttons.
# 

#---------------------------------------------------------
# Import the "simple gui" module.
import simplegui

#---------------------------------------------------------
# Define and initialize global variables.

# Initialize global variables that will hold the "width" 
# and "height" of the "canvas".
canvas_width = 300
canvas_heigth = 200
# Initialize global integer variable that will keep 
# track of the time in "tenths of seconds". The "stopwatch" 
# should be stopped when the frame opens.
tenths_of_seconds = 0
# Initialize global variable that will keep track of the 
# number of times the "watch" stopped on a whole second 
# "successfully" (1.0, 2.0, 3.0, etc.).
successful_stops = 0 
# Initialize global variable that will keep track of the  
# "total" number of times the "watch" stopped.
total_stops = 0

#---------------------------------------------------------

def format(time):
    """
    Helper function that converts "time" in "tenths of 
    seconds" into a formatted string in the following 
    form: "A:BC.D", where "A", "C" and "D" are digits in the 
    range "0-9" and "B" is in the range "0-5". 
    Note: "stopwatch" need only work correctly up to 10 
    minutes.
    """
    
    # Compute "tenths of a second", "seconds" and
    # "minutes" by using integer division and remainder 
    # (modular arithmetic) to extract various digits for 
    # the formatted "time" from the global integer "Timer".
    # Convert them into strings finally.
    tenths_of_seconds = str(time % 10)
    seconds = str((time // 10) % 60)
    minutes = str((time // 600) % 60)

    # The string returned must always correctly include 
    # leading zeros (if necessary). For example: 
    # format(0)   = 0:00.0 | format(11)  = 0:01.1 
    # format(321) = 0:32.1 | format(613) = 1:01.3            
    if len(seconds) == 1:
        seconds = "0" + seconds

    # Return the formatted "time" string.    
    return str(minutes) + ":" + str(seconds) + "." + str(tenths_of_seconds)
    
#---------------------------------------------------------
 
def button_start_hander():
    """
    Event handler for button "Start"; start the "Timer".
    """
    
    # Check if "Timer" is Running; if not, start the "Timer".
    if not timer.is_running():
        timer.start()
    
    return None

#---------------------------------------------------------

def button_stop_hander():
    """
    Event handler for button "Stop"; stop the "Timer" and 
    update the "stop-counters", that keep track of the number 
    of "successful stops" and the "total" number of 
    those ones.
    """
    
    # Check if "Timer" is Running; if yes, stop the "Timer".    
    if timer.is_running():
        timer.stop()
        
        # Update "stop-counters" (as global variables); i.e
        # increment "total stops" by one as well as the 
        # number of "successful stops" if and only if 
        # "watch" stopped on a whole second, by checking
        # if the "tenths of the current second" is "0" 
        # in the formatted "time" string.
        global total_stops, successful_stops
        total_stops += 1
        if (format(tenths_of_seconds)[-1] == "0"):
            successful_stops += 1

    return None

#---------------------------------------------------------

def button_reset_hander():
    """
    Event handler for button "Reset"; stop the "Timer" and
    reset the current "time" to zero. Reset also the 
    "stop-counters", that keep track of the number 
    of "successful stops" and the "total" number of 
    those ones. 
    """
    
    # Call "event handler" for button "Stop", stopping the
    # "Timer".
    button_stop_hander()
    
    # Reset the "Timer", i.e. in practice reset the 
    # variable that keeps track of the time in "tenths of 
    # seconds" as well as the "stop-counters" 
    # (as global variables).
    global tenths_of_seconds, total_stops, successful_stops
    tenths_of_seconds = 0
    total_stops = 0    
    successful_stops = 0
        
    return None

#---------------------------------------------------------

def timer_handler():
    """
    Event handler for "Timer" with 0.1 sec interval, which 
    "simply" increments a global integer.
    """
    
    # Increment "tenths_of_seconds" (as global variable) 
    # by one each time "Timer" calls this "event handler"; i.e
    # once per 0.1 seconds.
    global tenths_of_seconds
    tenths_of_seconds += 1
    
    return None

#---------------------------------------------------------

def draw_handler(canvas):    
    """
    Event handler that is responsible for all drawing. It
    receives "canvas" object and draws the current "time"
    in the middle of the "canvas" as well as the "stop- 
    counters" in the upper right-hand part of the "stopwatch 
    canvas".
    """
    
    # Set general "draw" properties.
    color = 'White'
    font_face = 'sans-serif'

    # Call function "format()" to convert "time" in "tenths 
    # of seconds" into a formatted string in the following
    # form: "A:BC.D".
    time = format(tenths_of_seconds)
    
    # Set specific "draw" properties for the "time" text.    
    font_size = 50
    margin_y = 14

    # Get the width of the "time" text in pixels; useful 
    # in (later) computing the position to draw the "time" 
    # text - centered justified on "canvas".
    time_textwidth_in_px = frame.get_canvas_textwidth(time, font_size, font_face)    
    time_point_x = (canvas_width // 2) - (time_textwidth_in_px // 2)
    time_point_y = (canvas_heigth // 2) + margin_y      
    
    # Draw "time".
    canvas.draw_text(time, [time_point_x, time_point_y], font_size, color, font_face)
    
    # Build string representing the "success" rate of 
    # watch "stops" by concatenating the number of "successful 
    # stops" and the number of "total stops". These counters 
    # will be drawn in the form "x/y", where "x" is the 
    # number of "successful stops" and "y" is number of 
    # "total stops".
    stops = str(successful_stops) + "/" + str(total_stops)
    
    # Set specific "draw" properties for the "stop-counters". 
    font_size = 25
    margin_x = 25
    margin_y = 30

    # Get the width of the "stops" text in pixels; useful 
    # in (later) computing the position to draw the text of
    # the "success" rate of "stops" on "canvas".    
    stops_textwidth_in_px = frame.get_canvas_textwidth(stops, font_size, font_face)              
    stops_point_x = canvas_width - stops_textwidth_in_px - margin_x
    stops_point_y = margin_y
    
    # Draw "success" rate of "stops".
    canvas.draw_text(stops, [stops_point_x, stops_point_y], font_size, color, font_face)
        
    return None

#---------------------------------------------------------

# Create frame.
frame = simplegui.create_frame('Stopwatch', canvas_width, canvas_heigth)

# Create a timer repeatedly calling the proper "event 
# handler" every 0.1 seconds. 
timer = simplegui.create_timer(100, timer_handler)

# Register the "event handler" that is responsible 
# for all drawing.
frame.set_draw_handler(draw_handler)

# Register "event handlers" for "control" elements.
frame.add_button("Start", button_start_hander, 200)
frame.add_button("Stop", button_stop_hander, 200)
frame.add_button("Reset", button_reset_hander, 200)

# Start frame.
frame.start()

##########################################################

# Test code by calling the function "format()"
# repeatedly in the program with different "time" (tenths 
# of seconds) as its input arguments. 
# Uncomment each sequence of calls and check whether the 
# output in the console matches that provided in the 
# comments below.
# Note that function should always return a string with 
# six characters.
# Ref: testing template found at the following URL:
# http://www.codeskulptor.org/#examples-format_template.py
 
#---------------------------------------------------------
# Test.

#print format(0)
#print format(7)
#print format(17)
#print format(60)
#print format(63)
#print format(214)
#print format(599)
#print format(600)
#print format(602)
#print format(667)
#print format(1325)
#print format(4567)
#print format(5999)

#---------------------------------------------------------
# Output from test.

#0:00.0
#0:00.7
#0:01.7
#0:06.0
#0:06.3
#0:21.4
#0:59.9
#1:00.0
#1:00.2
#1:06.7
#2:12.5
#7:36.7
#9:59.9

##########################################################
