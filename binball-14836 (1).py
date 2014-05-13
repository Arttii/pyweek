import Tkinter
import random

def intToBin(a):
    # Takes a integer, returns a string with the binary notation
    # example: imput: 10 output: '1010'
    # alternative: return bin(10)[2:]
    return '{0:b}'.format(a)

def getRandomBin():
    # returns a random binary representation of numbers 0-255
    return intToBin(random.randint(255))

def drawBinLine(number, x, y):
    canvas.create_rectangle(x, y, x + 780, y + 38, outline = "brown", activeoutline = "red", width= 1, tags=('number' + str(number)))
    canvas.create_text(x + 10, y + 2, anchor = 'nw', text = str(number), font = ('Helvetica', '24'))
    binString = intToBin(number)
    print binString
    xStart = 200
    for i in range(0, 8):
        offset = i * (36 + 20)
        if i > 3: offset += 40
        binRepr = binString[i]
        if binRepr == '0':
            canvas.create_oval(x + xStart + offset, y + 2, x + xStart + offset + 36, y + 36, outline = "black", fill = '#82ecbc', activeoutline = "red", width = 2, tags=('ovalNumber' + str(number) + '_' + str(i), 'oval'))
        else:
            canvas.create_oval(x + xStart + offset, y + 2, x + xStart + offset + 36, y + 36, outline = "black", fill = '#2e7b85',activeoutline = "red", width = 2, tags=('ovalNumber' + str(number) + '_' + str(i), 'oval'))

def moveBall():
    itemNumber = canvas.find_withtag('playerBall')
    canvas.move(itemNumber, +5, 0)
    #print canvas.itemcget(itemNumber, 'y')
    coords = canvas.coords(itemNumber)
    if coords[2] > 850:
        canvas.move(itemNumber, -850, 0)
    master.after(30, moveBall)

# init Tkinter

canvas.create_rectangle(0, 0, 800, 800, fill='#00cccc', tags = ('background'))

canvas.create_text(2, 2, anchor = 'nw', text = 'Press Space to release the ball! Hit the bright bits!', font = ('Helvetica', '18'))
canvas.create_oval(30, 30, 30 + 36, 30 + 36, outline = "black", fill = '#8800cc', activeoutline = "red", width = 2, tags=('playerBall'))

# build the numbers 255-0 backwards
for i in range(0, 15):
    number = 255 - i
    drawBinLine(number, 10, 200 + i * 40)

master.after(30, moveBall)
Tkinter.mainloop()
