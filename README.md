# ArcadeGames | Interactive Programming in Python

"Mini-projects" in "Python", serving to reinforce "interactive programming" concepts taught in "Introduction to Interactive Programming in Python" on-line class offered by "Coursera" (https://www.coursera.org/course/interactivepython | September - November 2014). 
 
This course was designed to be an introduction to the basics of programming in "Python" by building simple interactive applications. The primary method for learning the course material was to work through multiple "mini-projects" in "Python". These projects included building games such as "Pong", "Blackjack", and "Asteroids". 
 
Note: a browser-based programming environment "CodeSkulptor" was developed that made developing interactive applications in "Python" simple (http://www.codeskulptor.org/). "CodeSkulptor" runs "Python" programs in the browser by clicking the upper left button. It runs in "Chrome 18+", "Firefox 11+", and "Safari 6+". Some features may work in other browsers, but full functionality should not be expected. It does NOT run in "Internet Explorer". 
 
Below you can find the description and how to play each game along with the source code with (extended) line by line comments as well as the "URL" for each of those "CodeSkulptor" cloud-saved "mini-projects". 
 
### Quick "Mini-Projects" Index

* RiceRocks
* Blackjack
* Memory
* Pong
* Stopwatch
* Guess the Number
* Rock-Paper-Scissors-Lizard-Spock


## RiceRocks

### game description 
 
Implementation of a 2D space game "RiceRocks" that is inspired by the classic arcade game "Asteroids". The player's goal is to destroy these asteroids before they strike the player's ship. Large asteroids spawn randomly on the screen with random "velocities". The game has multiple rocks and multiple missiles. A life is lost if the ship collides with a rock and points are scored if the missile collides with a rock. The program keeps track of the score and lives remaining and ends the game at the proper time. 
 
Note: we highly recommend using "Chrome". "Chrome" typically has better performance on games with more substantial drawing requirements and standardization on a common browser. Chrome's superior performance becomes apparent when program attempts to draw dozens of "Sprites". Unfortunately, no audio format is supported by all major browsers. The provided sounds are in the "mp3" format, which is supported by "Chrome" (but not by "Firefox" on some systems). 
 
### how to play 
 
In the game, the player controls a spaceship via four buttons:

* two buttons that rotate the spaceship clockwise or counter clockwise (independent of its current "velocity"). The "left" and "right" arrows control the orientation of the ship.
* a "thrust" button that accelerates the ship in its "forward" direction. The "up arrow" controls the thrusters of the ship.
* a "fire - spacebar" button that shoots missiles.

Just Click on the "run" upper left button on "CodeSkulptor" to start playing. 

-- click to play "RiceRocks" @ http://www.codeskulptor.org/#user38_ZS5c5CDjLVDH3kS.py


## Blackjack

### game description 
 
Implementation of card game: "Blackjack". "Cards" in "Blackjack" have the following values: an "ace" may be valued as either 1 or 11 (player's choice), "face" cards (kings, queens and jacks) are valued at 10 and the value of the remaining cards corresponds to their number. During a round of "Blackjack", the players plays against a "Dealer" with the goal of building a "Hand" (a collection of "Cards") whose cards have a total value that is higher than the value of the dealer's "Hand", but not over 21. A round of "Blackjack" is also sometimes referred to as a "Hand". 
 
### how to play 
 
The game logic for this simplified version of "Blackjack" is as follows:

* The "Player" and the "Dealer" are each dealt two "Cards" initially with one of the dealer's cards being dealt faced down (his hole card).
* The "Player" may then ask for the "Dealer" to repeatedly "hit" his "Hand" by dealing him another "Card".
* If, at any point, the value of the player's "Hand" exceeds 21, the "Player" is "busted" and loses immediately.
* At any point prior to busting, the "Player" may "stand" and the "Dealer" will then hit his "Hand" until the value of his "Hand" is 17 or more. For the "Dealer", "aces" count as 11 unless it causes the dealer's "Hand" to bust.
* If the "Dealer" busts, the "Player" wins. Otherwise, the "Player" and "Dealer" then compare the values of their "Hands" and the "Hand" with the higher value wins. The "Dealer" wins ties in this version.

The program keeps track of wins and losses for Blackjack's session (wins minus losses) and contains:
* a "Deal" button that shuffles the "Deck" and "deals" the two "Cards" to both the "Dealer" and the "Player". Note: pressing the "Deal" button in the middle of the round causes the player to lose the current round.
* a "Hit" button that adds an extra card to player's "Hand".
* a "Stand" button that repeatedly hits the "Dealer" until his "Hand" has value 17 or more and finally compares the value of the player's and dealer's "Hands".

Just Click on the "run" upper left button on "CodeSkulptor" to start playing. 

-- click to play "Blackjack" @ http://www.codeskulptor.org/#user38_Sre1SIq1cuvP3al.py


## Memory

### game description 
 
Implementation of "Memory" card game, with two game "modes": play with "textual numbers" or "images" - in both cases a game of 16 "cards". The scope of the game is to "expose" all eight pairs of numbers (or images). 
 
### how to play 
 
Press the "run" upper left button on "CodeSkulptor" to start the program. Click on a "card" of the "deck" to expose it. A click on an card already "exposed" is ignored. If one unpaired card is exposed, a click on a second unexposed card exposes the card that was clicked on. If two unpaired cards are exposed, a click on an unexposed card exposes the card that was clicked on and flips the two unpaired cards over. If all exposed cards are paired, a click on an unexposed card exposes the card that was clicked on and does not flip any other cards. Cards paired by two clicks in the same turn remain exposed until the start of the next game. 
 
The program keeps track of the "turns" playing the game and contains:

* a "Reset" button that reshuffles the "cards", resets the "turn" counter and restarts the game.
* a "Reset and Play with (images | numbers)" button, which resets as well as switches the "mode" of the game.

-- click to play "Memory" @ http://www.codeskulptor.org/#user41_yoFTVqEW70FhBKE.py


## Pong

### game description 
 
Implementation of the classic arcade game "Pong". Whenever ball touches "gutter", "Player" gets "points". 
 
### how to play 
 
Once more click on the "run" upper left button on "CodeSkulptor" to start the program.

* if the "w" or "s" key is pressed, move up or down left "paddle".
* if the "up arrow" or "down arrow" key is pressed, move up or down right "paddle". When key is released, "paddle" will stop moving in any case.
* "Restart" button initializes a new game by resetting the "paddles" and the "scores" as well as relaunching the ball.

-- click to play "Pong" @ http://www.codeskulptor.org/#user38_vH3nXtvB8jHAOdH.py


## Stopwatch

### game description 
 
A simple digital "stopwatch" that keeps track of the "time" in "tenths of a second" and the number of times the "watch" stopped on a whole second "successfully" (1.0, 2.0, 3.0, etc.). 
 
### how to play 
 
Just click on the "run" upper left button on "CodeSkulptor" to start the program. The "stopwatch" contains:

* a "Start" button to start the "Timer".
* a "Stop" button to stop the "Timer" and update the "counters" that keep track of the number of "successful stops" and the "total" number of those ones.
* a "Reset" button to stop the "Timer", reset the current "time" and the previously mentioned "counters" to zero.

-- click to play "Stopwatch" @ http://www.codeskulptor.org/#user38_HNRcSRMHWTveYXi.py


## Guess the Number

### game description 
 
Two-player game: the first player thinks of a "secret" number in some known "range", while the second player attempts to "guess" the number. After each "guess", the first player answers either "Higher", "Lower" or "Correct" depending on whether the "secret" number is higher, lower or equal to the guess. Player is restricted to a limited number of guesses. 
 
### how to play 
 
In this project, an interactive program has been built where the "computer" takes the role of the first player. A "user" acts as the second player, interacting with the program using:

* an "input" field to enter "guesses".
* two buttons - each one changing the "range" and starting a new game.

Computer's responses will be printed in the console. Just click on the "run" upper left button on "CodeSkulptor" to start the program. 

-- click to play "Guess the Number" @ http://www.codeskulptor.org/#user38_qUSUQsJHQTbf1Yf.py


## Rock-Paper-Scissors-Lizard-Spock

### game description 
 
"Rock-paper-scissors-lizard-Spock" (RPSLS) is a variant of "Rock-paper-scissors" that allows five choices. Each choice wins against two other choices, loses against two other choices and ties against itself. The key idea of this program is to equate the strings "rock", "paper", "scissors", "lizard", "Spock" to numbers as follows:

0. rock
1. Spock
2. paper
3. lizard
4. scissors

Each choice wins against the preceding two choices and loses against the following two choices (if "rock" and "scissors" are thought of as being adjacent using "modular arithmetic"). 
 
### how to play 
 
Just click on the "run" upper left button on "CodeSkulptor" and the program will then simulate playing a round of "Rock-paper-scissors-lizard-Spock" for each of the five possible player choices, generating its own (computer) random choice from any of the above mentioned five alternatives and then determining the winner using a simple rule (as described in the above mentioned description of the game). 

-- click to play "Rock-Paper-Scissors-Lizard-Spock" @ http://www.codeskulptor.org/#user38_aXAzMrLqV44gQUh.py

