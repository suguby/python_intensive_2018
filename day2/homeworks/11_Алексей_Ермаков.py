# -*- coding: utf-8 -*-

import math
import os
import random
import turtle


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.title('Game - The protection of the planet')
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5
total_bases_health = 3000

base_position_x = [-500, -300, 0, 300, 500]
base_position_y = -300
shot_position_x, shot_position_y = 0, -300


class Building:

    def __init__(self, base_position_x, base_position_y, base_number, base_health):
        self.base_number = base_number
        self.base_health = base_health
        total_base_images = {
            'base_1_100hp': 'nuclear_1.gif', 'base_1_50hp': 'nuclear_2.gif', 'base_1_0hp': 'nuclear_3.gif',
            'base_2_100hp': 'skyscraper_1.gif', 'base_2_50hp': 'skyscraper_2.gif', 'base_2_0hp': 'skyscraper_3.gif',
            'base_3_100hp': 'base.gif', 'base_3_2hp': 'base_opened.gif',
            'base_4_100hp': 'kremlin_1.gif', 'base_4_50hp': 'kremlin_2.gif', 'base_4_0hp': 'kremlin_3.gif',
            'base_5_100hp': 'house_1.gif', 'base_5_50hp': 'house_2.gif', 'base_5_0hp': 'house_3.gif',
        }

        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setpos(x=base_position_x, y=base_position_y)
        pic_path = os.path.join(BASE_PATH, "images", total_base_images['base_{}_100hp'.format(base_number)])
        window.register_shape(pic_path)
        base.shape(pic_path)
        base.showturtle()




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
            self.pen.forward(2)
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
    info = Missile(color='white', x=shot_position_x, y=shot_position_y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    base_position_attack = base_position_x
    info = Missile(color='red', x=x, y=y, x2=random.choice(base_position_attack), y2=base_position_y)
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


def base_build():
    for i in range(1, 6):
        base_number = i
        base_position_x = {1: -500, 2: -300, 3: 0, 4: 300, 5: 500}
        base_position_y = -300
        base_health = 2000

        base = Building(
            base_position_x=base_position_x[i], base_position_y=base_position_y,
            base_number=base_number, base_health=base_health)


def game_over():
    return total_bases_health < 0


def check_impact():
    global total_bases_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if (enemy_missile.distance(base_position_x[0], shot_position_y) < enemy_missile.radius * 5) or (
                enemy_missile.distance(base_position_x[1], shot_position_y) < enemy_missile.radius * 5) or (
                enemy_missile.distance(base_position_x[2], shot_position_y) < enemy_missile.radius * 5) or (
                enemy_missile.distance(base_position_x[3], shot_position_y) < enemy_missile.radius * 5) or (
                enemy_missile.distance(base_position_x[4], shot_position_y) < enemy_missile.radius * 5):
            total_bases_health -= 100
            print('total_base_health', total_bases_health)


base_build()

while True:
    window.update()

    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
