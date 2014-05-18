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

class fwSettings(object):
    backend='simple'       

    # Physics options
    hz=60.0
    velocityIterations=384
    positionIterations=80
    enableWarmStarting=True  
    enableContinuous=True   
    enableSubStepping=False
    

    #gameoptions
        
    randomevent=True
    increase=True

    # Drawing
    drawStats=False
    drawShapes=False
    drawJoints=False
    drawCoreShapes=False
    drawAABBs=False
    drawOBBs=False
    drawPairs=False
    drawContactPoints=False
    maxContactPoints=100
    drawContactNormals=False
    drawFPS=False
    drawMenu=False             
    drawCOMs=False          
    pointSize=2.5  
    keeptrash=10        

    # Miscellaneous  options
    pause=False
    singleStep=False
    onlyInit=False            

 
from optparse import OptionParser

parser = OptionParser()
list_options = [i for i in dir(fwSettings) if not i.startswith('_')]

for opt_name in list_options:
    value = getattr(fwSettings, opt_name)
    if isinstance(value, bool):
        if value:
            parser.add_option('','--NO'+opt_name, dest=opt_name, default=value,
                              action='store_'+str(not value).lower(),
                              help="don't "+opt_name)
        else:
            parser.add_option('','--'+opt_name, dest=opt_name, default=value,
                              action='store_'+str(not value).lower(),
                              help=opt_name)
            
    else:
        if isinstance(value, int):
            opttype = 'int'
        elif isinstance(value, float):
            opttype = 'float'
        else:
            opttype = 'string'
        parser.add_option('','--'+opt_name, dest=opt_name, default=value,
                          type=opttype,
                          help='sets the %s option'%(opt_name,))


(fwSettings, args) = parser.parse_args()
