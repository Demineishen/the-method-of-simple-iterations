import copy
import tkinter as tk

from functions import Polynom, ModuleFunction
from iteration_method import phi as phi_func, solution

# Data
y_function_values = []
function_draw = []
solution_x = None
function = Polynom()
y_phi = []
phi = []
step_lines = []
step_dots = []
WIN_H = 900
WIN_W = 1200
PANEL_H = WIN_H
PANEL_W = 200
CANVAS_H = WIN_H
CANVAS_W = WIN_W - PANEL_W

win = tk.Tk()
win.title('Метод простых итераций')
win.config(width=WIN_W, height=WIN_H)
win.resizable(False, False)

panel = tk.Frame(win, width=PANEL_H, height=PANEL_H, bd=4, relief=tk.GROOVE)
panel.place(x=0, y=0, width=PANEL_H, height=PANEL_H)
panel.config(width=WIN_W, height=WIN_H)

canvas = tk.Canvas(win, width=CANVAS_W, height=CANVAS_H, bg='#012')
canvas.place(x=PANEL_W, y=0, width=CANVAS_W, height=CANVAS_W)


def draw_axis(x_left, x_right, y_bottom, y_top):
    dx = CANVAS_W / (x_right - x_left)
    dy = CANVAS_H / (y_top - y_bottom)

    cx = - x_left * dx
    cy = y_top * dy

    canvas.create_line(0, cy, CANVAS_W, cy, fill='white')
    canvas.create_line(cx, 0, cx, CANVAS_H, fill='white')

    x_step = (x_right - x_left) / 20
    x = x_left
    while x <= x_right:
        x_canvas = (x - x_left) * dx
        canvas.create_line(x_canvas, cy - 3, x_canvas, cy + 3, fill='white')
        canvas.create_text(x_canvas, cy + 15, text=str(round(x, 2)), font="Verdana 9", fill='white')

        x += x_step

    y_step = (y_top - y_bottom) / 20
    y = y_top
    while y >= y_bottom:
        y_canvas = (y - y_top) * dy
        canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas, fill='white')
        canvas.create_text(cx + 25, -y_canvas, text=str(round(y, 2)), font="Verdana 9", fill='white')

        y -= y_step

    return dx, dy


def frange(begin, end, step):
    x = begin
    t = []
    while x <= end:
        t.append(x)
        x += step
    return t


def function_generator(x_tmp, f: Polynom or ModuleFunction):
    y_tmp = []
    for x in x_tmp:
        y = f.get_value(x)
        y_tmp.append(y)
    return y_tmp


def graph_dot(x_tmp, y_tmp, color):
    dot_list = []
    i = 0
    for x in x_tmp:
        y = y_tmp[i]
        x = (x - x_tmp[0]) * dx
        y = (y - y_top) * dy
        dot = canvas.create_oval(x - 1, -(y - 1), x + 1, -(y + 1), fill=color, outline=color)
        dot_list.append(dot)
        i += 1
    return dot_list


def draw_dot(rel_x, rel_y, color, r=4):
    x = CANVAS_W / 2 + dx * rel_x
    y = WIN_H / 2 - dy * rel_y
    return canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color), (x, y)


def clear_solution():
    if solution_x is not None:
        canvas.delete(solution_x)
        for line in step_lines:
            canvas.delete(line)
        for dot in step_dots:
            canvas.delete(dot)


def clear_functions():
    for dot in function_draw:
        canvas.delete(dot)
    for dot in phi:
        canvas.delete(dot)


def parabola_redraw():
    global y_function_values
    global function_draw
    global solution_x
    global function
    clear_functions()
    clear_solution()
    try:
        a = float(a_button.get())
        b = float(b_button.get())
        c = float(c_button.get())
        result_field_value.set("")
    except ValueError:
        result_field_value.set("Значение коэффициента\nуказано неверно")
        return
    function = Polynom(a, b, c)
    y_function_values = function_generator(x_list, function)
    function_draw = graph_dot(x_list, y_function_values, 'yellow')
    draw_phi('dark blue')


def module_redraw():
    global y_function_values
    global function_draw
    global solution_x
    global function
    clear_functions()
    clear_solution()
    try:
        a = float(a_module_button.get())
        b = float(b_module_button.get())
        result_field_value.set("")
    except ValueError:
        result_field_value.set("Значение коэффициента\nуказано неверно")
        return
    function = ModuleFunction(a, b)
    y_function_values = function_generator(x_list, function)
    function_draw = graph_dot(x_list, y_function_values, 'yellow')
    draw_phi('dark blue')


