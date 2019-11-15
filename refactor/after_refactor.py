#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
По умолчанию при старте программы опорные точки отсутствуют и программа находится в состоянии паузы
(движение кривой выключено). Для добавления точек сделайте несколько кликов левой кнопкой мыши. Отрисовка
кривой произойдет, когда точек на экране станет больше двух. Кнопка P запустит движение кривой.
Задача:
1. Изучить документацию к библиотеке pygame и код программы. Понять механизм работы программы (как
происходит отрисовка кривой, перерасчет точек сглаживания и другие нюансы реализации программы)
2. Произвести рефакторинг кода, переписать программу в ООП стиле с использованием классов и наследования.
* Реализовать класс 2-мерных векторов Vec2d. В классе следует определить методы __add__, __sub__,
__mul__(произведение на число). А также добавить возможность вычислять длину вектора с использованием
len(a), и метод int_pair, который возвращает кортеж из двух целых чисел
* Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки,
с её скоростью, пересчет координат точек (set_points) и отрисовку ломаной draw_points.
* Реализовать класс Knot(населдник класса Polyline), в котором добавление и пересчёт координат инициируют
вызов функции get_knot для расчета точек кривой по добавляемым опорным точкам.
* Все классы должны быть самостоятельными и не использовать внешних функций.
* Реализовать дополнительный функционал. К дополнительным задачам относятся: реализовать возможность
удаления опорной точки из кривой, реализовать возможность отрисовки на экране нескольких кривых,
реализовать возможность ускорения/замедления скорости движения кривой.
"""

import math
import random

import pygame


class Vec2d:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __add__(self, other: 'Vec2d') -> 'Vec2d':
        result = Vec2d(self.__x + other.x, self.__y + other.y)
        return result

    def __sub__(self, other: 'Vec2d') -> 'Vec2d':
        result = Vec2d(self.__x - other.x, self.__y - other.y)
        return result

    def __mul__(self, other: int) -> 'Vec2d':
        result = Vec2d(self.__x * other, self.__y * other)
        return result

    def __len__(self) -> float:
        return math.sqrt(self.__x * self.__x + self.__y * self.__y)

    @property
    def int_pair(self) -> tuple:
        return self.__x, self.__y

    @int_pair.setter
    def int_pair(self, point: tuple):
        self.__x, self.__y = point

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __repr__(self):
        return f"<Vec2d: x->{self.__x}, y->{self.__y}>"


class Polyline:
    def __init__(self, points: list = None, speeds: list = None):
        self.points = points or []
        self.speeds = speeds or []
        self.max_speed = 9.0
        self.min_speed = 0.05

    def set_points(self, screen_dim: Vec2d) -> None:
        for point in range(len(self.points)):
            self.points[point] = self.points[point] + self.speeds[point]
            if self.points[point].x > screen_dim.x or self.points[point].x < 0:
                self.speeds[point].int_pair = (-self.speeds[point].x, self.speeds[point].y)
            if self.points[point].y > screen_dim.y or self.points[point].y < 0:
                self.speeds[point].int_pair = (self.speeds[point].x, -self.speeds[point].y)

    def delete_point(self):
        if self.points:
            return self.points.pop(random.randint(0, len(self.points)-1))
        else:
            return

    def increase_speeds(self):
        for idx in range(len(self.speeds)):
            self.speeds[idx] = self.speeds[idx] * 1.25
            if self.speeds[idx].x > self.max_speed:
                self.speeds[idx].int_pair = self.max_speed, self.speeds[idx].y
            if self.speeds[idx].y > self.max_speed:
                self.speeds[idx].int_pair = self.speeds[idx].x, self.max_speed

    def decrease_speeds(self):  # TODO ABS
        for idx in range(len(self.speeds)):
            print("before: " + repr(self.speeds[idx]))
            self.speeds[idx] = self.speeds[idx] * 0.825
            if self.speeds[idx].x < self.min_speed:
                self.speeds[idx].int_pair = self.min_speed, self.speeds[idx].y
            if self.speeds[idx].y < self.min_speed:
                self.speeds[idx].int_pair = self.speeds[idx].x, self.min_speed
            print("after: " + repr(self.speeds[idx]))


    @staticmethod
    def draw_points(points, game_display, style="points", width=3, color=(255, 255, 255)) -> None:
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(game_display, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(game_display, color,
                                   (int(p.x), int(p.y)), width)


class Knot(Polyline):
    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + Knot.get_point(points, alpha, deg - 1) * (1 - alpha)

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * 0.5,
                   self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * 0.5]

            res.extend(Knot.get_points(ptn, count))
        return res

    def reset(self):
        self.points = []
        self.speeds = []


class Helper:
    def __init__(self, game_display, font1, font2):
        self.__data = []
        self.__color_help = (255, 50, 50, 255)
        self.__pointlist_help = [(0, 0), (800, 0), (800, 600), (0, 600)]
        self.__width_help = 5
        self.__color_font = (128, 128, 255)
        self.__game_display = game_display

        self.__font1 = font1

        self.__font2 = font2

    def draw_help(self, steps):
        self.__game_display.fill((50, 50, 50))
        self.__data.append(["F1", "Show Help"])
        self.__data.append(["R", "Restart"])
        self.__data.append(["P", "Pause/Play"])
        self.__data.append(["Num+", "More points"])
        self.__data.append(["Num-", "Less points"])
        self.__data.append(["", ""])
        self.__data.append([str(steps), "Current points"])

        pygame.draw.lines(self.__game_display,
                          (255, 50, 50, 255),
                          True,
                          [(0, 0), (800, 0), (800, 600), (0, 600)],
                          5)
        for i, text in enumerate(self.__data):
            self.__game_display.blit(self.__font1.render(text[0],

                                                         True,
                                                         (128, 128, 255)),
                                     (100, 100 + 30 * i))
            self.__game_display.blit(self.__font2.render(text[1],
                                                         True,
                                                         (128, 128, 255)),
                                     (200, 100 + 30 * i))
        self.__data.clear()


class ScreenSaver:
    def __init__(self, screen_dim, steps):
        self.__knot = Knot()
        self.__screen_dim = Vec2d(screen_dim[0], screen_dim[1])
        self.__steps = steps
        self.__show_help = False
        self.__pause = True
        self.__hue = 0
        self.__game_display = None
        self.__working = False

    def _init_pygame(self):
        pygame.init()
        self.__game_display = pygame.display.set_mode(self.__screen_dim.int_pair)
        pygame.display.set_caption('MyScreenSaver')
        self.__working = True
        self.__color = pygame.Color(0)

        self.__font1 = pygame.font.SysFont("courier", 24)

        self.__font2 = pygame.font.SysFont("serif", 24)
        self.__helper = Helper(self.__game_display, self.__font1, self.__font2)

    def _event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__working = False
                if event.key == pygame.K_r:
                    self.__knot.reset()
                if event.key == pygame.K_p:
                    self.__pause = not self.__pause
                if event.key == pygame.K_KP_PLUS:
                    self.__steps += 1
                if event.key == pygame.K_F1:
                    self.__show_help = not self.__show_help
                if event.key == pygame.K_KP_MINUS:
                    self.__steps -= 1 if self.__steps > 1 else 0
                if event.key == pygame.K_DELETE:
                    self.__knot.delete_point()
                if event.key == pygame.K_i:
                    self.__knot.increase_speeds()
                if event.key == pygame.K_d:
                    self.__knot.decrease_speeds()


            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__knot.points.append(Vec2d(event.pos[0], event.pos[1]))
                self.__knot.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def _change_color(self):
        self.__hue = (self.__hue + 1) % 360
        self.__color.hsla = (self.__hue, 100, 50, 100)

    def _draw(self):
        Knot.draw_points(self.__knot.points,
                         self.__game_display)
        Knot.draw_points(self.__knot.get_knot(self.__steps),
                         self.__game_display,
                         "line",
                         3,
                         self.__color)

    def _close_pygame(self):
        pygame.display.quit()
        pygame.quit()
        exit(0)

    def run(self):
        self._init_pygame()
        while self.__working:
            self._event_loop()

            self.__game_display.fill((0, 0, 0))

            self._change_color()

            self._draw()

            if not self.__pause:
                self.__knot.set_points(self.__screen_dim)
            if self.__show_help:
                self.__helper.draw_help(self.__steps)

            pygame.display.flip()

        self._close_pygame()


if __name__ == '__main__':
    g = ScreenSaver((800, 600), 35)
    g.run()
    k = Knot()
    k.points = [Vec2d(500, 600), Vec2d(400, 463), Vec2d(300, 323)]
    print(k.points[0] + k.points[1])
    print(k.points)
