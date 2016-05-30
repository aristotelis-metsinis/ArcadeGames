#
# Mini-project # 8 - "RiceRocks" (Asteroids).
# 
# Author: Aristotelis Metsinis
# Email: aristotelis.metsinis@gmail.com
# Mini-project # 8: An Introduction to Interactive Programming in Python 
#				    @ https://www.coursera.org/course/interactivepython
# Date: 16 Nov 2014
# Version: 10.0
# Based on Mini-project # 7 - "Spaceship", ver 8.0).
#
# Implementation of a 2D space game "RiceRocks" that is 
# inspired by the classic arcade game "Asteroids".
# In the game, the player controls a spaceship via four 
# buttons: 
# * two buttons that rotate the spaceship clockwise or 
# counterclockwise (independent of its current "velocity").
# * a "thrust" button that accelerates the ship in its 
# "forward" direction. 
# * a "fire" button that shoots missiles.
# Large asteroids spawn randomly on the screen with 
# random "velocities".
# The player's goal is to destroy these asteroids before 
# they strike the player's ship.
# 
# In Mini-project # 7, a working spaceship plus a 
# single asteroid and a single missile was implemented
# only. The ship did not die if it hit a rock.
# Missiles "lifespan" was ignored. A single missile
# was allowed; not yet blowing up rocks.
# The number of "lives" remaining and the "score" were
# simply shown; neither of those elements was changed.
#
# In Mini-project # 8, the game has multiple
# rocks and multiple missiles. A life is lost if the ship
# collides with a rock and points are scored if the 
# missile collides with a rock. The program keeps track of
# the score and lives remaining and ends the game at the 
# proper time. Animated explosions have been added when 
# there is a collision.
#
# Note: we highly recommend using "Chrome".
# "Chrome" typically has better performance on games 
# with more substantial drawing requirements and 
# standardization on a common browser. 
# Chrome's superior performance becomes apparent when
# program attempts to draw dozens of "Sprites".
# Unfortunately, no audio format is supported by all 
# major browsers. The provided sounds are in the "mp3"
# format, which is supported by "Chrome" (but not by 
# "Firefox" on some systems).
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

# Globals for user interface.
# Initialize global constants that will hold the "width"
# and "height" of the "canvas".
WIDTH = 800
HEIGHT = 600

# Motion keys.
# The "left" and "right" arrows should control the 
# orientation of the ship.
# The "up arrow" should control the thrusters of the ship.
# Shoot when the "spacebar" is pressed.
MOTION_KEYS = ["left", "right", "up", "space"]

# To get the "acceleration" right, we need to multiply 
# the "forward" vector of the ship by this constant;
# small fraction of the "forward" acceleration vector 
# so that the ship does not accelerate too fast. So,
# scale each component of ship's "acceleration" vector 
# by this factor to generate a reasonable "acceleration".
THRUST = 0.1
# Update ship's "angular velocity" by this constant 
# whenever "left" and "right" arrow keys are pressed. So,
# a reasonable "angular velocity" at which ship should 
# turn.
ANGLE_VELOCITY = 0.05
# If "thrusters" are off, "friction" will bring
# the ship to a stop by introducing a deceleration
# in the opposite direction to the "velocity" of 
# the ship. Constant factor less than one.
# So, the "velocity" should always be multiplied by a 
# constant factor less than one to slow the ship down.
FRICTION = 0.01

# Rock's "angular velocity"; rotate once per second
# approximately.
ROCK_ANGLE_VELOCITY = 0.1
# Rock's min and max "angular velocity".
ROCK_MIN_ANGLE_VELOCITY = -0.15
ROCK_MAX_ANGLE_VELOCITY = 0.15
# Rock's min and max "velocity".
ROCK_MIN_VELOCITY = -1
ROCK_MAX_VELOCITY = 1
# Use this scaling factor to vary the "velocity" of rocks
# based on the score to make game play more difficult 
# as the game progresses. In practice, divide score by 
# this factor and compute the smallest integral value 
# greater than or equal to the result of the division.
# Then the "velocity" of a rock is multipled by the 
# outcome.
VELOCITY_SCALING_FACTOR = 10
# Limit the total number of rocks in the game at any one 
# time. With too many rocks the game becomes less fun and 
# the animation slows down significantly.
MAX_NUMBER_OF_ROCKS = 12

# Missile speed; used for the computation of the "velocity"
# of a missile, i.e. the combination (sum) of the ship's
# current "velocity" and a - by this factor - multiple 
# of the ship's "forward" vector.
MISSILE_SPEED = 8

