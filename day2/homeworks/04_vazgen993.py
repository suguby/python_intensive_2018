# -*- coding: utf-8 -*-

# После того, как здоровье здания становится < 0, последнее исчезает. Игра заканчивается, когда исчезнут все здания.

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
X_CORDS = (BASE_X, BASE_X - 400, BASE_X - 200, BASE_X + 200, BASE_X + 400)


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

    def __init__(self, x, y, health, picture):

        self.health = health

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x, y=y)
        pic_path = os.path.join(BASE_PATH, "images", picture)
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen

    def clear_building(self):
        self.pen.clear()
        self.pen.hideturtle()

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
    info = Missile(color='red', x=x, y=y, x2=random.choice(X_CORDS), y2=BASE_Y)
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

base = Building(x=BASE_X, y=BASE_Y, picture='base.gif', health=2000)
house = Building(x=X_CORDS[1], y=BASE_Y, picture='house_1.gif', health=1000)
kremlin = Building(x=X_CORDS[2], y=BASE_Y, picture='kremlin_1.gif', health=1000)
nuclear = Building(x=X_CORDS[3], y=BASE_Y, picture='nuclear_1.gif', health=1000)
skyscraper = Building(x=X_CORDS[4], y=BASE_Y, picture='skyscraper_1.gif', health=1000)

current_buildings_list = [base, house, kremlin, nuclear, skyscraper]

def check_buildings_health(buildings):
    for building in buildings:
        if building.health < 0:
            building.clear_building()
            buildings.remove(building)

def game_over():
    return len(current_buildings_list) == 0

def check_impact():
    for building in current_buildings_list:
        for enemy_missile in enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.distance(building.x, building.y) < enemy_missile.radius * 10:
                building.health -= 100
                # print('base_health', base_health)


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    check_buildings_health(buildings=current_buildings_list)
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
