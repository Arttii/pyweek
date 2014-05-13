import Tkinter
import random
import numpy as np
import Box2D as box  # The main library
from Box2D.b2 import *  # This maps Box2D.b2Vec2 to vec2 (and so on)
import pdb


# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 30
ITME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# pretty colors
colors = ['#A50026', '#D73027', '#F46D43', '#FDAE61', '#FEE090',
          '#E0F3F8', '#ABD9E9', '#74ADD1', '#4575B4', '#313695']

# --- tkinter setup ---
master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width=800, height=800, bd=-2)
canvas.pack(fill=Tkinter.BOTH, expand=1,
            ipadx=0, ipady=0, padx=0, pady=0)

canvas.create_rectangle(0, 0, 800, 800, fill=colors[6], tags=('background'))


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
Tkinter.Canvas.create_circle = _create_circle


# --- pybox2d world setup ---
# Create the world
world = box.b2World(gravity=(0, -10), doSleep=True)


# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(
    position=(0, 1),
    shapes=polygonShape(box=(50, 5)),
)

# Create a dynamic body
dynamic_body = world.CreateDynamicBody(position=(10, 15), angle=15)

# And add a box fixture onto it (with a nonzero density, so it will move)
box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

body = world.CreateDynamicBody(position=(20, 15))
circle = body.CreateCircleFixture(radius=0.5, density=1, friction=0.3)
cpos = circle.shape.pos * PPM
body.userData = canvas.create_circle(
    cpos[0], cpos[1], circle.shape.radius * PPM, fill="blue", outline="#DDD", width=4)


items = []

# pdb.set_trace()

for body in (dynamic_body, ground_body):  # or: world.bodies
    for fixture in body.fixtures:
        shape = fixture.shape
        vertices = [(body.transform * v) * PPM for v in shape.vertices]
        vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
        body.userData = canvas.create_polygon(vertices, outline='white',
                                              fill=colors[2], width=2)


def update():

    for body in (world.bodies):
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    world.Step(TIME_STEP, 10, 10)
    master.after(30, update)


def update_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    x, y = position[0], SCREEN_HEIGHT - position[1]

    canvas_item = body.userData
    r = circle.radius * PPM

    canvas.coords(canvas_item, x - r, y - r, x + r, y + r)


def update_polygon(polygon, body, fixture):

    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [[v[0], SCREEN_HEIGHT - v[1]]
                for v in vertices]
    vertices = sum(vertices, [])
    canvas_item = body.userData
    canvas.coords(canvas_item, *vertices)
circleShape.draw = update_circle
polygonShape.draw = update_polygon
master.after(30, update)
master.after(30, draw)
Tkinter.mainloop()
