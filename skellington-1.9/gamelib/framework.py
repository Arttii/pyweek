
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


from Box2D import *
from .settings import fwSettings
from time import time

 

class fwDestructionListener(b2DestructionListener):
    
    test = None
    def __init__(self, **kwargs):
        super(fwDestructionListener, self).__init__(**kwargs)

    def SayGoodbye(self, object):
        if isinstance(object, b2Joint):
            if self.test.mouseJoint==object:
                self.test.mouseJoint=None
            else:
                self.test.JointDestroyed(object)
        elif isinstance(object, b2Fixture):
            self.test.FixtureDestroyed(object)

class fwQueryCallback(b2QueryCallback):
    def __init__(self, p): 
        super(fwQueryCallback, self).__init__()
        self.point = p
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2_dynamicBody:
            inside=fixture.TestPoint(self.point)
            if inside:
                self.fixture=fixture
              
                return False
         
        return True

class Keys(object):
    pass

class FrameworkBase(b2ContactListener):
    

    def __reset(self):
      
        self.points             = []
        self.world              = None 
        self.settings           = fwSettings
        self.using_contacts     = False
        self.stepCount          = 0
 
        self.destructionListener= None
        self.renderer           = None

    def __init__(self):
        super(FrameworkBase, self).__init__()

        self.__reset()

        # Box2D Initialization
        self.world = b2World(gravity=(0,-10), doSleep=True)

        self.destructionListener = fwDestructionListener(test=self)
        self.world.destructionListener=self.destructionListener
        self.world.contactListener=self
        self.t_steps, self.t_draws=[], []
 

    def Step(self, settings):
       
        self.stepCount+=1
        
        if settings.hz > 0.0:
            timeStep = 1.0 / settings.hz
        else:
            timeStep = 0.0
        
       
        if settings.pause:
            if settings.singleStep:
                settings.singleStep=False
            else:
                timeStep = 0.0
 
        self.world.warmStarting=settings.enableWarmStarting
        self.world.continuousPhysics=settings.enableContinuous
        self.world.subStepping=settings.enableSubStepping

       
        self.points = []

        
        t_step=time()
        self.world.Step(timeStep, settings.velocityIterations, settings.positionIterations)
        self.world.ClearForces()
        t_step=time()-t_step

      
        t_draw=time()
        if self.renderer:
            self.renderer.StartDraw()
            self.renderer.EndDraw()
        
 

     
    def SimulationLoop(self):
         
        self.Step(self.settings)

    def ConvertScreenToWorld(self, x, y):
        """
        Return a b2Vec2 in world coordinates of the passed in screen coordinates x, y
        NOTE: Renderer subclasses must implement this
        """
        raise NotImplementedError()

    def DrawStringAt(self, x, y, str, color=(229,153,153,255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        NOTE: Renderer subclasses must implement this
        """
        raise NotImplementedError()

    def Print(self, str, color=(229,153,153,255)):
        """
        Draw some text at the top status lines
        and advance to the next line.
        NOTE: Renderer subclasses must implement this
        """
        raise NotImplementedError()

    def PreSolve(self, contact, old_manifold):
        """
        This is a critical function when there are many contacts in the world.
        It should be optimized as much as possible.
        """
        if not (self.settings.drawContactPoints or self.settings.drawContactNormals or self.using_contacts):
            return
        elif len(self.points) > self.settings.maxContactPoints:
            return

        manifold = contact.manifold
        if manifold.pointCount == 0:
            return

        state1, state2 = b2GetPointStates(old_manifold, manifold)
        if not state2:
            return

        worldManifold = contact.worldManifold
        
        for i, point in enumerate(state2):
            # TODO: find some way to speed all of this up.
            self.points.append(
                    {
                        'fixtureA' : contact.fixtureA,
                        'fixtureB' : contact.fixtureB,
                        'position' : worldManifold.points[i],
                        'normal' : worldManifold.normal,
                        'state' : state2[i]
                    }  )

   

    def FixtureDestroyed(self, fixture):
        """
        Callback indicating 'fixture' has been destroyed.
        """
        pass

    def JointDestroyed(self, joint):
        """
        Callback indicating 'joint' has been destroyed.
        """
        pass

    def Keyboard(self, key):
        """
        Callback indicating 'key' has been pressed down.
        """
        pass

    def KeyboardUp(self, key):
        """
        Callback indicating 'key' has been released.
        """
        pass

def main(game):
    """
    Loads the test class and executes it.
    """
    print("Loading Angry bits")
    temp = game()
    temp.run()
 
from .pygame_framework import PygameFramework as Framework
#s/\.Get\(.\)\(.\{-\}\)()/.\L\1\l\2/g
