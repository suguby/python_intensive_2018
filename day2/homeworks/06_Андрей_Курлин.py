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
HOUSE_X, HOUSE_Y = -400,-300
KREMLIN_X, KREMLIN_Y = -200,-300
NUCLEAR_X, NUCLEAR_Y = 200,-300
SKYSCRAPER_X, SKYSCRAPER_Y = 400,-300


class Missile:  # класс для ракет

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



class Building:  # класс для зданий
    def __init__(self, x, y, name, health):
        self.name = name
        self.base_health = health
        self.x = x
        self.y = y

        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setpos(x=x, y=y)
        pic_path = os.path.join(BASE_PATH, "images", self.name)
        window.register_shape(pic_path)
        base.shape(pic_path)
        base.showturtle()

        self.base = base
        checker = turtle.Turtle(visible=False)
        checker.penup()
        checker.setpos(x=self.x, y=self.y - 65)
        checker.penup()
        checker.write(self.health)
        self.checker = checker


    @property  # getter хп здания
    def health(self):
        return self.base_health

    @health.setter  # setter хп здания
    def health(self,value):
        self.base_health = value
        self.checker.setpos(x=self.x, y=self.y-65)
        self.checker.write(self.health)

    def change_shape(self):
        if self.name[-5] == '1':
            self.name = self.name[:-5]+'2.gif'
            pic_path = os.path.join(BASE_PATH, "images", self.name)
            window.register_shape(pic_path)
            self.base.shape(pic_path)
        elif self.name[-5] == '2':
            self.name = self.name[:-5]+'3.gif'
            pic_path = os.path.join(BASE_PATH, "images", self.name)
            window.register_shape(pic_path)
            self.base.shape(pic_path)






def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    cords = random.choice(
        [[BASE_X, BASE_Y], [HOUSE_X, HOUSE_Y], [KREMLIN_X, KREMLIN_Y], [NUCLEAR_X, NUCLEAR_Y], [SKYSCRAPER_X,
                                                                                                SKYSCRAPER_Y]])
    info = Missile(color='red', x=x, y=y, x2=cords[0], y2=cords[1])
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


MAIN_BASE = Building(x=BASE_X, y=BASE_Y, name="base.gif", health=2000)  # создание основного здания и других зданий

house = Building(x=HOUSE_X, y=HOUSE_Y,name='house_1.gif', health=1000)
kremlin = Building(x=KREMLIN_X, y=KREMLIN_Y,name='kremlin_1.gif', health=1000)
nuclear = Building(x=NUCLEAR_X, y=NUCLEAR_Y,name='nuclear_1.gif', health=1000)
skyscraper = Building(x=SKYSCRAPER_X, y=SKYSCRAPER_Y,name='skyscraper_1.gif', health=1000)


def game_over():
    return (MAIN_BASE.health <= 0) or (skyscraper.health < 0 and house.health < 0 and kremlin.health < 0 and nuclear.health < 0)


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            MAIN_BASE.checker.clear()
            MAIN_BASE.health -= 25
        elif enemy_missile.distance(HOUSE_X, HOUSE_Y) < enemy_missile.radius * 10:
            house.checker.clear()
            house.health -= 25
            if house.health in [300, 600]:
                house.change_shape()
        elif enemy_missile.distance(KREMLIN_X, KREMLIN_Y) < enemy_missile.radius * 10:
            kremlin.checker.clear()
            kremlin.health -= 25
            if kremlin.health in [300, 600]:
                kremlin.change_shape()
        elif enemy_missile.distance(NUCLEAR_X, NUCLEAR_Y) < enemy_missile.radius * 10:
            nuclear.checker.clear()
            nuclear.health -= 25
            if nuclear.health in [300, 600]:
                nuclear.change_shape()
        elif enemy_missile.distance(SKYSCRAPER_X, SKYSCRAPER_Y) < enemy_missile.radius * 10:
            skyscraper.checker.clear()
            skyscraper.health -= 25
            if skyscraper.health in [300, 600]:
                skyscraper.change_shape()
            #print('base_health', MAIN_BASE.health)


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)