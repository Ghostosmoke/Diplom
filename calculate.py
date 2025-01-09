from functools import reduce
from operator import mul
from math import factorial
def R():
    pass
def AverageWaitingTime(L:int,k:list):
    m_z = (1-reduce(mul,[1 / k[i] for i in range(1,L) for n in range(k[i]-1)]))
    return m_z
def AverageWaitingQueue(lambda_0:float,k:float,m_z:float,n:int,s:int)->float:
    alf = lambda_0 * m_z / k
    M = ((alf ** n / factorial(n) * sum([j * (alf / n) ** j for j in range(0,s)]))
         / (sum([alf ** j / factorial(j) for j in range(0,n)])
                 + alf ** n / factorial(n) * sum([(alf / n) ** j for j in range(1,s)])))
    return M
def AverageDelayUnregulatedCross():
    W_H = AverageWaitingTime() * AverageWaitingQueue()
    return W_H
