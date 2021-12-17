import numpy as np
import cmath
import parser


def data(filename, reverse=False):
    x, y = parser.parse_file("functions/" + filename)
    if reverse:
        points = [j + i * 1j for j, i in zip(x, y)]
    else:
        points = [j - i * 1j for j, i in zip(x, y)]

    f_s = []
    vectors = 200
    n = len(points)
    dt = 1 / n
    for j in range(-vectors, vectors + 1):
        f = 0
        for i in range(n):
            f += (points[i] * cmath.exp(-2 * cmath.pi * i * dt * j * 1j) * dt)
        f_s.append(f)

    angles = np.angle(f_s)
    norms = np.absolute(f_s)
    return norms, angles, vectors
