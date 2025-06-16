import pygame
import sys
import math
import numpy as np

from pprint import pprint


# Инициализация Pygame
pygame.init()
# Определение размеров окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Схема дороги с перекрестком и транспортом")


# Дорога
WIDTH_ROAD = math.ceil(WIDTH // 8)  # 100

# Линия разделительных полос
WIDTH_LINE = math.ceil(WIDTH_ROAD // 10)  # 10

# Для разрешение поворота
w_5 = WIDTH_ROAD / 5 #20
w_10 = WIDTH_ROAD / 10 #10

# Цвета
GREEN = (34, 177, 76)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN_LIGHT = (0, 255, 0)
color = [GREEN, GRAY, WHITE, BLACK, RED, YELLOW, GREEN_LIGHT]


# 0 - начальный пиксель по ширине
# 1 - начальный пиксель по высоте
# 2 - размер по ширине 100 значит 100 пикселей
# 3 - размер по высоте

# rect(0,1,2,3)

# Класс для создания дороги
class Road:
    def __init__(self):
        pass

    # Центрирование по ширине
    def Width_center(self, width: float) -> float:
        return (WIDTH - width) // 2

    # Центрирование по высоте
    def Height_center(self, height: float) -> float:
        return (HEIGHT - height) // 2

    #Рисует разрешенные направления для движения для каждой стороны
    def Move_allowed(self, x: float, y: float, angle: int):
        # Стрелка налево
        if angle == 270:
            vertices = [(x - w_5 * 7 / 5, y - w_10 * 3 / 5), (x - w_10, y - w_5), (x - w_10, y + w_10)]
            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x - w_5 / 2,
                                         y - w_10,
                                         w_5,
                                         w_10))
            pygame.draw.polygon(window, WHITE, vertices)
        # Стрелка вниз
        if angle == 180:
            vertices = [(x + w_10 / 2, y + w_5 * 3 / 2), (x - w_10, y + w_5 * 2 / 3), (x + w_5, y + w_5 * 2 / 3)]
            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x,
                                         y,
                                         w_10,
                                         w_5))
            pygame.draw.polygon(window, WHITE, vertices)
        # Стрелка вправо
        if angle == 90:
            vertices = [(x + w_5 * 2, y - w_10 * 3 / 5), (x + w_5, y - w_5), (x + w_5, y + w_10)]
            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x + w_5 / 100,
                                         y - w_10,
                                         w_5,
                                         w_10))

            pygame.draw.polygon(window, WHITE, vertices)
        # Стрелка вверх
        if angle == 0:
            vertices = [(x + w_10 / 2, y - 2 * w_5), (x - w_10, y - w_5), (x + w_5, y - w_5)]

            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x,
                                         y - 2 * w_10,
                                         w_10,
                                         w_5))
            pygame.draw.polygon(window, WHITE, vertices)

    # Общая команда для сбора выдачи разрешение на движение в ту или иную сторону
    def Move_allowed_all(self, x: float, y: float, angle: list):
        for i in angle:
            self.Move_allowed(x, y, angle=i)

    # Пешеходный переход
    def draw_crosswalk(self, x: float, y: float, Width_crosswalk: float, left_right: bool = True,
                       count_line: int = WIDTH_LINE):
        if left_right:
            for i in range(count_line):
                pygame.draw.rect(window, WHITE,
                                 pygame.Rect(x,
                                             y + i * Width_crosswalk / count_line + 2,
                                             WIDTH_ROAD / 3,
                                             Width_crosswalk / count_line / 2))
        else:
            for i in range(count_line):
                pygame.draw.rect(window, WHITE,
                                 pygame.Rect(x + i * Width_crosswalk / count_line + 2,
                                             y,
                                             Width_crosswalk / count_line / 2,
                                             WIDTH_ROAD / 3))

    #Рисует линию по вертикали
    def draw_line_vertical(self, WIDTH_PIXEL: float = 0, HEIGHT_PIXEL: float = 0, dotted: bool = False):
        if dotted:
            list_dot = [i for i in range(0, HEIGHT//2, 4 * WIDTH_LINE)]
            for i in list_dot:
                pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL, HEIGHT_PIXEL + i, WIDTH_LINE, 2 * WIDTH_LINE))
        else:
            pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL, HEIGHT_PIXEL, WIDTH_LINE, HEIGHT//2))

    #Рисует линию по горизонтали
    def draw_line_horizontal(self, WIDTH_PIXEL: float = 0, HEIGHT_PIXEL: float = 0, dotted: bool = False):
        if dotted:
            list_dot = [i for i in range(0, WIDTH//2, 4 * WIDTH_LINE)]
            for i in list_dot:
                pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL + i, HEIGHT_PIXEL, 2 * WIDTH_LINE, WIDTH_LINE))
        else:
            pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL, HEIGHT_PIXEL, WIDTH//2, WIDTH_LINE))

    # Рисует дорогу слева
    def draw_road_left(self, crosswalk: bool = True, count_lane: int = 3,
                       alloweds: list = [[0,90],[90],[90],[90],[90],[90,180]]):
        Width_left = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(0,
                                     self.Height_center(Width_left),
                                     self.Width_center(WIDTH_ROAD),
                                     Width_left))
        for j in range(count_lane):
            self.Move_allowed_all(x=w_5,
                              y=self.Height_center(WIDTH_ROAD * (count_lane / 2 - j - 0.6)),angle=alloweds[j])
        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(WIDTH_ROAD) - WIDTH_ROAD / 3,
                                y=self.Height_center(Width_left),
                                Width_crosswalk=Width_left,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))

    # Рисует дорогу справа
    def draw_road_right(self, crosswalk: bool = True, count_lane: int = 6, width_crosswalk: float = 0,
                        alloweds: list = [[180,270],[180],[180],[180],[180],[90,180]]):
        Width_right = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(-WIDTH_ROAD),
                                     self.Height_center(Width_right),
                                     WIDTH // 2,
                                     Width_right))
        for j in range(count_lane):
            self.Move_allowed_all(x=WIDTH - w_5,
                              y=self.Height_center(WIDTH_ROAD * (count_lane / 2 - j - 0.4)),angle=alloweds[j])
        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(WIDTH_ROAD) + WIDTH_ROAD + width_crosswalk,
                                y=self.Height_center(Width_right),
                                Width_crosswalk=Width_right,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))


    # Рисует дорогу сверху
    def draw_road_up(self, crosswalk: bool = True, count_lane: int = 6,
                     alloweds: list = [[180,270],[180],[180],[180],[180],[90,180]]):
        Width_up = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(Width_up),
                                     0,
                                     Width_up,
                                     self.Height_center(WIDTH_ROAD)))

        for j in range(count_lane):
            self.Move_allowed_all(x=self.Width_center(WIDTH_ROAD * (count_lane / 2 - j - 0.4)),
                              y=w_5,angle=alloweds[j])

        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(Width_up),
                                y=self.Height_center(WIDTH_ROAD) - WIDTH_ROAD / 3,
                                Width_crosswalk=Width_up,
                                left_right=False,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))

    # Рисует дорогу снизу
    def draw_road_down(self, crosswalk: bool = True, count_lane: int = 6,
                       alloweds: list = [[0,270],[0],[0],[0],[0],[90,0]]):
        Width_down = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(Width_down),
                                     self.Height_center(-WIDTH_ROAD//2),
                                     Width_down,
                                     WIDTH // 2))
        for j in range(count_lane):
            self.Move_allowed_all(x=self.Width_center(WIDTH_ROAD * (count_lane / 2 - j - 0.4)),
                              y=HEIGHT-w_5,angle=alloweds[j])
        if crosswalk == True:
            self.draw_crosswalk(x=self.Width_center(Width_down),
                                y=self.Height_center(WIDTH_ROAD) + WIDTH_ROAD,
                                Width_crosswalk=Width_down,
                                left_right=False,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))

    # Рисует квадрат по центру
    def draw_road_center(self, max_line_up_down: int = 3, max_line_left_right: int = 2):
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(WIDTH_ROAD * max_line_left_right // 2),
                                     self.Height_center(WIDTH_ROAD * max_line_up_down // 2),
                                     WIDTH_ROAD * max_line_left_right // 2,
                                     WIDTH_ROAD * max_line_up_down // 2))

    # cross_T выбирается сторона которую не будет рисовать (варианты)['up','down','left','right']
    def draw_road(self,
                  count_lane_up: int = 2, count_lane_down: int = 3, count_lane_right: int = 2, count_lane_left: int = 2,
                  dotted_line: list = [0, 0, 0, 0],
                  cross: bool = False,
                  cross_T: bool = True, line_T: str = 'up', crosswalk: list = [False,False,False,False],alloweds: list = []):
        # allowed = [np.zeros((count_lane_up,1)),np.zeros((count_lane_right,1))
        #     ,np.zeros((count_lane_down,1)),np.zeros((count_lane_left,1))]
        if cross:

            max_horizontal = max(count_lane_up, count_lane_down)
            max_vertical = max(count_lane_right, count_lane_left)

            self.draw_road_up(crosswalk[0], count_lane_up)
            for i in range(count_lane_up-1):
                self.draw_line_vertical(WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_up / 2 - i - 1)) - WIDTH_LINE//2,
                                  HEIGHT_PIXEL=0, dotted=True)
                if dotted_line[0] == i:
                    self.draw_line_vertical(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_up / 2 - i - 1)) - WIDTH_LINE // 2,
                        HEIGHT_PIXEL=0, dotted=False)

            self.draw_road_right(crosswalk[1], count_lane_right, width_crosswalk=(max_vertical-2)*WIDTH_LINE)
            for i in range(count_lane_right-1):
                self.draw_line_horizontal(
                    WIDTH_PIXEL=self.Width_center(WIDTH_ROAD // 2),
                    HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_right / 2 - i - 1)) - WIDTH_LINE // 2,
                    dotted=True)
                if dotted_line[2] == i:
                    self.draw_line_horizontal(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD//2),
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_right / 2 - i - 1)) - WIDTH_LINE // 2)

            self.draw_road_down(crosswalk[2], count_lane_down)
            for i in range(count_lane_down-1):
                self.draw_line_vertical(WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_down / 2 - i - 1)) - WIDTH_LINE//2,
                                  HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD//2), dotted=True)
                if dotted_line[2] == i:
                    self.draw_line_vertical(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_down / 2 - i - 1)) - WIDTH_LINE // 2,
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD//2), dotted=False)

            self.draw_road_left(crosswalk[3], count_lane_left)
            for i in range(count_lane_left - 1):
                self.draw_line_horizontal(
                    WIDTH_PIXEL=0,
                    HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_left / 2 - i - 1)) - WIDTH_LINE // 2,
                    dotted=True)
                if dotted_line[3] == i:
                    self.draw_line_horizontal(
                        WIDTH_PIXEL=0,
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_left / 2 - i - 1)) - WIDTH_LINE // 2)

            self.draw_road_center(max_line_up_down=max_vertical,max_line_left_right=max_horizontal)

        if cross_T:
            max_horizontal = max(count_lane_up , count_lane_down)
            max_vertical = max(count_lane_right , count_lane_left)
            if 'up'!=line_T:


                self.draw_road_up(crosswalk[0] , count_lane_up)
                for i in range(count_lane_up - 1):
                    self.draw_line_vertical(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_up / 2 - i - 1)) - WIDTH_LINE // 2 ,
                        HEIGHT_PIXEL=0 , dotted=True)
                    if dotted_line[0] == i:
                        self.draw_line_vertical(
                            WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_up / 2 - i - 1)) - WIDTH_LINE // 2 ,
                            HEIGHT_PIXEL=0 , dotted=False)
            if 'down' != line_T:
                self.draw_road_down(crosswalk[2] , count_lane_down)
                for i in range(count_lane_down - 1):
                    self.draw_line_vertical(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD * (count_lane_down / 2 - i - 1)) - WIDTH_LINE // 2 ,
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD // 2) , dotted=True)
                    if dotted_line[2] == i:
                        self.draw_line_vertical(
                            WIDTH_PIXEL=self.Width_center(
                                WIDTH_ROAD * (count_lane_down / 2 - i - 1)) - WIDTH_LINE // 2 ,
                            HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD // 2) , dotted=False)
            if 'left'!=line_T:
                self.draw_road_left(crosswalk[3] , count_lane_left)
                for i in range(count_lane_left - 1):
                    self.draw_line_horizontal(
                        WIDTH_PIXEL=0 ,
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_left / 2 - i - 1)) - WIDTH_LINE // 2 ,
                        dotted=True)
                    if dotted_line[3] == i:
                        self.draw_line_horizontal(
                            WIDTH_PIXEL=0 ,
                            HEIGHT_PIXEL=self.Height_center(
                                WIDTH_ROAD * (count_lane_left / 2 - i - 1)) - WIDTH_LINE // 2)
            if 'right'!=line_T:
                self.draw_road_right(crosswalk[1] , count_lane_right , width_crosswalk=(max_vertical - 2) * WIDTH_LINE)
                for i in range(count_lane_right - 1):
                    self.draw_line_horizontal(
                        WIDTH_PIXEL=self.Width_center(WIDTH_ROAD // 2) ,
                        HEIGHT_PIXEL=self.Height_center(WIDTH_ROAD * (count_lane_right / 2 - i - 1)) - WIDTH_LINE // 2 ,
                        dotted=True)
                    if dotted_line[2] == i:
                        self.draw_line_horizontal(
                            WIDTH_PIXEL=self.Width_center(WIDTH_ROAD // 2) ,
                            HEIGHT_PIXEL=self.Height_center(
                                WIDTH_ROAD * (count_lane_right / 2 - i - 1)) - WIDTH_LINE // 2)
            self.draw_road_center(max_line_up_down=max_vertical,max_line_left_right=max_horizontal)


# Класс для машины
class Car:
    def __init__(self, x, y, color: tuple = (255, 255, 255), left_right: bool = True):
        if left_right:
            self.width = WIDTH_ROAD / 2
            self.height = WIDTH_ROAD / 4
        else:
            self.width = WIDTH_ROAD / 4
            self.height = WIDTH_ROAD / 2
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


# Класс для светофора
class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'red'  # Начальное состояние

    def draw(self):
        # Основание светофора
        pygame.draw.rect(window, BLACK, pygame.Rect(self.x, self.y, 20, 50))
        # Светофор
        colors = [RED, YELLOW, GREEN_LIGHT]
        for i, color in enumerate(colors):
            pygame.draw.circle(window, color if self.state == color else BLACK, (self.x + 10, self.y + 10 + i * 15), 7)

    def change_light(self):
        # Логика смены светофора
        if self.state == 'red':
            self.state = 'green'
        else:
            self.state = 'red'


# Основная функция
def main():

    clock = pygame.time.Clock()

    road = Road()
    # traffic_light = TrafficLight(350, 250)
    # 1.Вверху 2.Слева 3.Снизу  4.Правая
    # cross_car
    # cars = [Car(360, 150, (0, 0, 255), left_right=False),
    #         Car(240, 315, (255, 120, 0)),
    #         Car(415, 385, (0, 255, 0), left_right=False),
    #         Car(510, 260, (255, 0, 0))]
    # cross_car_t
    # cars = [
    #     Car(240, 315, (255, 120, 0)),
    #     Car(415, 385, (0, 255, 0), left_right=False),
    #     Car(510, 260, (255, 0, 0))]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False


                # sys.exit()

        window.fill(GREEN)  # Заливка фона травой

        # Отрисовка дороги и перекрестка
        road.draw_road()
        # UP
        # road.draw_crosswalk(353, 215)
        # LEFT
        # road.draw_crosswalk(315, 253, left_right=False)
        # DOWN
        # road.draw_crosswalk(350, 353)
        # RIGHT
        # road.draw_crosswalk(450, 253, left_right=False)

        # Отрисовка машин
        # for car in cars:
        #     car.draw()

        # Отрисовка светофора
        # traffic_light.draw()

        # Смени цвет светофора (для визуализации)
        # traffic_light.change_light()

        pygame.display.flip()  # Обновление дисплея
        clock.tick(1)  # Ограничение FPS для смены светофора каждые 2 секунды
    pygame.quit()
if __name__ == "__main__":
    main()
    main()
