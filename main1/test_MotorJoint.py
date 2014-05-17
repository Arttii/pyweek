#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version by Ken Lauer / sirkne at gmail dot com
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

from framework import *
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


class MotorJoint(Framework):
    name = "MotorJoint"
    description = 'g to stop/go'
    count = 800
    top_position = 40
    levy_width,levy_height = 2,0.5
    bits=defaultdict(lambda:[0,None])
    hit=0 
    miss=0
    gameover=False
    attached=True
    bodies=[]
    current=0
    def __init__(self):
        Framework.__init__(self)

        self.world.gravity=(0,-20)
        self.numbers=range(1,2)
        shuffle(self.numbers)
        ground = self.world.CreateStaticBody( shapes=[
                         
                        b2PolygonShape(box=( 30, 0.5, (0, 0), 0)),
                        b2PolygonShape(box=( 30, 0.5, (0, 0), 0)),
                    ],userData='ground', allowSleep=False)
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
            lowerTranslation = -25,
            upperTranslation = 25,
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
        for i in range(N):
            i = i / float(2)
            body1 = self.world.CreateDynamicBody(position=(0.3 + i, y),
                    fixtures=fd,)



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

      #  self.joint = self.world.CreateMotorJoint(bodyA=ground,
      #  bodyB=body,localAnchorA=(10,10),localAnchorB=[0,0],
                             # maxForce=1000000, maxTorque=1000000)
        
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

        if key == Keys.K_n:
           self.reset()
        if key == Keys.K_g:
            self.go = not self.go
        if key == Keys.K_c:
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

        self.numbers=range(1,2)
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
       
        up_bits=[ self.world.CreateDynamicBody(position=(i*6-24, 3),
            allowSleep=False,userData=["bit",i,False],
            fixtures=b2FixtureDef(density=200.0, friction=0.6,
                                  shape=b2PolygonShape(box= (2,2)),),) for i in range(4)]
        low_bits=[self.world.CreateDynamicBody(position=(i*6+6, 3),
            allowSleep=False,userData=["bit",i+4,False],
            fixtures=b2FixtureDef(density=200.0, friction=0.6,
                                  shape=b2PolygonShape(box= (2,2)),),) for i in range(4)]

         
        bits=up_bits+low_bits
        self.bodies=bits
        binString = intToBin( self.number)
        self.bin=binString
        for i,b in enumerate(bits):
            binRepr = binString[i]
            self.bits[i]=[binRepr,b]
           
    def next(self):
        if self.current> len(self.numbers)-1:
            return

        self.hit=self.hit+1
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
        self.current=self.current+1    
        self.attachPayload()  
        self.generate_bit()       
                     
    def restart(self):
        if self.current> len(self.numbers)-1:
            return
        self.miss=self.miss+1
        
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
        self.current=self.current+1                 
        self.attachPayload()  
        self.generate_bit()       
       

        
        
            
    def attachPayload(self):

            if self.current> len(self.numbers)-1 :
                 return
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
       
        self.time += 1.0 / settings.hz
        if self.crane.upperLimit < self.crane.translation or self.crane.lowerLimit > self.crane.translation:
            self.crane.motorSpeed = -self.crane.motorSpeed


        # We are going to destroy some bodies according to contact
        # points. We must buffer the bodies that should be destroyed
        # because they may belong to multiple contact points.
        nuke = []
        
        # Traverse the contact results. Destroy bodies that
        # are touching heavier bodies.
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
                              error=True
                               
                           else:
                              body1.userData='trash'
                              body2.userData[2]=True
                             # self.attachPayload()
                               
                              

                        elif data2=='ground':
                             body1.userData='trash'
                            
                             self.attachPayload()
                              
                       
                    else:
                        if data1[0]=='bit':
                           if self.bits[data1[1]][0]=='0':
                              body2.userData='trash'
                              error=True
                               
                           else:
                              body2.userData='trash'
                              body1.userData[2]=True
                              #self.attachPayload()
                               
                              

                        elif data1=='ground':
                             body2.userData='trash'
                             
                             self.attachPayload()
                              
                     
        
        

        if  self.payload.position.y<-30:
            if not self.world.locked:
                self.world.DestroyBody(self.payload)
            self.attachPayload()
        
        correct=''.join([str(int(item.userData[2]))  for item in self.bodies if item.userData[0]=='bit'])
        if correct==self.bin:
            self.next()
        if error:
            self.restart()              
        # Destroy the bodies, skipping duplicates.
        if self.current> len(self.numbers)-1:
            if self.hit==len(self.numbers):
                    self.DrawStringAt(50,50,"8 Bit champion wohoooo!",color=(255,255,255))
                    self.DrawStringAt(50,100,"Press n for new game",color=(255,255,255))

                 
            else:
                    self.DrawStringAt(50,50,"You got {miss} wrong and {hit} right.".format(miss=str(self.miss),hit=str(self.hit)),color=(255,255,255))
                    self.DrawStringAt(50,100,"Press n for new game",color=(255,255,255))

       
        #self.renderer.DrawPoint(renderer.to_screen(linear_offset),
                               #4, b2Color(0, 0, 0))
        self.DrawStringAt(10,455,"Number:"+str(self.number),color=(255,255,255))
        self.DrawStringAt(100,455,str(self.bin),color=(1,1,1))
        self.DrawStringAt(200,455,"Correct number %s"%self.hit,color=(1,1,1))
        self.DrawStringAt(300,455,"Incorrect numbers %s"%self.miss,color=(1,1,1))
          
        for k,i in enumerate(self.bits.values()):
                if i[1]:

                    vertices=self.transform(i[1])
                    if i[1].userData[2]:
                        self.renderer.DrawSolidPolygon(vertices,b2Color(1,1,1))
                    else:
                        self.renderer.DrawSolidPolygon(vertices,b2Color(0.5,0.5,0.5))
       
        super(MotorJoint, self).Step(settings)


    def PostSolve(self, contact, impulse):
        pass

    def transform(self,body):
        verts =body.fixtures[0].shape.vertices
        transform = body.transform
     
        return self.fix_vertices([transform * v for v in verts])


if __name__ == "__main__":
    main(MotorJoint)
