from functools import reduce
from operator import mul
from math import factorial
import numpy as np

def R(n: float , T_0: float , lambda_list: float):
    return 1

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
    print('''Ввод данных происходит по часовой стрелке начиная с дороги которая находится сверху''')
    kol = int(input('Введите количество полос, где крестообразный = 4, T-образный = 3'))
    line_T = None
    dict_number={
        1:'up',
        2:'right',
        3:'down',
        4:'left'
    }
    if kol == 3:
        print('Вы введи Т - образный перекресток. ')
        lint_T = str(input('Укажите какой полосы не будет из этих четырех вариантов(up,right,down,left)'))

    for i in range(kol):
        print('Ввод данных по количеству полос')
        if dict_number[i] != line_T:
            print('Вы вводите данные для',dict_number[i])

    m_z=AverageWaitingTime(k=2,)
    alf=m_z * lambda_[1] / k[1]
    if alf<1:
        W_H =
    else:
        alf=0.9
if __name__ == "__main__":
    main()
