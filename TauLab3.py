import matplotlib.pyplot as plt
import control.matlab as matlab
import numpy as np
import sympy as sp
from sympy.solvers import solve
from sympy import Symbol


def init():
    # print("1. Ввод генератора")
    Tg = 6.4  # float(input("Введите постоянную времени генератора Tg: "))
    W1 = matlab.tf([1], [Tg, 1])
    # print("2. Ввод турбины")
    # print("Паровая турбина: knm/(Tnm*p+1)")
    knm = 1  # float(input("Введите коэффициент knm: "))
    Tnm = 7  # float(input("Введите коэффициент Tnm: "))
    W2 = matlab.tf([knm], [Tnm, 1])
    # print("3. Усилительно-исполнительный орган")
    ky = 24 #float(input("Введите коэффициент ky: "))
    Ty = 5 #float(input("Введите постоянную времени Ty: "))
    W3 = matlab.tf([ky], [Ty, 1])
    # print("4. Регулятор")
    # print('4.1. ПД-регулятор')
    kp = 0.1 #float(input("Введите коэффициент пропорциональности kp: "))
    kdk = 0.3 #float(input("Введите дифференциальный коэффициент kdk: "))
    kd = matlab.tf([kdk, 0], [1])
    WPD = kp + kd
    #print('4.2. ПИД-регулятор')
    kp1 = 0.1
    ki1 = 0.005
    kd1 = 0.1
    ki = matlab.tf([ki1], [1, 0])
    kdd = matlab.tf([kd1, 0], [1])
    WPID=kp1+ki+kdd
    return W1, W2, W3, WPD, WPID


def ht(SAU, title):
    [y, x] = matlab.step(SAU)
    plt.grid(True)
    plt.plot(x, y, "red")
    plt.title(title)
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")


w1, w2, w3, wpd, wpid = init()
SAU_with_PD = matlab.feedback(w1 * w2 * w3 * wpd, 1, -1)
SAU_with_PID = matlab.feedback(w1 * w2 * w3 * wpid, 1, -1)
print('САУ с ПД регулятором: ', SAU_with_PD)
print('САУ с ПИД регулятором: ', SAU_with_PID)

ht(SAU_with_PD, 'Переходная характеристика САУ с ПД-регулятором')
plt.show()
ht(SAU_with_PID, 'Переходная характеристика САУ с ПИД-регулятором')
plt.show()
