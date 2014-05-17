 

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
