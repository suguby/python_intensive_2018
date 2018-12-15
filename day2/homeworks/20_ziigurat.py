# The work of David
# работа Давида

import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENEMY_COUNT = 5
BASE_X, BASE_Y = 0, -300
FONT = ("Arial", 14, "bold")

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.screensize(1200, 800)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.tracer(n=2)


class Missile:

    def __init__(self, x, y, color, x2, y2, trace=True):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed('fastest')
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        if trace:
            pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(5)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


class Building:

    def __init__(self, pos, name, health):
        self.health = health
        self.text_pos = pos
        self.text_turtle = turtle.Turtle(visible=False)

        building = turtle.Turtle()
        building.hideturtle()
        building.penup()
        building.setpos(*pos)
        pic_path = os.path.join(BASE_PATH, "images", name)
        window.register_shape(pic_path)
        building.shape(pic_path)
        building.showturtle()

        self.building = building
        self.text_health()

    def text_health(self):
        self.text_turtle.reset()
        self.text_turtle.hideturtle()
        self.text_turtle.penup()
        self.text_turtle.goto(self.text_pos[0], self.text_pos[1] - 75)
        self.text_turtle.write(str(self.health), align="center", font=FONT)


class Graphics:

    def __init__(self, pos, text):
        self.text_turtle = turtle.Turtle(visible=False)
        self.text_turtle.speed('fastest')
        self.text_turtle.penup()
        self.text_turtle.goto(*pos)
        self.text_turtle.write(text, font=FONT)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    target = [i for i in buildings.values()]
    target = random.choice(target)
    info = Missile(color='red', x=x, y=y, x2=target[0], y2=target[1])
    enemy_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

our_building = []

buildings = {
    'base': (BASE_X, BASE_Y),
    'skyscraper': (-200, -300),
    'nuclear1': (250, -300),
    'nuclear2': (-320, -300),
}

base = Building(pos=buildings['base'], name='base.gif', health=2000)
skyscraper = Building(pos=buildings['skyscraper'], name='skyscraper_1.gif', health=1500)
nuclear_1 = Building(pos=buildings['nuclear1'], name='nuclear_1.gif', health=1450)
nuclear_2 = Building(pos=buildings['nuclear2'], name='nuclear_1.gif', health=1550)


def game_over():
    return base.health < 0


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue

        if enemy_missile.distance(*buildings['base']) < enemy_missile.radius * 10:
            base.health -= 100
            base.text_health()

        if enemy_missile.distance(*buildings['skyscraper']) < enemy_missile.radius * 10:
            skyscraper.health -= 100
            skyscraper.text_health()

        if enemy_missile.distance(*buildings['nuclear1']) < enemy_missile.radius * 10:
            nuclear_1.health -= 100
            nuclear_1.text_health()

        if enemy_missile.distance(*buildings['nuclear2']) < enemy_missile.radius * 10:
            nuclear_2.health -= 100
            nuclear_2.text_health()


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