# Tiled explosion image that can be used to create 
# animated explosions consisting of this number of
# images (number of sub-images of the "Sprite").
EXPLOSION_ANIMATIONS = 24

# Volume for the sound to be the given level on a 0 
# (silent) - 1.0 (maximum) scale. Default is 1.
VOLUME = 0.5

# This is the max remaining lives.
MAX_LIVES = 3
# Add these units in a case of a (missile - rock) hit.
# A point for each hit, scaled to these units.
SCORE_SCALING_FACTOR = 10

# Initialize global constants that will hold general
# "draw" properties.
FONT_SIZE = 25
FONT_COLOR = 'White'
FONT_FACE = 'sans-serif'

#---------------------------------------------------------
# Define and initialize global variables.

# Initialize global variable that will hold the "score"
# of the game.
score = 0
# Initialize global variable that will hold the number 
# of "lives" remaining.
lives = MAX_LIVES
# Initialize global variable used for "timing" and 
# "animation" purposes.
time = 0
# Boolean flag indicating whether the game has started
# (True) or not (False).
started = False

# Initialize global variable that will be assigned
# the "rock" (Sprite) group object (an empty set).
rock_group = set([])
# Initialize global variable that will be assigned
# the "missile" (Sprite) group object (an empty set).
missile_group = set([])
# Initialize global variable that will be assigned
# the "explosion" (Sprite) group object (an empty set).
explosion_group = set([]) 

#---------------------------------------------------------

class ImageInfo:
    """
    Define "Image Info" class.
    """
    
    #-----------------------------------------------------
    
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        """
        Create and initialize a "Image Info" object.
        Stores information about the image.
        """
        
        # Centre of the image.
        self.center = center
        # Size of the image.
        self.size = size
        # The radius of a circle that completely encloses 
        # the image; use this circle to detect collisions 
        # with the ship instead of having to worry about 
        # the exact shape of the image.
        self.radius = radius
        # The lifespan of the image; not needed for the 
        # ship - other objects like missiles have a 
        # lifespan, i.e. they should be drawn only for a 
        # certain period of time.
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        # Whether or not image is animated; not needed for
        # the ship as being a static image - other objects
        # like explosions are animated images.
        self.animated = animated

    #-----------------------------------------------------
    
    def get_center(self):
        """
        Get the centre of the image.
        """
        
        return self.center
    
    #-----------------------------------------------------
    
    def get_size(self):
        """
        Get the size of the image.
        """
        
        return self.size

    #-----------------------------------------------------
    
    def get_radius(self):
        """
        Get the radius of a circle that completely encloses 
        the image.
        """
        
        return self.radius

    #-----------------------------------------------------
    
    def get_lifespan(self):
        """
        Get the lifespan of the image.
        """
        
        return self.lifespan

    #-----------------------------------------------------
    
    def get_animated(self):
        """
        Get whether or not image is animated.
        """
        
        return self.animated

#---------------------------------------------------------    
# Art assets created by "Kim Lathrop"; may be freely 
# re-used in non-commercial projects, please credit Kim.
    
# Debris images - debris1_brown.png, debris2_brown.png, 
#    			  debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, 
#				  debris3_blue.png, debris4_blue.png, 
# 				  debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# Splash image.
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image.
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile images - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images - asteroid_blue.png, asteroid_brown.png,
#					asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Animated explosion - explosion_orange.png, 
#					   explosion_blue.png, 
#					   explosion_blue2.png, 
# 					   explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# Sound assets purchased from "sounddogs.com"; 
# please do not redistribute.
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(VOLUME)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

#--------------------------------------------------------- 

def angle_to_vector(ang):
    """
    Helper function to handle transformation.
    When thrusting, the ship should accelerate in the 
    direction of its "forward" vector. This vector can be 
    computed from the orientation/angle of the ship using 
    this "helper" function.
    """
    
    return [math.cos(ang), math.sin(ang)]

#--------------------------------------------------------- 

def dist(p,q):
    """
    Helper function to compute the "distance" of two
    2D points.
    """
    
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#--------------------------------------------------------- 
 
