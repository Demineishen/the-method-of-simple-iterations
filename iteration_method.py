import math
import copy

from functions import Polynom, ModuleFunction


def stop_iteration_criteria(x_old, x_new, dif):
    return abs(x_old - x_new) < dif


def phi(f: Polynom or ModuleFunction, x):
    return x - 0.1 * f.get_value(x)


def solution(f: Polynom or ModuleFunction, x, dif=0.000001):
    steps_x = []
    steps_y = []
    i = 1
    while True:
        x_prev = copy.copy(x)
        x = phi(f, x_prev)
        steps_x.append(x_prev)
        steps_y.append(copy.copy(x))
        try:
            if stop_iteration_criteria(x_prev, x, dif):
                print('Количество итераций на решение: ', i)
                print('x =', x)
                return x, (steps_x, steps_y), i
        except OverflowError:
            return None, (steps_x, steps_y), i
        i += 1
