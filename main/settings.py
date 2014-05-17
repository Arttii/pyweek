 

class fwSettings(object):
    backend='pygame'        # The default backend to use in (can be: pyglet, pygame, etc.)

    # Physics options
    hz=60.0
    velocityIterations=384
    positionIterations=80
    enableWarmStarting=True   # Makes physics results more accurate (see Box2D wiki)
    enableContinuous=True     # Calculate time of impact
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
    drawMenu=False             # toggle by pressing F1
    drawCOMs=False            # Centers of mass
    pointSize=2.5  
    keeptrash=10           # pixel radius for drawing points

    # Miscellaneous testbed options
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
