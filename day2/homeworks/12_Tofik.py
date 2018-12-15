# -*- coding: utf-8 -*-

import os
import random
import turtle
import time

#   The game will restart after RESTART_TIME seconds after the end of the game.
#       real hit damage = HIT_DAMAGE * 4
#       not a bug but a feature
ENEMY_COUNT, OUR_COUNT = 5, 10
RADIUS_SIZE = 10
HIT_DAMAGE = 25
RESTART_TIME = 3
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_X, BASE_Y, BASE_HEALTH = 0, -300, 1000
KREMLIN_X, KREMLIN_Y, KREMLIN_HEALTH = -200, -300, 500
HOUSE_X, HOUSE_Y, HOUSE_HEALTH = -400, -300, 500
NUCLEAR_X, NUCLEAR_Y, NUCLEAR_HEALTH = 200, -300, 500
SKYSCRAPER_X, SKYSCRAPER_Y, SKYSCRAPER_HEALTH = 400, -300, 500


class Building:
    def __init__(self, x, y, shape_1, health):
        window.register_shape(shape_1)
        pen = turtle.Turtle(visible=False, shape=shape_1)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        pen.showturtle()

        health_bar = turtle.Turtle(shape="square", visible=False)
        health_bar.speed(0)
        health_bar.penup()
        health_bar.setpos(x=x, y=y - 60)
        health_bar.color("red")
        health_bar.shapesize(0.5, 2)
        health_bar.showturtle()

        self.health_bar = health_bar
        self.pen = pen
        self.current_health = health
        self.max_health = health
        self.shape_1 = shape_1


    #   this function to reset game
    def heal(self):
        self.current_health = self.max_health
        self.pen.shape(self.shape_1)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


class Base(Building):
    def __init__(self, x, y, shape_1, shape_2, health):
        Building.__init__(self, x, y, shape_1, health)
        window.register_shape(shape_2)
        self.shape_2 = shape_2

    def hit(self):
        self.current_health -= HIT_DAMAGE
        #print(self.current_health)
        if self.current_health <= 0:
            self.pen.shape(self.shape_2)
            self.health_bar.hideturtle()
            standing_buildings.remove(self)
        elif 2 * self.current_health / self.max_health > 0.1:
            self.health_bar.shapesize(0.5, 2 * self.current_health / self.max_health)


class OurBuilding(Building):
    def __init__(self, x, y, shape_1, shape_2, shape_3, health):
        Building.__init__(self, x, y, shape_1, health)
        window.register_shape(shape_2)
        window.register_shape(shape_3)
        self.shape_2 = shape_2
        self.shape_3 = shape_3

    def hit(self):
        self.current_health -= HIT_DAMAGE

        if self.current_health < 0:
            self.pen.shape(self.shape_3)
            self.health_bar.hideturtle()
            standing_buildings.remove(self)
        else:
            if self.current_health < self.max_health // 2:
                self.pen.shape(self.shape_2)
            if 2 * self.current_health / self.max_health > 0.1:
                self.health_bar.shapesize(0.5, 2 * self.current_health / self.max_health)


class Missile:
    def __init__(self, x, y, color, x2, y2):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        if color == "white":
            window.register_shape(os.path.join(BASE_PATH, "images", "missile.gif"))
            pen.shape(os.path.join(BASE_PATH, "images", "missile.gif"))
            pen.resizemode()
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
            if self.pen.color() == "white":
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

    def clear(self):
        self.pen.clear()
        self.pen.hideturtle()

    def distance(self, obj):
        return self.pen.distance(obj.pen)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


def fire_missile(x, y):
    global our_missile_count
    if our_missile_count < OUR_COUNT:
        info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
        our_missiles.append(info)
        our_missile_count += 1


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    x_to = [build.x for build in standing_buildings]
    info = Missile(color='red', x=x, y=y, x2=random.choice(x_to), y2=BASE_Y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    global our_missile_count
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        if dead.color == "white":
            our_missile_count -= 1
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_interceptions():
    global score
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile) < our_missile.radius * RADIUS_SIZE:
                enemy_missile.state = 'dead'
                score += 50


def check_impact():
    for enemy_missile in enemy_missiles:
        for building in standing_buildings:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.distance(building) < enemy_missile.radius * RADIUS_SIZE:
                building.hit()


def show_result():
    result = turtle.Turtle(visible=False)
    result.write("Result " + str(score), font=("Arial", 15, "normal"))
    time.sleep(RESTART_TIME)
    result.clear()
    result.hideturtle()


window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)
house = OurBuilding(x=HOUSE_X, y=HOUSE_Y, shape_1=os.path.join(BASE_PATH, "images", "house_1.gif"),
                    shape_2=os.path.join(BASE_PATH, "images", "house_3.gif"),
                    shape_3=os.path.join(BASE_PATH, "images", "house_3.gif"), health=HOUSE_HEALTH)
kremlin = OurBuilding(x=KREMLIN_X, y=KREMLIN_Y, shape_1=os.path.join(BASE_PATH, "images", "kremlin_1.gif"),
                      shape_2=os.path.join(BASE_PATH, "images", "kremlin_2.gif"),
                      shape_3=os.path.join(BASE_PATH, "images", "kremlin_3.gif"), health=KREMLIN_HEALTH)
nuclear = OurBuilding(x=NUCLEAR_X, y=NUCLEAR_Y, shape_1=os.path.join(BASE_PATH, "images", "nuclear_1.gif"),
                      shape_2=os.path.join(BASE_PATH, "images", "nuclear_2.gif"),
                      shape_3=os.path.join(BASE_PATH, "images", "nuclear_3.gif"), health=KREMLIN_HEALTH)
skyscraper = OurBuilding(x=SKYSCRAPER_X, y=SKYSCRAPER_Y, shape_1=os.path.join(BASE_PATH, "images", "skyscraper_1.gif"),
                         shape_2=os.path.join(BASE_PATH, "images", "skyscraper_2.gif"),
                         shape_3=os.path.join(BASE_PATH, "images", "skyscraper_3.gif"), health=KREMLIN_HEALTH)
base = Base(x=BASE_X, y=BASE_Y, shape_1=os.path.join(BASE_PATH, "images", "base_opened.gif"),
            shape_2=os.path.join(BASE_PATH, "images", "base.gif"), health=BASE_HEALTH)
score = 0
while True:
    window.onclick(fire_missile)

    our_missile_count = 0
    our_missiles = []
    enemy_missiles = []
    standing_buildings = [house, kremlin, base, nuclear, skyscraper]
    for building in standing_buildings:
        building.heal()

    while base.current_health > 0:
        window.update()
        check_impact()
        check_enemy_count()
        check_interceptions()
        move_missiles(missiles=our_missiles)
        move_missiles(missiles=enemy_missiles)

    for missile in our_missiles:
        missile.clear()
    for missile in enemy_missiles:
        missile.clear()
    show_result()