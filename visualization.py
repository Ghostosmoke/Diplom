import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Определение размеров окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Схема дороги с перекрестком и транспортом")
#Дорога
WIDTH_ROAD = math.ceil(WIDTH // 8) #100

#Линия разделительных полос
WIDTH_LINE = math.ceil(WIDTH_ROAD // 10) #10

# Цвета
GREEN = (34, 177, 76)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN_LIGHT = (0, 255, 0)
color = [GREEN, BLACK, YELLOW, RED]


#0 - начальный пиксель по ширине
#1 - начальный пиксель по высоте
#2 - размер по ширине 100 значит 100 пикселей
#3 - размер по высоте

#rect(0,1,2,3)

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

    # Разрешение движение на лево
    def Move_allowed_left(self, x: float, y: float, left_right: bool = True):
        w_5=WIDTH_ROAD/5
        w_10=WIDTH_ROAD/10

        if left_right:
            vertices = [(x + w_5, y - 2 * w_10), (x, y - w_10), (x + 2 * w_5, y - w_10)]
            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x,
                                         y,
                                         w_5,
                                         w_10))
            pygame.draw.rect(window, WHITE,
                             pygame.Rect(x+w_5,
                                         y-w_10,
                                         w_10,
                                         w_5))
            pygame.draw.polygon(window,WHITE,vertices)

    # Разрешение движение на прямо
    def Move_allowed_straight(self):
        pass

    # Разрешение движение на право
    def Move_allowed_right(self):
        pass

    # Общая команда для сбора выдачи разрешение на движение в ту или иную сторону
    def Move_allowed(self):
        self.Move_allowed_left(x=100, y=100)

    # Пешеходный переход
    def draw_crosswalk(self, x: float, y: float, Width_crosswalk: float, left_right: bool = True, count_line: int = WIDTH_LINE):
        if left_right:
            for i in range(count_line):
                pygame.draw.rect(window, WHITE,
                                 pygame.Rect(x + i * Width_crosswalk / count_line + 2,
                                             y,
                                             Width_crosswalk / count_line / 2,
                                             WIDTH_ROAD / 3))
        else:
            for i in range(count_line):
                pygame.draw.rect(window, WHITE,
                                 pygame.Rect(x,
                                             y + i * Width_crosswalk / count_line + 2,
                                             WIDTH_ROAD / 3,
                                             Width_crosswalk / count_line / 2))

    # Рисует дорогу линии на дороге
    def draw_line_on_road(self, WIDTH_PIXEL: float = 0, HEIGHT_PIXEL: float = 0, up_right: bool = False,
                          dotted: bool = False):
        list_dot = [0, WIDTH if WIDTH >= HEIGHT else HEIGHT]
        if up_right:
            if dotted:
                list_dot = [i for i in range(0, HEIGHT, 4 * WIDTH_LINE)]
            #Сверху вниз
            for i in list_dot:
                pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL, HEIGHT_PIXEL + i, WIDTH_LINE, 2 * HEIGHT))
        else:
            if dotted:
                list_dot = [i for i in range(0, WIDTH, 4 * WIDTH_LINE)]
            #Слева направо
            for i in list_dot:
                pygame.draw.rect(window, WHITE, pygame.Rect(WIDTH_PIXEL + i, HEIGHT_PIXEL, 2 * WIDTH_LINE, WIDTH_LINE))
    # Рисует дорогу слева
    def draw_road_left(self, crosswalk: bool = True, dotted: bool = False,count_lane: int = 3):
        Width_left = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(0,
                                     self.Height_center(Width_left),
                                     self.Width_center(WIDTH_ROAD),
                                     Width_left))
        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(WIDTH_ROAD)-WIDTH_ROAD/3,
                                y=self.Height_center(Width_left),
                                Width_crosswalk=Width_left,
                                left_right=False,
                                count_line=math.ceil(WIDTH_LINE*count_lane/2))
    # Рисует дорогу справа
    def draw_road_right(self, crosswalk: bool = True,count_lane: int = 6):
        Width_right = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(-WIDTH_ROAD),
                                     self.Height_center(Width_right),
                                     WIDTH//2,
                                     Width_right))
        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(WIDTH_ROAD) + WIDTH_ROAD,
                                y=self.Height_center(Width_right),
                                Width_crosswalk=Width_right,
                                left_right=False,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))
    # Рисует дорогу сверху
    def draw_road_up(self, crosswalk: bool = True,count_lane: int = 6):
        Width_up = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(Width_up),
                                     0,
                                     Width_up,
                                     self.Height_center(WIDTH_ROAD)))

        if crosswalk:
            self.draw_crosswalk(x=self.Width_center(Width_up),
                                y=self.Height_center(WIDTH_ROAD) - WIDTH_ROAD/3,
                                Width_crosswalk=Width_up,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))
    # Рисует дорогу снизу
    def draw_road_down(self, crosswalk: bool = True,count_lane: int = 6):
        Width_down = WIDTH_ROAD * count_lane / 2
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(Width_down),
                                     self.Height_center(-WIDTH_ROAD),
                                     Width_down,
                                     Width_down))
        if crosswalk == True:
            self.draw_crosswalk(x=self.Width_center(Width_down),
                                y=self.Height_center(WIDTH_ROAD) + WIDTH_ROAD,
                                Width_crosswalk=Width_down,
                                count_line=math.ceil(WIDTH_LINE * count_lane / 2))
    # Рисует квадрат по центру
    def draw_road_center(self,max_line_up_down: int = 2, max_line_left_right: int = 2):
        pygame.draw.rect(window, GRAY,
                         pygame.Rect(self.Width_center(WIDTH_ROAD*max_line_left_right//2),
                                     self.Height_center(WIDTH_ROAD*max_line_up_down//2),
                                     WIDTH_ROAD*max_line_left_right//2,
                                     WIDTH_ROAD*max_line_up_down//2))


    # cross_T выбирается сторона которую не будет рисовать (варианты)['up','down','left','right']
    def draw_road(self, center_x: int = WIDTH//2 - WIDTH_ROAD//2, center_y: int = HEIGHT//2 - WIDTH_ROAD//2,
                  count_lane_up: int = 2, dotted_up: list = [],
                  count_lane_down: int = 1, dotted_down: list = [],
                  count_lane_right: int = 1, dotted_right: list = [],
                  count_lane_left: int = 1, dotted_left: list = [],
                  cross: bool = False,
                  cross_T: bool = True, line_T: str = 'up'):
        # Основная дорога
        if count_lane_left < 0:
            WIDTH_LEFT = 1/2 * count_lane_left * WIDTH_ROAD
            pygame.draw.rect(window, GRAY, pygame.Rect(self.Width_center(WIDTH_LEFT+WIDTH_ROAD), 0,
                                                       WIDTH_LEFT+WIDTH_ROAD, HEIGHT/2))
            for i in range(count_lane_left):
                bool_left = False
                if i in dotted_left:
                    bool_left = True
                self.draw_line_on_road(HEIGHT_PIXEL=0, WIDTH_PIXEL=self.Width_center(WIDTH_LINE), up_right=True,
                                       dotted=bool_left)
        if count_lane_right > 0:
            pass
        if count_lane_up > 0:
            pass
        if count_lane_down > 0:
            pass
        if cross:
            # Крестообразная
            pygame.draw.rect(window, GRAY, pygame.Rect(self.Width_center(WIDTH_ROAD), 0, WIDTH_ROAD, HEIGHT))
            self.draw_line_on_road(HEIGHT_PIXEL=0, WIDTH_PIXEL=self.Width_center(WIDTH_LINE), up_right=True)
            pygame.draw.rect(window, GRAY, pygame.Rect(0, self.Height_center(WIDTH_ROAD), WIDTH, WIDTH_ROAD))
            self.draw_line_on_road(HEIGHT_PIXEL=self.Height_center(WIDTH_LINE), WIDTH_PIXEL=0, dotted=True)
        if cross_T:
            pass
            # if 'up'!=line_T:
            #     self.draw_road_up()
            # if 'down' != line_T:
            #     self.draw_road_down()
            # if 'left'!=line_T:
            #     self.draw_road_left()
            # if 'right'!=line_T:
            #     self.draw_road_right()
            # self.draw_road_center()
        self.Move_allowed_left(100,100)
        #Центр

        max_up, max_left = 1, 1
        if count_lane_up > 1 or count_lane_down > 1:
            max_up = max(count_lane_up, count_lane_down)
        if count_lane_left > 1 or count_lane_right > 1:
            max_left = max(count_lane_left, count_lane_right)
        #pygame.draw.rect(window, RED, pygame.Rect(center_x,center_y, WIDTH_ROAD, self.Height_center(max_up * WIDTH_ROAD + 2*WIDTH_ROAD)))







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
    #traffic_light = TrafficLight(350, 250)
    #1.Вверху 2.Слева 3.Снизу  4.Правая
    #cross_car
    # cars = [Car(360, 150, (0, 0, 255), left_right=False),
    #         Car(240, 315, (255, 120, 0)),
    #         Car(415, 385, (0, 255, 0), left_right=False),
    #         Car(510, 260, (255, 0, 0))]
    #cross_car_t
    cars = [
            Car(240, 315, (255, 120, 0)),
            Car(415, 385, (0, 255, 0), left_right=False),
            Car(510, 260, (255, 0, 0))]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(GREEN)  # Заливка фона травой

        # Отрисовка дороги и перекрестка
        road.draw_road()
        #UP
        #road.draw_crosswalk(353, 215)
        #LEFT
        #road.draw_crosswalk(315, 253, left_right=False)
        #DOWN
        #road.draw_crosswalk(350, 353)
        #RIGHT
        #road.draw_crosswalk(450, 253, left_right=False)


        # Отрисовка машин
        for car in cars:
            car.draw()

        # Отрисовка светофора
        #traffic_light.draw()

        # Смени цвет светофора (для визуализации)
        #traffic_light.change_light()

        pygame.display.flip()  # Обновление дисплея
        clock.tick(1)  # Ограничение FPS для смены светофора каждые 2 секунды


if __name__ == "__main__":
    main()