class Ship:
    """
    Define "Ship" class.
    """
    
    #-----------------------------------------------------
    
    def __init__(self, pos, vel, angle, image, info):
        """
        Create and initialize a "Ship" object of a 
        specific "position", "velocity", "angle", "image"
        and "image - info".
        """
        
        # "Position" of the ship on the "canvas" (vector / 
        # pair of floats).
        self.pos = [pos[0], pos[1]]
        # "Velocity" of the ship; the direction the ship
        # is moving does not have to be in the direction
        # it is facing (vector / pair of floats).
        self.vel = [vel[0], vel[1]]
        # Make the ship accelerate in the 
        # direction it is facing (boolean).
        # Initially set to "false" indicating that we are 
        # not thrusting in the beginning; engines are 
        # turned off - we should not draw the thrust and 
        # we should not accelerate.
        self.thrust = False
        # Ship's orientation (scalar / float); the angle
        # between the horizontal axis and the direction the
        # ship is pointing (in radians; not degrees).
        self.angle = angle
        # Ship's angular velocity (scalar / float); control
        # how fast the ship will actually rotate whenever
        # "left" and "right" arrow keys are pressed.
        # Initially set to "0" indicating that the ship 
        # should not be rotating in the beginning. 
        self.angle_vel = 0
        
        # The image of the ship (tiled image; the first 
        # tile is the ship without thrusters - the second 
        # tile is the ship with thrusters).
        self.image = image
        # Get information about this image.
        self.image_center = info.get_center()
        self.image_size = info.get_size()        
        self.radius = info.get_radius()

    #-----------------------------------------------------
    
    def draw(self, canvas):
        """
        Draw ship's image by incorporating ship's 
        "position" and "angle". Draw the "thrust" image 
        when thrusters are on.
        Note: the angle should be in radians, not degrees;
        one radian is equal to "180/pi" degrees.
        """
        
        # Draw ship's image with or without thrusters 
        # depending on whether or not the ship is currently
        # thrusting. The ship should also be drawn rotated 
        # to the proper "angle" so that it is 
        # facing in the proper way.
        if not self.thrust:        
            canvas.draw_image(self.image,
                             (self.image_center[0], self.image_center[1]),
                             (self.image_size[0], self.image_size[1]),
                             (self.pos[0], self.pos[1]),
                             (self.image_size[0], self.image_size[1]),
                              self.angle)
        else:
            canvas.draw_image(self.image,
                             (3 * self.image_center[0], self.image_center[1]),
                             (self.image_size[0], self.image_size[1]),
                             (self.pos[0], self.pos[1]),
                             (self.image_size[0], self.image_size[1]),
                              self.angle)            
            
        return None           

    #-----------------------------------------------------
    
    def update(self):
        """
        Modify and update ship's "angle", "position" and 
        "velocity".
        It gets called every time the "draw" handler for 
        the system is called.
        """

        # Update ship's "angle" (orientation) based on its 
        # "angular velocity".        
        self.angle += self.angle_vel

        # Update the "position" of the ship based on its 
        # "velocity".  
        # Note: as seen below, while the ship accelerates 
        # in its "forward" direction, the ship always 
        # moves in the direction of its "velocity" vector. 
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Ship's "position" wraps around the screen when 
        # it goes off the edge (by using modular 
        # arithmetic).
        self.pos[0] %= WIDTH 
        self.pos[1] %= HEIGHT
        
        # If "thrusters" are off, "friction" will bring
        # the ship to a stop by introducing a deceleration
        # in the opposite direction to the "velocity" of 
        # the ship (constant factor slightly less than one). 
        # Without a "friction" the
        # ship will move as fast as we want by keeping
        # "thrusters" continually on. "Friction" actually
        # caps the "velocity" of the ship.
        # So, the "velocity" should always be multiplied by a 
        # constant factor less than one to slow the ship 
        # down. 
        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)

        # When thrusting, update the "velocity" of the 
        # ship in terms of its "acceleration" in the 
        # direction of the "forward" vector.
        if self.thrust:
            # However previously we need to figure out 
            # what direction the ship is accelerating in; 
            # the "forward" vector that
            # corresponds to the direction that should
            # accelerate in based on ship's angle; by 
            # making use of the "angle_to_vector()" 
            # function.
            # Also, to get the acceleration right, we 
            # need to multiply the "forward" vector by a 
            # constant (small fraction of the "forward" 
            # "acceleration" vector so that the ship does 
            # not accelerate too fast).
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * THRUST
            self.vel[1] += forward[1] * THRUST                    
        
        return None
    
    #-----------------------------------------------------
    
    def adjust_orientation(self, angle_vel):
        """
        Increment and decrement the "angular velocity" by 
        the (fixed in practice) "angle_vel" amount.
        """
        
        self.angle_vel += angle_vel
        
        return None

    #-----------------------------------------------------
    
    def set_thrust(self, on_off):
        """
        Turn the thrusters on/off depending on the 
        "on_off" boolean argument. 
        Rewind and Play the "thrust" sound when the 
        "thrust" is on. 
        Pause/Stop the sound when the "thrust" turns off.
        """
        
        self.thrust = on_off  
        
        if self.thrust:
            # Stop playing the sound in any case, and 
            # make it so the next "sound.play()" will 
            # start playing the sound at the 
            # beginning.                                                 
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()            
        else:
            # Stop playing the sound. 
            ship_thrust_sound.pause()
        
        return None

    #-----------------------------------------------------
    
    def shoot(self):
        """
        Spawn a new missile (an instance of the "Sprite" 
        class) and add it to the "missile_group".        
        Call this method when the "spacebar" is pressed.
        """
        
        # The missile spawns from the tip of the ship;
        # so missile's initial "position" should be the 
        # tip of ship's "cannon". 
        # Also the missile is travelling in the direction 
        # the ship is facing. So, the "velocity" of a 
        # missile is the combination (sum) of the ship's 
        # current "velocity" and a multiple of the ship's
        # "forward" vector. Furthermore, missiles will 
        # always have a zero "angular velocity" and a 
        # "lifespan". Finally, missile sound is passed to 
        # the "Sprite" initializer so that the shooting 
        # sound is played whenever a missile spawns.               
        
        forward = angle_to_vector(self.angle) 
        
        missile_pos = [self.pos[0] + self.radius * forward[0], 
                       self.pos[1] + self.radius * forward[1]]
                       
        missile_vel = [self.vel[0] + MISSILE_SPEED * forward[0], 
                       self.vel[1] + MISSILE_SPEED * forward[1]]
                
        a_missile = Sprite(missile_pos, missile_vel,
                           self.angle, 0, missile_image, 
                           missile_info, missile_sound)        
        
        # Keep a set of missiles and spawn this new 
        # missile into this set when firing using the 
        # space bar.
        global missile_group
        missile_group.add(a_missile)
                
        return None

    #-----------------------------------------------------

    def get_position(self):
        """
        Get the position of the ship.
        """

        return self.pos

    #-----------------------------------------------------

    def get_radius(self):
        """
        Get the radius of a circle that completely 
        encloses the (image of the) ship.
        """

        return self.radius
    
