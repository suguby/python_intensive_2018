# -*- coding: utf-8 -*-

import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300


class Missile:

    def __init__(self, x, y, color, x2, y2):
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

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


class Building:
    def __init__(self, x, y, image, health):
        self.x = x
        self.y = y
        self.health = health
        self.image = image
        self.pic_path = os.path.join(BASE_PATH, "images", self.image)
        self.building = turtle.Turtle()
        self.building.hideturtle()
        self.building.speed(0)
        self.building.penup()
        self.building.setpos(x=x, y=y)
        window.register_shape(self.pic_path)
        self.building.shape(self.pic_path)
        self.building.showturtle()

    def missiles_attack(self, attacking_missiles):
        for attacking_missile in attacking_missiles:
            if attacking_missile.state != 'explode':
                continue
            if attacking_missile.distance(self.x, self.y) < attacking_missile.radius * 10:
                self.health -= 100

    def is_dead(self):
        return self.health <= 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_health(self):
        return self.health


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    x2 = random.randint(-400, 400)
    info = Missile(color='red', x=x, y=y, x2=x2, y2=BASE_Y)
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

base = Building(BASE_X, BASE_Y, "base.gif", 2000)
house = Building(BASE_X + 200, BASE_Y, "house_1.gif", 200)
kremlin = Building(BASE_X - 200, BASE_Y, "kremlin_1.gif", 200)
nuclear = Building(BASE_X + 400, BASE_Y, "nuclear_1.gif", 200)
skyscraper = Building(BASE_X - 400, BASE_Y, "skyscraper_1.gif", 200)


while True:
    window.update()
    if base.is_dead():
        continue
    # check_impact()
    base.missiles_attack(attacking_missiles=enemy_missiles)

    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
