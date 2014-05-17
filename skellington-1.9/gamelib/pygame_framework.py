#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
# Modified 2014 Artyom Topchyan

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

 

import pygame
import framework
from pygame.locals import *
from .framework import *
 

class PygameDraw(b2DrawExtended):
    
    surface = None
    axisScale = 10.0
    def __init__(self, **kwargs): 
        b2DrawExtended.__init__(self, **kwargs)
        self.flipX = False
        self.flipY = True
        self.convertVertices = True

    def StartDraw(self):
        self.zoom=self.test.viewZoom
        self.center=self.test.viewCenter
        self.offset=self.test.viewOffset
        self.screenSize=self.test.screenSize

    def EndDraw(self): pass

    
    def DrawSolidPolygon(self, vertices, color):
       
        if  type(color)==b2Color:
             
            color=color.bytes
        if not vertices:
            return

        if len(vertices) == 2:
            pygame.draw.aaline(self.surface, color, vertices[0], vertices[1])
        else:
            pygame.draw.polygon(self.surface, color, vertices, 0)
          #  pygame.draw.polygon(self.surface, (color/2).bytes+[127], vertices, 0)
            pygame.draw.polygon(self.surface, color, vertices, 1)
 

class PygameFramework(FrameworkBase):
    def setup_keys(self):
        keys = [s for s in dir(pygame.locals) if s.startswith('K_')]
        for key in keys:
            value=getattr(pygame.locals, key)
            setattr(Keys, key, value)

    def __reset(self):
        # Screen/rendering-related
        self._viewZoom          = 10.0
        self._viewCenter        = None
        self._viewOffset        = None
        self.screenSize         = None
        self.rMouseDown         = False
        self.textLine           = 30
        self.font               = None
        self.fps                = 0

        
        self.setup_keys()
        
    def __init__(self):
        super(PygameFramework, self).__init__()

        self.__reset()
        print('Initializing pygame framework...')
        # Pygame Initialization
        pygame.init()
        caption= "Python Box2D Testbed - " + self.name
        pygame.display.set_caption(caption)

        # Screen and debug draw
        self.screen = pygame.display.set_mode( (800,600) )
        self.screenSize = b2Vec2(*self.screen.get_size())

        self.renderer = PygameDraw(surface=self.screen, test=self)
        self.world.renderer=self.renderer
        
        try:
            self.font = pygame.font.Font(None, 15)
            self.font2 = pygame.font.Font(None, 35)
            self.font3 = pygame.font.Font(None, 75)
        except IOError:
            try:
                self.font = pygame.font.Font("freesansbold.ttf", 15)
                self.font2 = pygame.font.Font("freesansbold.ttf", 35)
                self.font3 = pygame.font.Font("freesansbold.ttf", 75)
            except IOError:
                print("Unable to load default font or 'freesansbold.ttf'")
                print("Disabling text drawing.")
                self.Print = lambda *args: 0
                self.DrawStringAt = lambda *args: 0
        self.fonts=[self.font,self.font2,self.font3]
         

        self.viewCenter = (0,20.0)
        self.groundbody = self.world.CreateBody()

    def setCenter(self, value):
        """
        Updates the view offset based on the center of the screen.
        
        Tells the debug draw to update its values also.
        """
        self._viewCenter = b2Vec2( *value )
        self._viewCenter *= self._viewZoom
        self._viewOffset = self._viewCenter - self.screenSize/2
    
    def setZoom(self, zoom):
        self._viewZoom = zoom

    viewZoom   = property(lambda self: self._viewZoom, setZoom,
                           doc='Zoom factor for the display')
    viewCenter = property(lambda self: self._viewCenter/self._viewZoom, setCenter, 
                           doc='Screen center in camera coordinates')
    viewOffset = property(lambda self: self._viewOffset,
                           doc='The offset of the top-left corner of the screen')

    def checkEvents(self):
        """
        Check for pygame events (mainly keyboard/mouse events).
        Passes the events onto the GUI also.
        """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == Keys.K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key, down=True)
            elif event.type == KEYUP:
                self._Keyboard_Event(event.key, down=False)
            
 

        return True

    def run(self):
         

        running = True
        self.clock = pygame.time.Clock()
        while running:
            running = self.checkEvents()
            self.screen.fill( (28,28,28) )
 
            self.CheckKeys()

            
            self.SimulationLoop()

          

            pygame.display.flip()
            self.clock.tick(self.settings.hz)
            self.fps = self.clock.get_fps()
    
        self.world.contactListener = None
        self.world.destructionListener=None
        self.world.renderer=None

    def _Keyboard_Event(self, key, down=True):
        
        if down:
            if key==Keys.K_p:    
                self.settings.pause=not self.settings.pause
            else:              
                self.Keyboard(key)
        else:
            self.KeyboardUp(key)

    def CheckKeys(self):
       
        pygame.event.pump()
        self.keys = keys = pygame.key.get_pressed()
       
    def Step(self, settings):
       

        super(PygameFramework, self).Step(settings)

         

    

    def ConvertScreenToWorld(self, x, y):
        return b2Vec2((x + self.viewOffset.x) / self.viewZoom, 
                           ((self.screenSize.y - y + self.viewOffset.y) / self.viewZoom))

    def DrawStringAt(self, x, y, str, color=(229,153,153,255),font=1):
        
        self.screen.blit(self.fonts[font].render(str, True, color), (x,y))

    def Print(self, str, color=(229,153,153,255)):
        
        self.screen.blit(self.font.render(str, True, color), (5,self.textLine))
        self.textLine += 15

    def Keyboard(self, key):
        
        pass

    def KeyboardUp(self, key):
         
        pass

