import Tkinter
import random
import pdb
from math import *
target = []
thrust = 10


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
Tkinter.Canvas.create_circle = _create_circle


def intToBin(a):
    # Takes a integer, returns a string with the binary notation
    # example: imput: 10 output: '1010'
    # alternative: return bin(10)[2:]
    return '{0:b}'.format(a).zfill(8)


def getRandomBin():
    # returns a random binary representation of numbers 0-255
    return intToBin(random.randint(255))


def drawBinLine(number, x, y):
    canvas.create_rectangle(x, y, x + 780, y + 38, outline="brown",
                            activeoutline="red", width=1, tags=('number' + str(number)))
    canvas.create_text(x + 10, y + 2, anchor='nw',
                       text=str(number).zfill(3), font=('Helvetica', '24'))
    binString = intToBin(number)
    # print binString
    xStart = 200
    for i in range(0, 8):
        offset = i * (36 + 20)
        if i > 3:
            offset += 40
        binRepr = binString[i]
        if binRepr == '0':
            canvas.create_oval(
                x + xStart + offset, y + 2, x + xStart + offset + 36, y + 36, outline="black",
                fill='#82ecbc', activeoutline="red", width=2, tags=('ovalNumber' + str(number) + '_' + str(i), 'oval'))
        else:
            canvas.create_oval(
                x + xStart + offset, y + 2, x + xStart + offset + 36, y + 36, outline="black",
                fill='#2e7b85', activeoutline="red", width=2, tags=('ovalNumber' + str(number) + '_' + str(i), 'oval'))


def move_in_direction(itemNumber,target):

    coords = canvas.coords(itemNumber)

    # a bit hacky at the moment

    tx = target[0] -  (coords[0]+18)
    ty = target[1] - (coords[1]+18)
    dist = sqrt(tx * tx + ty * ty)

    velX = (tx / dist) * thrust
    velY= (ty / dist) * thrust
    canvas.move(itemNumber, velX, velY)


def moveBall():
    global target
    itemNumber = canvas.find_withtag('playerBall')
    move_in_direction(itemNumber,target)
    #canvas.move(itemNumber, 0, 10)
    coords = canvas.coords(itemNumber)
    if coords[3] > 850:
        canvas.move(itemNumber, 0, -750)
    else:
        master.after(30, moveBall)


def drawShootingLine(event, *rest):
    # print event.x, event.y
    newCoords = canvas.coords(shootingLineItemNumber)
    mouseX = event.x
    mouseY = event.y
    lineStartX = int(newCoords[0])
    lineStartY = int(newCoords[1])
    newCoords = (lineStartX, lineStartY, mouseX, mouseY)
    canvas.coords(shootingLineItemNumber, newCoords)

    #master.after(30, drawShootingLine)


def mouseClicked(event, *rest):
    global target #need to put ball in a class
    target = [event.x, event.y]
    master.after(30, moveBall)

# init Tkinter
master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width=800, height=800, bd=-2)
canvas.pack(fill=Tkinter.BOTH, expand=1,
            ipadx=0, ipady=0, padx=0, pady=0)
canvas.create_rectangle(0, 0, 800, 800, fill='#00cccc', tags=('background'))

canvas.create_text(230, 5, anchor='nw',
                   text='Point with the mouse to shoot the ball!', font=('Helvetica', '18'))

# playfield
canvas.create_rectangle(180, 50, 700, 795, outline="green", width='2')

# build the numbers 255-0 backwards
for i in range(0, 15):
    #number = 255 - i
    number = random.randint(0, 255)
    drawBinLine(number, 10, 200 + i * 40)

# set starting ball
ballSize = 36
canvas.create_circle(450, 100, ballSize / 2,
                     outline="black", fill='#8800cc', activeoutline="red", width=2, tags=('playerBall'))


# build the shooting line
shootingLineItemNumber = canvas.create_line(450, 100, 450, 150, fill='red')
canvas.bind('<Motion>', drawShootingLine)
canvas.bind('<Button-1>', mouseClicked)
print canvas.coords(shootingLineItemNumber)

Tkinter.mainloop()
