# -*- coding: utf-8 -*-

import random
import turtle


window = turtle.Screen()
window.bgcolor('blue')
window.setup(1200 + 5, 800 + 5)
window.screensize(1200, 800)
# window.tracer(n=2)


pen = turtle.Turtle()
pen.color('yellow')
pen.width(2)
pen.speed(0)
pen.shape('turtle')
# pen.hideturtle()


def flake(x, y, length):
    angles = [0, 60, 120, 180, 240, 300]
    colors = ['red', 'green', 'white', 'cyan']
    for angle in angles:
        pen.penup()
        pen.setpos(x, y)
        pen.pendown()
        pen.setheading(angle)
        if angle > 90:
            random_color = random.choice(colors)
            pen.color(random_color)
        pen.forward(length)
        pen.backward(length // 2)
        pen.setheading(angle + 50)
        pen.forward(length // 2)
        pen.backward(length // 2)
        pen.setheading(angle - 50)
        pen.forward(length // 2)


for x in range(-400, 400, 100):
    flake(x, y=0, length=40)


window.mainloop()