#--------------------------------------------------------- 

class Sprite:
    """
    Define "Sprite" class. 
    "Sprite" is a 2D image or animation overlaid on top of 
    a game to add visual complexity.    
    """
    
    #-----------------------------------------------------
    
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        """
        Create and initialize a "Sprite" object;
        implements rocks and missiles.
        Note: "velocity" and "rotation" are not anymore 
        controlled by keys as in the case of the ship. 
        Rock "Sprites" have set "velocity", "position", 
        and "angular velocity" randomly when they are 
        created. Also, missiles will always have a zero 
        "angular velocity" and a certain "lifespan".
        """
        
        # "Position" of the "Sprite" on the "canvas" 
        # (vector / pair of floats).
        self.pos = [pos[0], pos[1]]
        # "Velocity" of the "Sprite".
        self.vel = [vel[0], vel[1]]
        # "Sprite's" orientation (scalar / float); the 
        # angle between the horizontal axis and the 
        # direction the "Sprite" is pointing (in radians; 
        # not degrees).                                
        self.angle = ang
        # "Sprite's" angular velocity (scalar / float); 
        # control how fast the "Sprite" will actually 
        # rotate.
        self.angle_vel = ang_vel
        # The image of the "Sprite".
        self.image = image
        # Get information about this image.
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        # The lifespan of the image.
        self.lifespan = info.get_lifespan()
        # Whether or not image is animated.
        self.animated = info.get_animated()
        # Age of the "Sprite"; if the "age" is greater than 
        # or equal to the "lifespan" of the "Sprite", then 
        # it should be removed.
        self.age = 0
        # Option of giving "Sprite" a sound.
        if sound:
            sound.rewind()
            sound.play()
   
    #-----------------------------------------------------
    
    def draw(self, canvas):
        """
        Draw the "Sprite".
        Check if "self.animated" attribute is "True". 
        If so, then choose the correct tile in the image 
        based on the "age". The image is tiled 
        horizontally. If "self.animated" is "False", it 
        should continue to draw the "Sprite" as before.
        """
        
        if not self.animated:       
            canvas.draw_image(self.image, self.image_center, 
                              self.image_size, self.pos, 
                              self.image_size, self.angle)
        else:
            # Tiled explosion image that can be used to 
            # create animated explosions.
            # Modular arithmetic; so the number coming back 
            # will be always within the range from zero to
            # the number of the (sub)images of the "Sprite".
            # Integer division; to avoid index by a fraction 
            # (rather index by a whole number) - index 
            # inside the tiled image.
            image_index = (self.age % EXPLOSION_ANIMATIONS) // 1
            # Computation of the sub-image centre.
            image_center = [self.image_center[0] + (self.image_size[0] * image_index),
                            self.image_center[1]]  
            canvas.draw_image(self.image, image_center, 
                              self.image_size, self.pos, 
                              self.image_size, self.angle)           
        
        return None
    
    #-----------------------------------------------------
    
    def update(self):
        """
        Update "Sprite" every time this is called inside  
        the "draw" handler; move and rotate "Sprite".
        Return "False" (i.e. keep "Sprite") if the "age" 
        is less than the "lifespan" or "True" (i.e. 
        remove "Sprite") otherwise.
        Note: "velocity" and "rotation" are not anymore 
        controlled by keys as in the case of the ship. 
        Rock "Sprites" have set "velocity", "position", 
        and "angular velocity" randomly when they are 
        created. Rocks do not accelerate or 
        experience friction. Also, missiles will 
        always have a zero "angular velocity" and a
        certain "lifespan".
        """

        # Update Sprite's "angle" (orientation) based on 
        # its "angular velocity".          
        self.angle += self.angle_vel
        
        # Update the "position" of the "Sprite" based on 
        # its "velocity".          
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Sprite's position wraps around the screen when 
        # it goes off the edge (by using modular 
        # arithmetic).
        self.pos[0] %= WIDTH 
        self.pos[1] %= HEIGHT          

        # Increment the "age" of the "Sprite" every time 
        # "update()" is called.
        self.age += 1
        # If the "age" is greater than or equal to the 
        # "lifespan" of the "Sprite", then it should be 
        # removed (i.e. return "True", else "False").
        if self.age >= self.lifespan:
            return True
        else:                 
            return False

    #-----------------------------------------------------

    def collide(self, other_object):
        """
        Take an "other_object" as an argument and return 
        "True" if there is a collision with a (rock) 
        "Sprite" or "False" otherwise. This "other object" 
        may be either the "ship" or a "missile" object
        in practice.
        """
                
        # Compute the distance between the centres of the
        # two objects. If less that the sum of their
        # radius then assume collision (the circles that 
        # enclose them overlap).
        if dist(self.pos, other_object.get_position()) < ( self.radius + other_object.get_radius()):                          
            return True
        else:
            return False

    #-----------------------------------------------------

    def get_position(self):
        """
        Get the position of the "Sprite".
        """

        return self.pos

    #-----------------------------------------------------

    def get_radius(self):
        """
        Get the radius of a circle that completely 
        encloses the (image of the) "Sprite".
        """

        return self.radius    
                
