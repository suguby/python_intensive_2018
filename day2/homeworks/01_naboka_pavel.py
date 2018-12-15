# -*- coding: utf-8 -*-

import math
import os
import random
import turtle
from builtins import property, range

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5
GUN_X = 0
GUN_Y = -300


class Missile:

    def __init__(self, x, y, color, x2, y2):
        self.x = x
        self.y = y
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
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
            self.pen.forward(4)
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


class Base:

    def __init__(self, x, y, type):
        self.position_x = x
        self.position_y = y
        self.model = type
        self.health = 2000
        self.hit_damage = 100

        pen_base = turtle.Turtle(visible=False)
        pen_base.speed(0)
        pen_base.penup()
        pen_base.setpos(x=x, y=y)
        picture = os.path.join(BASE_PATH, "images", "%s.gif" % type)
        window.register_shape(picture)
        pen_base.shape(picture)
        pen_base.showturtle()

    def hit_missle(self):
        old_health = self.health
        self.health = self.health - self.hit_damage
        print("Base health: %d => %d\n" % (old_health, self.health))

    def destroy(self):
        return self.health < 0

    @property
    def x(self):
        return self.position_x

    @property
    def y(self):
        return self.position_y


def fire_missile(x, y):
    info = Missile(color='white', x=GUN_X, y=GUN_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    target = random.randint(0, number_of_bases - 1)
    info = Missile(color='red', x=x, y=y, x2=our_bases[target].x, y2=our_bases[target].y)
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
            if enemy_missile.distance(our_missile.pen.xcor(), our_missile.pen.ycor()) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []
our_bases = []


def game_over():
    for base in our_bases:
        if base.destroy():
            return True
    return False


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        for base in our_bases:
            if enemy_missile.distance(base.x, base.y) < enemy_missile.radius * 10:
                base.hit_missle()


number_of_bases = 2
for iterator in range(number_of_bases):
    info = Base(0, -300, 'base')
    our_bases.append(info)

while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
