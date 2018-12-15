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


class Building:
    def __init__(self, name, health, x, y, pics_path):
        self.x = x
        self.y = y
        self.pics_path = pics_path
        self.number = 0
        self.start_health = health
        self.health = health
        self.name = name

        pen = turtle.Turtle()
        self.pen = pen
        self.draw()

    def check_health(self):
        return self.health <= 0

    def take_damage(self, damage):
        self.health -= damage
        number = self.pics_path.__len__() - math.floor(
            self.health * self.pics_path.__len__() / (self.start_health + 1)) - 1
        if number != self.number:
            self.draw()
            self.number = number

        if self.health <= 0:
            self.remove()
            game.buildings_manager.remove(self)
        print(self.name, 'health', self.health)

    def check_impact(self, missile):
        return missile.distance(self.x, self.y) < missile.radius * 10

    def remove(self):
        self.pen.clear()
        self.pen.hideturtle()

    def draw(self):

        self.pen.clear()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.setpos(x=self.x, y=self.y)
        window.register_shape(self.pics_path[self.number])
        self.pen.shape(self.pics_path[self.number])
        self.pen.showturtle()


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


class BuildingsManager:
    def __init__(self):
        buildings = []

        base = Building("база", 2000, BASE_X, BASE_Y, [os.path.join(BASE_PATH, "images", "base.gif")])
        buildings.append(base)

        buildings.append(Building("реактор", 1500, BASE_X - 200, BASE_Y, [
            os.path.join(BASE_PATH, "images", "nuclear_1.gif"),
            os.path.join(BASE_PATH, "images", "nuclear_2.gif"),
            os.path.join(BASE_PATH, "images", "nuclear_3.gif"),
        ]))

        buildings.append(Building("реактор", 1000, BASE_X - 400, BASE_Y, [
            os.path.join(BASE_PATH, "images", "skyscraper_1.gif"),
            os.path.join(BASE_PATH, "images", "skyscraper_2.gif"),
            os.path.join(BASE_PATH, "images", "skyscraper_3.gif"),
        ]))

        buildings.append(Building("реактор", 500, BASE_X + 200, BASE_Y, [
            os.path.join(BASE_PATH, "images", "house_1.gif"),
            os.path.join(BASE_PATH, "images", "house_2.gif"),
            os.path.join(BASE_PATH, "images", "house_3.gif"),
        ]))

        buildings.append(Building("реактор", 800, BASE_X + 400, BASE_Y, [
            os.path.join(BASE_PATH, "images", "kremlin_1.gif"),
            os.path.join(BASE_PATH, "images", "kremlin_2.gif"),
            os.path.join(BASE_PATH, "images", "kremlin_3.gif"),
        ]))

        self.buildings = buildings

    def count(self):
        return self.buildings.__len__()

    def get_random(self):
        return self.buildings[random.randint(0, self.count() - 1)]

    def remove(self, building):
        self.buildings.remove(building)

    def check_impact(self, missile):
        for building in self.buildings:
            if building.check_impact(missile):
                building.take_damage(100)


class Game:
    def __init__(self, count_enemy, buildings_manager):
        self.buildings_manager = buildings_manager
        self.count_enemy = count_enemy

        self.our_missiles = []
        self.enemy_missiles = []
        self.count_dead_enemy_missiles = 0

        window.onclick(self.fire_missile)

    def game_over(self):
        return self.buildings_manager.count() == 0

    def check_impact(self):
        for enemy_missile in self.enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            self.buildings_manager.check_impact(enemy_missile)

    def check_enemy_count(self):
        if len(self.enemy_missiles) < self.count_enemy:
            self.fire_enemy_missile()

    def fire_enemy_missile(self):
        if self.buildings_manager.count() == 0:
            return
        target = self.buildings_manager.get_random()
        x = random.randint(-600, 600)
        y = 400
        info = Missile(color='red', x=x, y=y, x2=target.x, y2=target.y)
        self.enemy_missiles.append(info)

    def check_interceptions(self):
        for our_missile in self.our_missiles:
            if our_missile.state != 'explode':
                continue
            for enemy_missile in self.enemy_missiles:
                if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                    enemy_missile.state = 'dead'

    def move_missiles(self, missiles):
        for missile in missiles:
            missile.step()

    def proc_missiles(self, missiles):
        dead_missiles = [missile for missile in missiles if missile.state == 'dead']
        for dead in dead_missiles:
            missiles.remove(dead)
        return dead_missiles.__len__()

    def check(self):
        self.check_impact()
        self.check_enemy_count()
        self.check_interceptions()

    def draw(self):
        self.move_missiles(missiles=self.our_missiles)
        self.move_missiles(missiles=self.enemy_missiles)
        self.updateLevel(self.proc_missiles(missiles=self.enemy_missiles))

    def fire_missile(self, x, y):
        info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
        self.our_missiles.append(info)

    def updateLevel(self, count_dead_enemy_missiles):
        self.count_dead_enemy_missiles += count_dead_enemy_missiles
        if self.count_dead_enemy_missiles > 10:
            self.count_enemy += 1
            self.count_dead_enemy_missiles = 0


buildingsManager = BuildingsManager()
game = Game(count_enemy=ENEMY_COUNT, buildings_manager=buildingsManager)

while True:
    window.update()
    if game.game_over():
        continue
    game.check()
    game.draw()