#---------------------------------------------------------

def draw(canvas):
    """
    Event handler that is responsible for all drawing.
    It receives the "canvas" object and draws the animated
    background, the ship, the rock and missile "Sprites"
    as well as game's score and remaining lives.
    If the number of lives becomes 0, the game is reset 
    and the "splash" screen appears.
    """
    
    global time    
    # Animate background.
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    global lives    
    # Draw remaining "lives".
    canvas.draw_text("Lives: " + str(lives), 
                     [WIDTH // 8, HEIGHT // 8], 
                     FONT_SIZE, FONT_COLOR, FONT_FACE)
    
    global score
    # Draw "score";
    # but first get the width of the "score" text in 
    # pixels; useful in (later) computing the
    # position to draw the "score" text - right justified
    # on the "canvas".
    score_text = "Score: " + str(score)
    score_textwidth_in_px = frame.get_canvas_textwidth(score_text, FONT_SIZE, FONT_FACE)  
    score_point_x = WIDTH - (WIDTH // 8) - (score_textwidth_in_px)
    score_point_y = HEIGHT // 8
    canvas.draw_text(score_text, 
                     [score_point_x, score_point_y], 
                     FONT_SIZE, FONT_COLOR, FONT_FACE)
    
    global rock_group, missile_group, explosion_group
    # Draw ship and "Sprites".
    my_ship.draw(canvas)        
    if rock_group:        
        # Take the group of rocks and the "canvas" and
        # call the "draw" method for each 
        # rock "Sprite" in the group.
        process_sprite_group(canvas, rock_group, "draw")    
    if missile_group:
        # Take the group of missiles and the "canvas" and
        # call the "draw" method for each 
        # missile "Sprite" in the group.        
        process_sprite_group(canvas, missile_group, "draw")
    if explosion_group:        
        # Take the group of explosions and the "canvas" 
        # and call the "draw" method for each 
        # explosion "Sprite" in the group.
        process_sprite_group(canvas, explosion_group, "draw")
                    
    # Update ship and "Sprites".
    my_ship.update()
    if rock_group:
        # Take the group of rocks and the "canvas" and
        # call the "update" method for each rock "Sprite"
        # in the group.
        process_sprite_group(None, rock_group, "update")        
    if missile_group:
        # Take the group of missiles and the "canvas" and
        # call the "update" method for each 
        # missile "Sprite" in the group.         
        process_sprite_group(None, missile_group, "update")
    if explosion_group:        
        # Take the group of explosions and the "canvas" 
        # and call the "update" method for each 
        # explosion "Sprite" in the group.
        process_sprite_group(None, explosion_group, "update")
              
    # Determine if the ship hits any of the rocks.
    # If so, decrease the number of lives by one.
    if group_collide(rock_group, my_ship):
        lives -= 1       

    global started    
    # If the number of lives becomes 0, the game is 
    # reset and the "splash" screen shall appear.    
    if lives == 0:
        started = False 
        # Destroy all "Sprites".
        rock_group = set([])
        #missile_group = set([])
        #explosion_group = set([])
                
    # Detect missile / rock collisions and
    # increment the "score" by the number of missile 
    # collisions (and a "scaling" factor).
    score += group_group_collide(rock_group, missile_group) * SCORE_SCALING_FACTOR

    # Draw "splash" screen if game not started; dismissed
    # with a mouse click before starting this game.
    if not started:
        canvas.draw_image(splash_image, 
                          splash_info.get_center(),
                          splash_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    return None

#---------------------------------------------------------

def rock_spawner():
    """
    Timer handler that spawns a rock; new rock on every 
    tick; once every second.
    Note: "velocity" and "rotation" are not anymore 
    controlled by keys as in the case of the ship. 
    Rock "Sprites" have set "velocity", "position", 
    and "angular velocity" randomly when they are 
    created. Last but not least, the total number of
    rock "Sprites" in the game is limited at any one time.
    """

    # Prevent any (more) rocks for spawning until the 
    # game is (re)started.    
    if not started:
        return None
    
    global rock_group    
    # Limit the total number of rocks in the game at any 
    # one time.
    if len(rock_group) >= MAX_NUMBER_OF_ROCKS:
        return None
    
    # Rock's "velocity".
    # Generate random floating-point number "n" in an 
    # arbitrary range: "min <= n < max".        
    velocity_range = ROCK_MAX_VELOCITY - ROCK_MIN_VELOCITY		                
    rock_vel = [random.random() * velocity_range + ROCK_MIN_VELOCITY, 
                random.random() * velocity_range + ROCK_MIN_VELOCITY]

    # Vary the velocity of rocks based on the score to 
    # make game play more difficult as the game progresses.
    # In practice, multiply "velocity" by 1, 2, 3, etc, as
    # the score gets higher.
    if score > 0: 
        rock_vel = [rock_vel[0] * math.ceil(float(score) / (VELOCITY_SCALING_FACTOR * SCORE_SCALING_FACTOR)),
                    rock_vel[1] * math.ceil(float(score) / (VELOCITY_SCALING_FACTOR * SCORE_SCALING_FACTOR))]
    
    # Rock's "angular velocity".
    # Generate random floating-point number "n" in an 
    # arbitrary range: "min <= n < max".         
    angle_velocity_range = ROCK_MAX_ANGLE_VELOCITY - ROCK_MIN_ANGLE_VELOCITY	        
    rock_angle_vel = random.random() * angle_velocity_range + ROCK_MIN_ANGLE_VELOCITY

    # Rock's "position".
    # Generate random integer "n" such that 
    # "min <= n < max".
    rock_pos = [random.randrange(0, WIDTH - 1), 
                random.randrange(0, HEIGHT - 1)]
        
    # Only spawn new rock if collision with ship is 
    # "false", taking into considaration also a "safe"
    # distance "margin" by making sure they are some 
    # distance away from the ship. Otherwise, ship can be 
    # destroyed when a rock spawns on top of it. So,
    # "skip" a rock spawn event if the spawned rock is too 
    # close to the ship.
    ship_radius = ship_info.get_radius()
    rock_radius = asteroid_info.get_radius()          
    while dist(rock_pos, my_ship.pos) < ( (2 * ship_radius) + rock_radius):                          
        rock_pos = [random.randrange(0, WIDTH - 1), 
                    random.randrange(0, HEIGHT - 1)]
        
    # So generate rocks that spin in both directions 
    # and, likewise, move in all directions. 
    a_rock = Sprite(rock_pos, rock_vel, 
                    0, rock_angle_vel, 
                    asteroid_image, asteroid_info)   

    # Spawn new rocks into the set of rocks by
    # adding the just created rock (an instance
    # of a "Sprite" object).
    rock_group.add(a_rock)
   
    return None

#---------------------------------------------------------

def process_sprite_group(canvas, sprite_group, method):
    """
    Helper function to take a "set" and a "canvas" and 
    call the "update" and "draw" methods for each "Sprite"
    in the group. Check also the return value of "update" 
    for "Sprites". If it returns "True", remove the 
    "Sprite" from the group. 
    Note: iterate over a copy of the "sprite group"  
    to avoid deleting (if necessary) from the same set 
    over which we are iterating.
    """

    group_copy = set(sprite_group)        
    for sprite in group_copy:                        
        if method == "draw":
            sprite.draw(canvas)
        else:
            remove_sprite = sprite.update()
            if remove_sprite:		    	
                sprite_group.remove(sprite)            		               

    return None  

#---------------------------------------------------------

def group_collide(group, other_object):
    """
    Helper function to take a set "group" and an a "Sprite"
    "other_object" and check for collisions between 
    "other_object" and elements of the group. In practice,
    collisions between a single "Sprite" (e.g. ship or a 
    missile) and any "Sprite" in the "group" (e.g. group 
    of rocks) will be detected.
    This function should return "True" or "False" 
    depending on whether there was a collision.
    "True" if there was a collision with anything in the 
    "group", "False" if "other_object" collided with 
    nothing in the "group".
    """

    collision = False
    
    # Upon a collision, the rock should be 
    # destroyed and the player should lose a life.
    # If there is a collision, the colliding object 
    # should will be removed from the group. To avoid 
    # removing an object from a set that we are iterating
    # over (which can cause a serious debugging headache),
    # we iterate over a copy of the set created via 
    # "set(group)". 
    group_copy = set(group)    
    for object in group_copy:
        if object.collide(other_object):
            group.remove(object)
            collision = True
            # Create a new "explosion" (an instance of 
            # the "Sprite" class) and add it to the 
            # "explosion_group".
            # Make sure that each explosion plays 
            # the explosion sound.            
            explosion = Sprite(object.get_position(), 
                               [0, 0], 0, 0,
                               explosion_image, 
                               explosion_info, 
                               explosion_sound) 
            explosion_group.add(explosion)
            
    return collision

#---------------------------------------------------------

def group_group_collide(group_1, group_2):
    """
    Helper function that essentially checks for 
    collisions between two groups by taking two groups 
    of objects as input and iterating through the 
    elements of a copy of the first group using a 
    for-loop. Then calls "group_collide()" with each of 
    these elements on the second group. Returns the 
    number of elements in the first group that collide 
    with the second group as well as deletes these 
    elements in the first group.
    """

    number_of_collisions = 0
    
    group_copy_1 = set(group_1)
    for object in group_copy_1:    
        collision = group_collide(group_2, object)
        if collision:
            # Essentially, we want to destroy rocks when 
            # they are hit by a missile.            
            group_1.discard(object)
            # Keep track the number of times 
            # "group_collide()" returns "True".
            number_of_collisions += 1
    
    # Return the number of collisions between "group_1" 
    # (e.g. rocks) and "group-2" (e.g. missiles); for 
    # example if the number is 6, then 6 rocks were 
    # destroyed and we can update score accordingly.
    return number_of_collisions

#---------------------------------------------------------
 
def keydown_handler(key):  
    """
    Event key handler. 
    Update ship's "angular velocity" and so control how 
    the ship rotates whenever "left" and "right" arrow keys 
    are pressed.
    While the "left arrow" is held down, ship should turn 
    counter-clockwise. While the "right arrow" is down, ship
    should turn clockwise. When neither key is down, ship 
    should maintain its orientation. Also,
    the "up arrow" should control the thrusters of the ship.    
    The thrusters should be on when the "up arrow" is down 
    and off when it is up.
    Shoot when the "spacebar" is pressed.    
    """   

    # Enable this handler only when game has started 
    # in practice.
    #if not started:
    #    return None
    
    # The "left" and "right" arrows should control the 
    # orientation of the ship.
    # The "up arrow" should control the thrusters of the ship.
    # Call "shoot()" method when the "spacebar" is pressed.
    if key == simplegui.KEY_MAP[MOTION_KEYS[0]]:
        # If the "left arrow" key is pressed, turn ship
        # counter-clockwise. 
        # Decrement the "angular velocity" by a 
        # fixed amount in practice. 
        my_ship.adjust_orientation(-ANGLE_VELOCITY)
        
    if key == simplegui.KEY_MAP[MOTION_KEYS[1]]:
        # If the "right arrow" key is pressed, turn ship
        # clockwise.        
        # Increment the "angular velocity" by a 
        # fixed amount in practice. 
        my_ship.adjust_orientation(ANGLE_VELOCITY)
        
    if key == simplegui.KEY_MAP[MOTION_KEYS[2]]:
        # If the "up arrow" key is pressed, thrusters 
        # should be on.
        my_ship.set_thrust(True) 
        
    if key == simplegui.KEY_MAP[MOTION_KEYS[3]]:
        # If the "spacebar" key is pressed, call "shoot()"
        # method.
        my_ship.shoot()         
     
    return None
 
#---------------------------------------------------------
 
def keyup_handler(key):
    """
    Event key handler. 
    Update ship's "angular velocity" and so control how 
    the ship rotates whenever "left" and "right" arrow keys 
    are pressed.
    While the "left arrow" is held down, ship should turn 
    counter-clockwise. While the "right arrow" is down, ship
    should turn clockwise. When neither key is down, ship 
    should maintain its orientation. Also,
    the "up arrow" should control the thrusters of the ship.    
    The thrusters should be on when the "up arrow" is down 
    and off when it is up.    
    """   
    
    # The "left" and "right" arrows should control the 
    # orientation of the ship. 
    # The "up arrow" should control the thrusters of the ship.
    if key == simplegui.KEY_MAP[MOTION_KEYS[0]]:
        # If the "left arrow" key is released, stop turning 
        # ship counter-clockwise.
        # Maintain ship's orientation by "canceling"
        # the last change of the "angular velocity". 
        my_ship.adjust_orientation(ANGLE_VELOCITY)
                
    if key == simplegui.KEY_MAP[MOTION_KEYS[1]]:
        # If the "right arrow" key is released, stop turning 
        # ship clockwise.
        # Maintain ship's orientation by "canceling"
        # the last change of the "angular velocity". 
        my_ship.adjust_orientation(-ANGLE_VELOCITY)
        
    if key == simplegui.KEY_MAP[MOTION_KEYS[2]]:
        # If the "up arrow" key is released, thrusters 
        # should be off.
        my_ship.set_thrust(False)                 
                       
    return None

#---------------------------------------------------------

def click(pos):
    """
    Mouse click handler that resets UI and conditions 
    whether "splash" image is drawn.
    """

    center = [WIDTH / 2, HEIGHT / 2]

    size = splash_info.get_size()

    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    global started, lives, score, my_ship
    if (not started) and inwidth and inheight:
        started = True
        # Make sure lives and score are properly 
        # initialized.
        lives = MAX_LIVES
        score = 0
        # Stop playing the sound, and 
        # make it so the next "sound.play()" will 
        # start playing the background music at the 
        # beginning.                                                 
        soundtrack.rewind()
        soundtrack.play() 
        # Initialize ship.
        #my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 
        #               0, ship_image, ship_info)

    return None

#---------------------------------------------------------

# Create and initialize frame.
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Initialize ship (and two "Sprites").
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 
               0, ship_image, ship_info)
# In the template of Mini-project # 7, the global variable
# "a_rock" was created at the start with zero "velocity". 
# Instead, we wanted to create version of "a_rock" once 
# every second in the "timer" handler.
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 
#                0, ROCK_ANGLE_VELOCITY, 
#                asteroid_image, asteroid_info)
# In the template of Mini-project # 7, the global variable
# "a_missile" was created at the start. Instead, we wanted 
# to create version of "a_missile" whenever "spacebar" key
# was pressed in the "keydown" handler.
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1],
#                   0, 0, missile_image, 
#                   missile_info, missile_sound)

# Register the "event handler" that is responsible
# for all drawing.
frame.set_draw_handler(draw)

# Register "event handlers" for "control" elements.
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(click)

# Create a "Timer" repeatedly calling the proper "event
# handler" every 1 second.
timer = simplegui.create_timer(1000.0, rock_spawner)

# Get things rolling.
# Start the "Timer".
timer.start()
# Start frame.
frame.start()
# Start playing the background music.                                                       
#soundtrack.play() 
