Angry Bits
===============

Entry in PyWeek #18  <http://www.pyweek.org/18/>
Team:  ccTeam 
Members: konemaster, Arti, stroet


DEPENDENCIES:

You might need to install some of these before running the game:

  Python:     http://www.python.org/
  PyGame:     http://www.pygame.org/
  pybox2d:    http://code.google.com/p/pybox2d/



RUNNING THE GAME:

On Windows or Mac OS X or Linux, run AngryBits.exe from. Alternatively locate the "run_game.py" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py



HOW TO PLAY THE GAME:

The goal of the game is to fill out 8 bits to get the number designated by Number. You do this by dropping a bit, which
will activate the first static bit it touches. When you activate the correct bits you will move forward to another number and 
raise your corect tries meter. If you hit an incorrect bit a new number will be generated for you, but raise your incorrect tries meter. 

The game gets more difficult the more correct numbers you get. This is done by increasing the speed based on the correct tries
and a random event, which gets more probable and fires more often based on that as well.

The game continues untill all 255 numbers have been expired. The goal is to correctly fill out as many number as possible.

The game is inteded to run in a small screen as a break brain puzzler/arcade game. Might also be usefull for kids to get the hang of
binary numbers.

Controls:

Release bit - Space
Pause - P
Restart Game - N
Hint - F1

Are also displayed ingame.

Settings:
There are some settings in settings.py  folder. You can tinker with the simulation settings to make it run 
better or turn off the random event and speed up. Not highly recommended though. No time to add a proper GUI for this.


LICENSE:

#  Copyright (c) 2014 Artyom Topchyan
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

