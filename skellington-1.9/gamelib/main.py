#  Copyright (c) 2010 Artyom topchyan
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



from .framework import *
import framework
from math import *
import numpy as np
from collections import defaultdict
import random
from random import shuffle
def sign(number):
    return cmp(number, 0)

def intToBin(a):
    # Takes a integer, returns a string with the binary notation
    # example: imput: 10 output: '1010'
    # alternative: return bin(10)[2:]
    return '{0:b}'.format(a).zfill(8)

def fix_vertices(self,vertices):
        return [ self.renderer.to_screen(v) for v in vertices] 


class Game(Framework):
    colors=[(178,24,43),(214,96,77),(244,165,130),(253,219,199),(247,247,247),(209,229,240),(146,197,222),(67,147,195),(33,102,172)]
    trash=0
    name = "MotorJoint"
    description = 'g to stop/go'
    count = 800
    lasttime=0
    top_position = 45
    levy_width,levy_height = 2,0.5
    bits=defaultdict(lambda:[0,None])
    hit=0 
    miss=0
    num=256
    cheat=False
    gameover=False
    attached=True
    time_elapsed_since_last_action = 0
    bodies=[]
    current=0
    def __init__(self):
        Framework.__init__(self)

        self.world.gravity=(0,-20)
        self.numbers=range(1,self.num)
        shuffle(self.numbers)
        ground = self.world.CreateStaticBody( shapes=[
                         
                        b2PolygonShape(box=( 40, 0.5, (0, 0), 0)),
                        b2PolygonShape(box=( 40, 0.5, (0, 0), 0)),
                    ],userData='ground', allowSleep=False)
        self.groundbody=ground
        top = self.world.CreateStaticBody(shapes=[b2EdgeShape(vertices=[(-1, self.top_position), (1, self.top_position)])],userData=["top"])
        # Define motorized body
        body = self.world.CreateDynamicBody(position=(0, self.top_position - 2),
            allowSleep=False,userData=["llevy"],

            fixtures=b2FixtureDef(density=2.0, friction=0.6,
                                  shape=b2PolygonShape(box= (self.levy_width, self.levy_height)),),)

        

        self.crane = self.world.CreatePrismaticJoint(bodyA=top,
            bodyB=body,
            anchor=(0,self.top_position),
            axis=(1, 0),
            maxMotorForce = 10000000000,maxMotorTorque=100000000,
            motorSpeed=15,
            enableMotor = True,
            lowerTranslation = -35,
            upperTranslation = 35,
            enableLimit = True)
        self.body = body

        prevBody = body

        #    prevBody = body1
        N = 3
        y = self.top_position - 2.5
        shape = b2PolygonShape(box=(0.2, 0.125))
        fd = b2FixtureDef(shape=shape,
            friction=0.2,
            density=20,
            categoryBits=0x0001,
            maskBits=(0xFFFF & ~0x0002),)
        prevBody = body
        self.levy=body
        self.crane_parts=[]
        for i in range(N):
            i = i / float(2)
            body1 = self.world.CreateDynamicBody(position=(0.3 + i, y),
                    fixtures=fd,)


            self.crane_parts.append(body1)
            self.connection = self.world.CreateRevoluteJoint(bodyA=prevBody,
                bodyB=body1,
                anchor=(i, y),
                collideConnected=False,)

            prevBody = body1

        extraLength = 0.01
        self.rd = rd = b2RopeJointDef(bodyA=body,
            bodyB=body1,
            maxLength=N - 1.0 + extraLength,
            localAnchorA=(0, -self.levy_height * 2),
            localAnchorB=(0, 0))
        self.rope = self.world.CreateJoint(rd)

        
        self.go = False
        self.time = 0.0

        self.last_link=body1
        shape.box = (0.5, 0.5)
        fd.density = 1
        fd.categoryBits = 0x0002
        self.payload = self.world.CreateDynamicBody(position=(i + 1, y),mass=2,
            fixtures=fd,userData=['payLoad'], allowSleep=False,
            angularDamping=1,)
        
        self.connection = self.world.CreateRevoluteJoint(bodyA=body1,
                bodyB=self.payload,
                collideConnected=False,)

        self.fd=fd
        
        self.generate_bit()
        self.using_contacts=True

    def Keyboard(self, key):
        if key == Keys.K_F1:
           self.cheat=not self.cheat
        if key == Keys.K_n:
           self.reset()
        if key == Keys.K_SPACE:
            if self.attached:
                self.world.DestroyJoint(self.connection)
                self.attached=False

    def reset(self):
        for b in self.world.bodies:
             if b.userData=='trash':
                 self.world.DestroyBody(b)
        for k,i in enumerate(self.bits.values()):
                if i[1]:
                     
                    self.bits[k][1]=None
                    self.bodies[k].userData="trash"
                    
                     
        for b in self.world.bodies:
             if b.userData=='trash':
                 self.world.DestroyBody(b)

        self.numbers=range(1,self.num)
        self.current=0
        shuffle(self.numbers)
        self.hit=0
        self.miss=0
        if not self.attached:self.attachPayload()  
        self.generate_bit()       

    def generate_bit(self):    
         
        if self.current> len(self.numbers)-1:
            return                 
        
        self.number = self.numbers[self.current]
       
        up_bits=[ self.world.CreateDynamicBody(position=(i*10-36, 3),
            allowSleep=False,userData=["bit",i,False],
            fixtures=b2FixtureDef(density=200.0, friction=0.6,
                                  shape=b2PolygonShape(box= (3,3)),),) for i in range(4)]
        low_bits=[self.world.CreateDynamicBody(position=(i*10+6, 3),
            allowSleep=False,userData=["bit",i+4,False],
            fixtures=b2FixtureDef(density=200.0, friction=0.6,
                                  shape=b2PolygonShape(box= (3,3)),),) for i in range(4)]

         
        bits=up_bits+low_bits
        self.bodies=bits
        binString = intToBin( self.number)
        self.bin=binString
        for i,b in enumerate(bits):
            binRepr = binString[i]
            self.bits[i]=[binRepr,b]
    def clean(self):
          for b in self.world.bodies:
             if b.userData=='trash':
                 self.world.DestroyBody(b)   
          self.trash=0          
    def next(self):
        
        if self.current> len(self.numbers)-1:
            return

        self.hit=self.hit+1
        self.clean
        for k,i in enumerate(self.bits.values()):
                if i[1]:
                     
                    self.bits[k][1]=None
                    self.bodies[k].userData="trash"
                     
        self.clean()
        if self.settings.increase:
            self.crane.motorSpeed=self.crane.motorSpeed+0.0005*self.hit
        self.current=self.current+1    
        self.attachPayload()  
        self.generate_bit()       
                     
    def restart(self):
        if self.current> len(self.numbers)-1:
            return
        self.miss=self.miss+1
        
        self.clean()
        for k,i in enumerate(self.bits.values()):
                if i[1]:
                     
                    self.bits[k][1]=None
                    self.bodies[k].userData="trash"
                     
        self.clean()
        self.current=self.current+1                 
        self.attachPayload()  
        self.generate_bit()       
       
         
            
    def attachPayload(self):

            
            position=self.last_link.position.x-1,self.last_link.position.y-1
            self.payload = self.world.CreateDynamicBody(position=position,mass=200,
                fixtures=self.fd,userData=['payLoad'],
                angularDamping=1,)

            self.connection = self.world.CreateRevoluteJoint(bodyA=self.last_link,
                    bodyB=self.payload,
                    collideConnected=False,)
            self.attached=True
    def fix_vertices(self,vertices):
        return [ self.renderer.to_screen(v) for v in vertices] 

    def Step(self, settings):
       
        self.time +=1/60.0
        
        dt=self.time-self.lasttime
        self.lasttime=self.time
        self.time_elapsed_since_last_action += dt
    # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
        if  self.time_elapsed_since_last_action > ( 120-0.43*self.hit) and settings.randomevent:
             coin=      random.random()
             if coin>0.5:
                self.crane.motorSpeed=- self.crane.motorSpeed
             self.time_elapsed_since_last_action = 0


        if self.crane.upperLimit < self.crane.translation or self.crane.lowerLimit > self.crane.translation:
            self.crane.motorSpeed = -self.crane.motorSpeed


      
        nuke = []
        
        
        body_pairs = [(p['fixtureA'].body, p['fixtureB'].body) for p in self.points]
        error=False
        for body1, body2 in body_pairs:
            data1,data2 = body1.userData, body2.userData
            
            if data1 and data2:
               if data1[0] =='payLoad' or data2[0] =="payLoad":
                    if data1[0] =="payLoad":

                        if data2[0]=='bit':
                           if self.bits[data2[1]][0]=='0':
                              body1.userData='trash'
                              self.trash=self.trash+1
                              error=True
                               
                           else:
                              body1.userData='trash'
                              self.trash=self.trash+1
                              body2.userData[2]=True
                              self.attachPayload()
                               
                              

                        elif data2=='ground':
                             body1.userData='trash'
                             self.trash=self.trash+1
                             self.attachPayload()
                              
                       
                    else:
                        if data1[0]=='bit':
                           if self.bits[data1[1]][0]=='0':
                              body2.userData='trash'
                              self.trash=self.trash+1
                              error=True
                               
                           else:
                              body2.userData='trash'
                              self.trash=self.trash+1
                              body1.userData[2]=True
                              self.attachPayload()
                               
                              

                        elif data1=='ground':
                             body2.userData='trash'
                             self.trash=self.trash+1
                             self.attachPayload()
                              
                     
        
        

        if  self.payload.position.y<-30:
            if not self.world.locked:
                self.world.DestroyBody(self.payload)
            self.attachPayload()

        if self.trash>settings.keeptrash:self.clean()
        correct=''.join([str(int(item.userData[2]))  for item in self.bodies if item.userData[0]=='bit'])
        if correct==self.bin:
            self.next()
        if error:
            self.restart()              
        # Destroy the bodies, skipping duplicates.
        if self.current> len(self.numbers)-1:
            if self.hit==len(self.numbers):
                    self.DrawStringAt(50,300,"8 Bit champion wohoooo!",color=self.colors[0],font=2)
                    self.DrawStringAt(50,350,"Press N for new game",color=self.colors[0],font=2)

                 
            else:
                    self.DrawStringAt(50,300,"You got {miss} wrong and {hit} right.".format(miss=str(self.miss),hit=str(self.hit)),color=self.colors[0],font=2)
                    self.DrawStringAt(50,350,"Press N for new game",color=self.colors[0],font=2)

      

        currentnumber=int(correct, 2)
        self.DrawStringAt(160,520,"Current:"+str(currentnumber),color=(53,151,143),font=2)
        self.DrawStringAt(485,520,"Number:"+str(self.number),color=self.colors[0],font=2)
        #self.DrawStringAt(100,555,str(self.bin),color=(1,1,1))
        self.DrawStringAt(5,520,"Correct:%s"%self.hit,color=(255,255,255))
        self.DrawStringAt(5,550,"Incorrect:%s"%self.miss,color=(255,255,255))
       
        vertices=self.transform(self.groundbody)
        self.renderer.DrawSolidPolygon(vertices,self.colors[8])
        try:
          
            for k,i in enumerate(self.bits.values()):
                    if i[1]:

                        vertices=self.transform(i[1])
                        if i[1].userData[2]:
                            self.renderer.DrawSolidPolygon(vertices,(240,59,32))
                        else:
                            self.renderer.DrawSolidPolygon(vertices,self.colors[6])

        except:
            a=1
        vertices=self.fix_vertices (b2PolygonShape(box=( 40, 5.5, (0, 50), 0)).vertices)
        self.renderer.DrawSolidPolygon(vertices,(22,22,22))
        vertices=self.transform(self.levy)
        self.renderer.DrawSolidPolygon(vertices,self.colors[0])
        vertices=self.transform(self.payload)
        self.renderer.DrawSolidPolygon(vertices,(252,78,42))
        for i in self.crane_parts:
             vertices=self.transform(i)
             self.renderer.DrawSolidPolygon(vertices,self.colors[1])
        for i in self.world.bodies:
            if i.userData=='trash':
             vertices=self.transform(i)
             self.renderer.DrawSolidPolygon(vertices,self.colors[4])

        
        if self.cheat:  
            self.DrawStringAt(485,10,str(self.bin),color=(44,162,95),font=2)
        else:
            self.DrawStringAt(485,10,"Hint - F1",color=(44,162,95),font=2)

        self.DrawStringAt(5,2,"New game - N",color=(255,255,255),font=1)
        self.DrawStringAt(5,25,"Pause - P",color=(255,255,255),font=1)
        self.DrawStringAt(175,2,"Release bit - Space",color=(255,255,255),font=1)
         
        super(Game, self).Step(settings)


    def PostSolve(self, contact, impulse):
        pass

    def transform(self,body):
        try:
            verts =body.fixtures[0].shape.vertices
            transform = body.transform
     
            return self.fix_vertices([transform * v for v in verts])
        except:
            return [(0,0),(0,0)]


 
def main():
    framework.main(Game)
 