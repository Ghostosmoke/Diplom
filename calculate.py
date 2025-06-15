from functools import reduce
from operator import mul
from math import factorial
import numpy as np
from pprint import pprint
import pygame
import visualization
import sys

def R(n: float , T_0: float , lambda_list: float):
    return 1
from visualization import Road,WIDTH,HEIGHT,GREEN
'''
L - число потоков которые надо пересечь
lambda_ - параметры этих потоков, которые распределены по специальному закону Эрланга порядков k[1], …, k[L]  соответственно;
Т_0 – минимальный интервал по времени между подряд идущими автомобилями, необходимый для продолжения движения;
r_(start) - это замена формулы где параметр start отвечает за начальное значение списка Произведение списка
'''
def AverageWaitingTime(L: int , k: list , T_0: float , lambda_: list):
    def r_(start: int):
        return reduce(mul , [R(n , T_0 , lambda_[i]) / k[i] for i in range(start , L) for n in range(k[i] - 1)])
    m_z = ((1 - r_(1)) * (k[1] + 1 + (k[1] - 1) * (1 - R(k[1] - 1 , T_0 , lambda_[1])) * r_(2))
           / (2 * lambda_[1] * R(k[1] - 1,T_0,lambda_[1]) * r_(2)))
    return m_z


def AverageWaitingQueue(lambda_0: float , k: float , m_z: float , n: int , s: int) -> float:
    alf = lambda_0 * m_z / k
    M = ((alf ** n / factorial(n) * sum([j * (alf / n) ** j for j in range(0 , s)]))
         / (sum([alf ** j / factorial(j) for j in range(0 , n)])
            + alf ** n / factorial(n) * sum([(alf / n) ** j for j in range(1 , s)])))
    return M


def AverageDelayUnregulatedCross(lambda_0: float , T_0: float , lambda_: list, k: float , m_z: float , n: int , s: int , L: int , k_list: list):
    W_H = AverageWaitingTime(L , k_list, T_0 , lambda_) * AverageWaitingQueue(lambda_0 , k , m_z , n , s)
    return W_H

def main():
    def main_road(road):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    # sys.exit()

            visualization.window.fill(GREEN)  # Заливка фона травой
            road.draw_road()
            pygame.display.flip()  # Обновление дисплея
            clock.tick(1)
        pygame.quit()
    print('''Ввод данных происходит по часовой стрелке начиная с дороги которая находится сверху''')
    kol_road = int(input('Введите количество полос, где крестообразный = 4, T-образный = 3: '))
    line_T = None
    dict_number={
        1:'up',
        2:'right',
        3:'down',
        4:'left'
    }
    kol_lane_massive=[]
    road=Road()
    massive_road_lane = []
    if kol_road == 3:
        print('Вы вели Т - образный перекресток. ')
        line_T = str(input('Укажите какой полосы не будет из этих четырех вариантов(up,right,down,left): '))

    if kol_road == 4:
        print('Вы вели Крестообразный перекресток. ')

    print('Ввод данных по количеству полос')
    for dict in dict_number:
        if dict_number[dict] != line_T:

            print('Вы вводите данные для',dict_number[dict])
            kol_road_lane = int(input('Введите количество полос: '))
            kol_lane_massive.append(kol_road_lane)
            massive_road_lane.append([])
            for _ in range(kol_road_lane):
                massive_road_lane[-1].append(0)
        else:
            kol_lane_massive.append(0)
    pprint(massive_road_lane)
    main_road()
    if line_T == None:
        road.draw_road(kol_lane_massive[0] , kol_lane_massive[1] , kol_lane_massive[2] , kol_lane_massive[3],cross=True)
    else:
        road.draw_road(kol_lane_massive[0] , kol_lane_massive[1] , kol_lane_massive[2] , kol_lane_massive[3],cross_T=True,line_T=line_T)
    print('Ввод данных на возможные направления для данной полосы')
    print('Введите данные для направления движения (0 = вверх, 90 = вправо, 180 = вниз, 270 = влево)')
    kol = 1
    for road_lane in massive_road_lane:
        for i in range(len(road_lane)):
            print('Введите значение или значения через пробел для',kol,'направления: ')
            kol +=1
            road_lane[i] = list(map(int, input().split()))
            print(road_lane)
    pprint(massive_road_lane)

    print('Ввод интенсивности на каждую полосу')
    print('Если нет интенсивности на поворот ')

    # m_z=AverageWaitingTime(k=2,)
    # alf=m_z * lambda_[1] / k[1]
    # if alf<1:
    #     W_H =
    # else:
    #     alf=0.9
if __name__ == "__main__":
    main()
