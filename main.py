import pygame
import graphics
import numpy as np


pygame.init()

surf = pygame.Surface((1200, 800))

finished = False
while not finished:
    menu = graphics.Menu(surf)
    anim = graphics.Animation(surf)
    data = menu.run()
    if menu.start:
        data[1] += 1.57
        data[0] *= 400 / max(data[0])
        ls0 = np.array(data[0])
        angles0 = np.array(data[1])
        n = data[2]
        sequence = [0]
        for i in range(n):
            sequence += [i + 1, - i - 1]

        dt0 = np.array(sequence) / 500
        ls1 = []
        angles1 = []
        for i in range(2 * n + 1):
            ls1.append(ls0[sequence[i] + n])
            angles1.append(angles0[sequence[i] + n])
    
        anim.run(angles1[1:], dt0[1:], ls1[1:])
        finished = anim.finished
    else:
        finished = True

pygame.quit()

