import pygame
import random

COLORS = ["cyan", "blue", "orange", "purple", "#ff6600", "green", "yellow"]


class Figure:
    """Здесь находятся все виды и повороты фигур, св-ва фигур\n
    В figures записаны все фигуры и их положения в кубе на 4х4."""
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = COLORS[self.type]
        self.rotation = 0

    def picture(self):
        """Возвращает положение фигуры"""
        return self.figures[self.type][self.rotation]

    def rotate(self):
        """Вращает фигуру"""
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        """Создает новую фигуру"""
        self.figure = Figure(3, 0)

    def overlap(self):
        """Проверка пересечения фигуры с границами игры или с фигурами.\n
        Мы проверяем по высоте, далее по ширине, и после есть ли ниже фигуры другая фигура"""
        overlaping = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.picture():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        overlaping = True
        return overlaping

    def break_lines(self):
        """Проверка на полные линии.\n
        Если есть полная линия, то она уничтожается, а все верхние линии спускаются на уровень вниз"""
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        """Быстрый спуск нажатием Space"""
        while not self.overlap():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def freeze(self):
        """Позволяет заморозить фигуру на месте прикосновения с другими фигурами или нижней границей"""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.picture():
                    self.field[i + self.figure.y][j + self.figure.x] = COLORS.index(self.figure.color) + 1
        self.break_lines()
        self.new_figure()
        if self.overlap():
            self.state = "gameover"

    def go_down(self):
        """Спуск нажатием Кнопки Вниз"""
        self.figure.y += 1
        if self.overlap():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        """Влево-вправо фигуру перемещает"""
        old_x = self.figure.x
        self.figure.x += dx
        if self.overlap():
            self.figure.x = old_x

    def rotate(self):
        """Переворачивает фигуру"""
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.overlap():
            self.figure.rotation = old_rotation


pygame.init()

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

running = True  # игровой цикл
clock = pygame.time.Clock()
fps = 30
game = Tetris(20, 10)
counter = 0  # счетчик кол-ва фигур

pressing_down = False  # зажатие кнопки вниз

while running:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill('white')

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, 'gray', [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, COLORS[game.field[i][j] - 1],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
    # рисование клеток и фигур

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.picture():
                    pygame.draw.rect(screen, game.figure.color,
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
    # рисование действующей фигуры

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, 'black')
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