def draw_phi(color):
    global y_phi
    global phi
    y_phi = []
    for x in x_list:
        y = phi_func(function, x)
        y_phi.append(y)
    phi = graph_dot(x_list, y_phi, color)


def draw_solution():
    global solution_x
    global function
    clear_solution()
    try:
        x_value, steps, iters = solution(function, float(x_button.get()), float(eps_button.get()))
    except ValueError:
        result_field_value.set("Значение коэффициента\nуказано неверно")
        return
    if x_value is not None:
        result_field_value.set("x = " + str(round(x_value, 10)) + "\nза " + str(iters) + " итераций.")
        x, y = None, None
        for i, step in enumerate(steps[0]):
            prev_x, prev_y = x, y
            dot, (x, y) = draw_dot(step, steps[1][i], 'red', 2)
            step_dots.append(copy.copy(dot))
            if prev_x is not None:
                step_lines.append(canvas.create_line(prev_x, prev_y, x, y, fill='pink'))
        solution_x, _ = draw_dot(x_value, 0, 'red', 4)
    else:
        result_field_value.set("Решение не найдено\n за " + str(iters) + " итераций.")


x_left, x_right = -10, 10
y_bottom, y_top = -10, 10
dx, dy = draw_axis(x_left, x_right, y_bottom, y_top)

x_list = frange(x_left, x_right, 0.01)

# Labels
v1 = tk.Label(panel, text="Квадратное\nуравнение")
v1.grid(row=1, column=1)
v2 = tk.Label(panel, text="Уравнение\n|ax + b|")
v2.grid(row=6, column=1)
v3 = tk.Label(panel, text="Параметры")
v3.grid(row=10, column=1)
a_label = tk.Label(panel, text="a")
a_label.grid(row=2, column=1)
b_label = tk.Label(panel, text="b")
b_label.grid(row=3, column=1)
c_label = tk.Label(panel, text="c")
c_label.grid(row=4, column=1)
a_module_label = tk.Label(panel, text="a")
a_module_label.grid(row=7, column=1)
b_module_label = tk.Label(panel, text="b")
b_module_label.grid(row=8, column=1)
eps_label = tk.Label(panel, text="ε")
eps_label.grid(row=11, column=1)
x_label = tk.Label(panel, text="x")
x_label.grid(row=12, column=1)
function_label = tk.Label(panel, text="Функция")
function_label.place(x=135, y=790, width=55, height=30)
phi_label = tk.Label(panel, text="Phi")
phi_label.place(x=170, y=820, width=17, height=30)
solution_label = tk.Label(panel, text="Решение")
solution_label.place(x=135, y=850, width=55, height=30)
result_label = tk.Label(panel, text="Результат:")
result_label.place(x=10, y=430, width=70, height=30)
result_field_value = tk.StringVar()
result_field = tk.Label(panel, textvariable=result_field_value)
result_field.place(x=10, y=460, width=170, height=30)
canvas.create_oval(10, 867, 18, 875, fill='red', outline='red')
canvas.create_line(10, 840, 35, 840, fill='dark blue', width=3)
canvas.create_line(10, 810, 35, 810, fill='yellow', width=3)

# Buttons
a_button = tk.Entry(panel, bd=2)
a_button.grid(row=2, column=2)
a_button.insert(0, "1")

b_button = tk.Entry(panel, bd=2)
b_button.grid(row=3, column=2)
b_button.insert(0, "0")

c_button = tk.Entry(panel, bd=2)
c_button.grid(row=4, column=2)
c_button.insert(0, "0")

a_module_button = tk.Entry(panel, bd=2)
a_module_button.grid(row=7, column=2)
a_module_button.insert(0, "1")

b_module_button = tk.Entry(panel, bd=2)
b_module_button.grid(row=8, column=2)
b_module_button.insert(0, "0")

eps_button = tk.Entry(panel, bd=2)
eps_button.grid(row=11, column=2)
eps_button.insert(0, "0.000001")

x_button = tk.Entry(panel, bd=2)
x_button.grid(row=12, column=2)
x_button.insert(0, "0")

show_button = tk.Button(panel, text="Показать", command=parabola_redraw)
show_button.grid(row=5, column=2, sticky="W")

show_module_button = tk.Button(panel, text="Показать", command=module_redraw)
show_module_button.grid(row=9, column=2, sticky="W")

show_button = tk.Button(panel, text="Решение", command=draw_solution)
show_button.grid(row=13, column=2, sticky="W")

parabola_redraw()
win.mainloop()
