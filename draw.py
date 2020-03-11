from display import *
from matrix import *


def add_circle(points, cx, cy, cz, r, step):
    limit = int(1 / step) + 1
    prevX = 0
    prevY = 0
    for i in range(limit):
        t = i * step
        x = (r * math.cos(2 * math.pi * t)) + cx
        y = (r * math.sin(2 * math.pi * t)) + cy
        if i > 0:
            add_edge(points, prevX, prevY, cz, x, y, cz)
        prevX = x
        prevY = y


def cubic(coefs, t):
    exponents = [t, t ** 2, t ** 3]
    return (coefs[0][0] * exponents[2]) + (coefs[0][1] * exponents[1]) + (coefs[0][2] * t) + (coefs[0][3])


def add_curve(points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type):
    if curve_type == "bezier":
        xCoefs = make_coefs(x0, x1, x2, x3, 0)
        yCoefs = make_coefs(y0, y1, y2, y3, 0)
    else:
        xCoefs = make_coefs(x0, x1, x2, x3, 1)
        yCoefs = make_coefs(y0, y1, y2, y3, 1)
    limit = int(1 / step) + 1
    prevX = 0
    prevY = 0
    for i in range(limit):
        t = i * step
        x = cubic(xCoefs, t)
        y = cubic(yCoefs, t)
        if (i > 0):
            add_edge(points, prevX, prevY, 0, x, y, 0)
        prevX = x
        prevY = y


def draw_lines(matrix, screen, color):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line(int(matrix[point][0]),
                  int(matrix[point][1]),
                  int(matrix[point + 1][0]),
                  int(matrix[point + 1][1]),
                  screen, color)
        point += 2


def add_edge(matrix, x0, y0, z0, x1, y1, z1):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)


def add_point(matrix, x, y, z=0):
    matrix.append([x, y, z, 1])


def draw_line(x0, y0, x1, y1, screen, color):
    # swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    # octants 1 and 8
    if (abs(x1 - x0) >= abs(y1 - y0)):

        # octant 1
        if A > 0:
            d = A + B / 2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y += 1
                    d += B
                x += 1
                d += A
            # end octant 1 while
            plot(screen, color, x1, y1)
        # end octant 1

        # octant 8
        else:
            d = A - B / 2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y -= 1
                    d -= B
                x += 1
                d += A
            # end octant 8 while
            plot(screen, color, x1, y1)
        # end octant 8
    # end octants 1 and 8

    # octants 2 and 7
    else:
        # octant 2
        if A > 0:
            d = A / 2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x += 1
                    d += A
                y += 1
                d += B
            # end octant 2 while
            plot(screen, color, x1, y1)
        # end octant 2

        # octant 7
        else:
            d = A / 2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x += 1
                    d += A
                y -= 1
                d -= B
            # end octant 7 while
            plot(screen, color, x1, y1)
        # end octant 7
    # end octants 2 and 7
# end draw_line
