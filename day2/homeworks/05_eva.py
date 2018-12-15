# -*- coding: utf-8 -*-

import math
import os
import random
import turtle

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic("../../images/background.png")
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5
BASE_X, BASE_Y = 0, -300

class Building:

    def __init__(self, x, y, health, pic_name):
        self.x = x
        self.y = y
        self.path = "../../images/" + pic_name
        self.health = health
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.setpos(x=x, y=y)

    def build(self):
        window.register_shape(self.path)
        self.pen.shape(self.path)
        self.pen.showturtle()

    def remove(self):
        self.pen.hideturtle()

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





def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    x2 = random.randint(-600, 600)
    info = Missile(color='red', x=x, y=y, x2=x2, y2=BASE_Y  - 50)
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
health = 2000

base = Building(x=BASE_X, y=BASE_Y, health = health, pic_name="base.gif")
base.build()

house = Building(x=-200, y=BASE_Y, health = health, pic_name="house_1.gif")
house.build()

kremlin = Building(x=200, y=BASE_Y, health = health, pic_name="kremlin_1.gif")
kremlin.build()

nuclear = Building(x=-400, y=BASE_Y, health = health, pic_name="nuclear_1.gif")
nuclear.build()

skyscraper = Building(x=400, y=BASE_Y, health = health, pic_name="skyscraper_1.gif")
skyscraper.build()


def check_building_health(building):
    if game_over(building=building):
        building.remove()

def game_over(building):
    return building.health <= 0

def check_impact(building):
    #global base_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(building.x, building.y) < enemy_missile.radius * 10:
            building.health -= 100

while True:
    window.update()
    if game_over(building = base):
        continue

    if game_over(building=house) and game_over(building=kremlin) and game_over(building=nuclear) and game_over(building=skyscraper):
        continue

    check_building_health(building=house)
    check_building_health(building=kremlin)
    check_building_health(building=nuclear)
    check_building_health(building=skyscraper)


    check_impact(building=base)
    check_impact(building=house)
    check_impact(building=kremlin)
    check_impact(building=nuclear)
    check_impact(building=skyscraper)

    check_enemy_count()
    print(base.health, house.health, skyscraper.health, kremlin.health, nuclear.health)
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)