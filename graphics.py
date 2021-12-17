import pygame
import numpy as np
import os
import fourier

FPS = 60

YELLOW = (255, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FIELD_WIDTH = 200
FIELD_HEIGHT = 50

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 70

col_x = 320

sc = pygame.display.set_mode((1200, 800))

START_POS = (600, 400)


class Window:
    """
    abstract class for all program's windows
    """

    @staticmethod
    def create_text(text, color, position, size, screen, background=BLACK):
        """
            abstract method, create text on screen
            :return: text
        """
        f1 = pygame.font.Font(None, size)
        text1 = f1.render(text, True,
                          color, background)
        screen.blit(text1, position)


class Menu(Window):
    """
    class of first window of program, where init all parameters
    """

    def __init__(self, screen):
        """
        init function
        :param screen: surface
        """
        self.screen = screen

        self.load_from_file_button = Button(200, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Load from file", self.screen, dx=-5)
        self.examples_button = Button(650, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Examples", self.screen, dx=-30)
        self.start_button = Button(970, 700, 200, 70, "Start!", self.screen)
        self.return_button = Button(30, 700, 230, 70, "Return", self.screen, dx=-15)
        self.load_button = Button(col_x + FIELD_WIDTH + 200, 370, 200, FIELD_HEIGHT, "Load", self.screen)

        col1 = 200
        col2 = 700
        self.example1_button = Button(col1, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Rose", self.screen)
        self.example2_button = Button(col1, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Star", self.screen)
        self.example3_button = Button(col1, 450, BUTTON_WIDTH, BUTTON_HEIGHT, "Key", self.screen)
        self.example4_button = Button(col1, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Butterfly", self.screen)
        self.example5_button = Button(col2, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Hello world!", self.screen)
        self.example6_button = Button(col2, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Woman", self.screen, dx=-30)
        self.example7_button = Button(col2, 450, BUTTON_WIDTH, BUTTON_HEIGHT, "Wolf", self.screen)
        self.example8_button = Button(col2, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Bird", self.screen)

        self.buttons = []

        self.text1 = Text("Visual Fourier transform", YELLOW, (280, 30), 80, self.screen)
        self.text2 = Text("Load from .svg file", WHITE, (col_x + 70, 300), 70, self.screen)
        self.text3 = Text("Data has been loaded", GREEN, (450, 720), 50, self.screen)
        self.text4 = Text("Incorrect filename", RED, (470, 720), 50, self.screen)
        self.texts = []

        self.field_filename = InsertField("", col_x, 370, FIELD_WIDTH + 200, FIELD_HEIGHT, self.screen)
        self.insert_fields = []

        self.load = False
        self.output = [[], [], 0]
        self.start = False
        self.finished = False

    def load_from_file_choice(self):
        output = False
        self.texts = [self.text1, self.text2]
        self.insert_fields = [self.field_filename]
        self.buttons = [self.start_button, self.load_button, self.return_button]
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                    finished = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for f in self.insert_fields:
                        if f.check_mouse():
                            f.activate()
                        else:
                            f.deactivate()

                    if self.load_button.check_mouse():
                        if self.load_file(self.field_filename.get_value()):
                            self.load = True
                            if self.text4 in self.texts:
                                self.texts.remove(self.text4)
                            if self.text3 not in self.texts:
                                self.texts.append(self.text3)
                        else:
                            self.load = False
                            if self.text3 in self.texts:
                                self.texts.remove(self.text3)
                            if self.text4 not in self.texts:
                                self.texts.append(self.text4)

                    if self.start_button.check_mouse():
                        if self.load:
                            self.start = True
                            output = True
                            finished = True
                        else:
                            self.texts.append(self.text4)

                    if self.return_button.check_mouse():
                        output = False
                        finished = True

                if event.type == pygame.KEYDOWN:
                    for f in self.insert_fields:
                        if event.key == 13:
                            f.deactivate()
                        if event.key == pygame.K_BACKSPACE:
                            if f.is_active and f.value != "":
                                f.value = f.value[:-2]
                                f.value += "|"
                                f.text.set_text(f.value)
                        else:
                            if len(f.value) < 15:
                                f.insert(event.unicode)

            for b in self.buttons:
                b.check_mouse()

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)
        return output

    def examples_choice(self):
        output = False
        self.texts = [self.text1]
        self.buttons = [self.example1_button, self.example2_button, self.example3_button,
                        self.example4_button, self.example5_button, self.example6_button,
                        self.example7_button, self.example8_button, self.return_button]
        clock = pygame.time.Clock()
        finished = False
        while not finished:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                    finished = True

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.example1_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("rose-output.txt")

                    if self.example2_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("star-output.txt", True)

                    if self.example3_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("key-output.txt")

                    if self.example4_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("butterfly-output.txt")

                    if self.example5_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("image-output.txt", True)

                    if self.example6_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("woman-output.txt")

                    if self.example7_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("wolf-output.txt")

                    if self.example8_button.check_mouse():
                        output = True
                        finished = True
                        self.start = True
                        self.output[0], self.output[1], self.output[2] = fourier.data("pigeon-output.txt")

                    if self.return_button.check_mouse():
                        finished = True

            for b in self.buttons:
                b.check_mouse()

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)

        return output

    def draw_objects(self):
        """Draws all objects in the window"""
        for text in self.texts:
            text.draw()

        for field in self.insert_fields:
            field.draw()

        for button in self.buttons:
            button.draw()

        sc.blit(self.screen, (0, 0))

    def run(self):
        """
        Returns parameters as an np.array([x, y, z, vx, vy, vz, time, step,
         x-axis, y-axis, air_force, sun_force, integrator, is_finished)
         axis: 0 -- x, 1 -- y, 2 -- z, 3 -- vx, 4 -- vy, 5 -- vz, 6 -- time
         forces: bool variables
         integrator: 0 -- Euler, 1 -- RK4, 2 -- Dormand-Prince
         is_finished: True if stop, False if go next
        :return:
        """

        with open("initial.txt") as file:
            initial = file.read().split("\n")

        velos = np.array([float(i) for i in initial[1].split(", ")])
        ls = np.array([float(i) for i in initial[0].split(", ")]) * 7.5
        angles = np.array([float(i) for i in initial[0].split(", ")]) + 100 * velos

        dt = 0.1
        self.texts = [self.text1]
        self.buttons = [self.load_from_file_button, self.examples_button]
        clock = pygame.time.Clock()
        while not self.finished:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.load_from_file_button.check_mouse():
                        if self.load_from_file_choice():
                            self.finished = True
                        else:
                            if self.finished:
                                return
                            self.texts = [self.text1]
                            self.buttons = [self.load_from_file_button, self.examples_button]
                            self.insert_fields = []

                    if self.examples_button.check_mouse():
                        if self.examples_choice():
                            self.finished = True
                        else:
                            if self.finished:
                                return
                            self.texts = [self.text1]
                            self.buttons = [self.load_from_file_button, self.examples_button]
                            self.insert_fields = []

            for b in self.buttons:
                b.check_mouse()

            angles += velos * dt
            pos_s = Animation.data_transform(angles, ls)
            for i in range(len(angles)):
                pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i + 1], 1)
                pygame.draw.circle(self.screen, YELLOW, pos_s[i + 1], 2)

            pygame.draw.circle(self.screen, YELLOW, pos_s[0], 2)
            sc.blit(self.screen, (0, 0))

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)

        return self.output

    def load_file(self, filename):
        if filename[-4:] == ".svg" and os.path.isfile("svg-equations-1.1.0/" + filename):
            os.system("java -jar svg-equations-1.1.0/svgeq-release.jar svg-equations-1.1.0/" + filename)
            os.system("cp svg-equations-1.1.0/" + filename.replace(".svg", "") + "-output.txt" + " functions/")
            self.output[0], self.output[1], self.output[2] = fourier.data(filename.replace(".svg", "") + "-output.txt")
            return True

        else:
            return False


class Text:
    """
    class for working with text fields
    """

    def __init__(self, text, color, position, size, screen, background=BLACK):
        """
        init function
        :param text: text
        :param color: color
        :param position: text position
        :param size: field size
        :param screen: surface
        :param background: background
        """
        self.text = text
        self.base_color = color
        self.current_color = color
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.screen = screen
        self.background = background
        self.is_active = True

    def draw(self):
        """
        draw text on screen
        :return:
        """
        f1 = pygame.font.Font(None, self.size)
        text1 = f1.render(self.text, True,
                          self.current_color, self.background)
        self.screen.blit(text1, (self.x, self.y))

    def activate(self):
        """
        change active fields color
        :return:
        """
        if not self.is_active:
            self.is_active = True
            self.current_color = self.base_color

    def deactivate(self):
        """
        chnge deactive fields in grey color
        :return:
        """
        if self.is_active:
            self.is_active = False
            self.current_color = (100, 100, 100)

    def set_text(self, text):
        """
        set text
        :param text: text
        :return:
        """
        self.text = text


class InsertField:
    """
    class for inserting
    """

    def __init__(self, value, x, y, width, height, screen):
        """
        init function
        :param value: value
        :param x: x position on screen
        :param y: y position on screen
        :param width: width
        :param height: height
        :param screen: surface
        """
        self.is_active = False
        self.value = str(value)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.text = Text(self.value, BLACK, (self.x + 7, self.y + 10), 40, self.screen, WHITE)

    def draw(self):
        """
        drawing text on screen
        :return:
        """
        pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.height))
        self.text.draw()

    def insert(self, char):
        """
        set text in field
        :param char: symbol
        :return:
        """
        if self.is_active:
            self.value = self.value[:-1]
            self.value += str(char)
            self.value += "|"
            self.text.set_text(self.value)

    def activate(self):
        """
        activate field
        :return:
        """
        if not self.is_active:
            self.is_active = True
            self.value += "|"
            self.text.set_text(self.value)

    def deactivate(self):
        """
        disactivate field
        :return:
        """
        if self.is_active:
            self.value = self.value[:-1]
            self.is_active = False
            self.text.set_text(self.value)

    def check_mouse(self):
        """
        check mouse position
        :return:
        """
        if self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y \
                + self.height:
            return True
        else:
            return False

    def get_value(self):
        try:
            if self.is_active:
                return self.value[:-1]
            else:
                return self.value
        except ValueError:
            return 0


class Button:
    """
    class for buttons
    """

    def __init__(self, x, y, w, h, text, screen, color=YELLOW, dx=0, dy=0):
        """
        init function
        :param x: x position
        :param y: y position
        :param w: width
        :param h: height
        :param text: text
        :param screen: surface
        :param color: color
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.screen = screen
        self.color = color
        self.text = text
        self.w = w
        self.h = h
        self.is_active = False
        self.text_class = Text(self.text, BLACK, (self.x + (self.w - len(self.text) * 22) / 2 + self.dx,
                                                  self.y + self.h * 0.2 + self.dy), self.h, self.screen, self.color)

    def draw(self):
        """
        draw text on the screen
        :return:
        """
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        self.text_class.draw()

    def check_mouse(self):
        """
        check mouse position
        :return:
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h:
            self.is_active = True
            self.color = (255, 235, 0)
            self.text_class = Text(self.text, BLACK,
                                   (self.x + (self.w - len(self.text) * 22) / 2 + self.dx,
                                    self.y + self.h * 0.2 + self.dy),
                                   self.h, self.screen, self.color)
            return True
        else:
            self.is_active = False
            self.color = YELLOW
            self.text_class = Text(self.text, BLACK,
                                   (self.x + (self.w - len(self.text) * 22) / 2 + self.dx,
                                    self.y + self.h * 0.2 + self.dy),
                                   self.h, self.screen, self.color)
            return False


class Animation(Window):

    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        self.finished = False
        self.return_button = Button(30, 700, 230, 70, "Return", self.screen, dx=-15)
        way = pygame.Surface((1200, 800), pygame.SRCALPHA, 32)
        self.way = way.convert_alpha()

    def run(self, angles, velocities, length, dt=1):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                    self.finished = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_button.check_mouse():
                        finished = True

            self.return_button.check_mouse()
            angles += dt * velocities
            self.draw_objects(angles, length)
            pygame.display.update()
            self.screen.fill(BLACK)

    def draw_objects(self, angles, length):
        pos_s = self.data_transform(angles, length)
        for i in range(len(angles)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i+1], 1)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i+1], 2)

        pygame.draw.circle(self.screen, YELLOW, pos_s[0], 2)
        pygame.draw.circle(self.way, WHITE, pos_s[-1], 1)
        self.return_button.draw()
        sc.blit(self.screen, (0, 0))
        sc.blit(self.way, (0, 0))

    @staticmethod
    def data_transform(angles, length):
        data_cos = np.cos(angles.copy())
        data_sin = np.sin(angles.copy())
        y_s = np.cumsum(length * data_cos)
        x_s = np.cumsum(length * data_sin)
        return np.column_stack([np.insert(x_s, 0, 0) + START_POS[0], np.insert(y_s, 0, 0) + START_POS[1]])
