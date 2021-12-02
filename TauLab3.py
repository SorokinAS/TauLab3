import matplotlib.pyplot as plt
import control.matlab as matlab
import numpy as np
import sympy as sp
import math

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
    kp = 0.2 #float(input("Введите коэффициент пропорциональности kp: "))
    kdk = 2 #float(input("Введите дифференциальный коэффициент kdk: "))
    kd = matlab.tf([kdk, 0], [1])
    WPD = kp + kd
    #print('4.2. ПИД-регулятор')
    kp1 = 0.13
    ki1 = 0.0068
    kd1 = 0.54569
    ki = matlab.tf([ki1], [1, 0])
    kdd = matlab.tf([kd1, 0], [1])
    WPID = kp1 + ki + kdd
    return W1, W2, W3, WPD, WPID


def ht(SAU, title):
    print("Прямые оценки качества переходного процесса: \n")
    [y, t] = matlab.step(SAU)
    y_max = max(y)
    y_ust = y[len(y)-1]
    t_reg = None

    plt.grid(True)
    plt.plot(t, y, "red")
    plt.title(title)
    plt.xlabel("Время")
    plt.ylabel("Амплитуда")
    det = ((y_max - y[-1]) / y[-1]) * 100
    print("Перерегулирование: ", round(det, 2), "%")
    for i in range(len(y)-1,np.argmax(y), -1):
        if y[i] > y_ust * 1.05 or y[i] < y_ust * 0.95:
            t_reg = t[i-1]
            break
    print('Время регулирования: ', round(t_reg, 2), 'c\n')
    # print('Колебательность: ')
    # print('Степень затухания: ')
    plt.show()


def pol(SAU):
    print("Косвенные оценки качества переходного процесса: \n")
    pols = matlab.pzmap(SAU, True, None, 'Нули и полюса САУ')
    a_min = max(pols[0])
    print('Время регулирования: ', round(3/(abs(sp.re(a_min))), 2), 'c')
    mu = float(abs(sp.im(a_min)/(abs(sp.re(a_min)))))
    print('Степень колебательности: ', round(mu, 2))
    if mu ==0:
        sigma = math.inf
        fi = 1 - math.exp(-math.pi / math.inf)
    else:
        sigma = math.exp(math.pi / mu)
        fi = 1 - math.exp(-math.pi / mu)
    print('Перерегулирование: ', round(sigma, 2))
    print('Степень затухания: ', round(fi, 2))
    plt.show()


def loghar(SAU):
    log=matlab.bode(SAU)
    axes = plt.gcf().get_axes()
    axes[0].set_title("ЛАЧХ")
    axes[1].set_title("ЛФЧХ")
    plt.xlabel("Частота (рад/с)")
    plt.show()


w1, w2, w3, wpd, wpid = init()
SAU_with_PD = matlab.feedback(w1 * w2 * w3 * wpd, 1, -1)
SAU_with_PID = matlab.feedback(w1 * w2 * w3 * wpid, 1, -1)
# print('САУ с ПД регулятором: ', SAU_with_PD)
# print('САУ с ПИД регулятором: ', SAU_with_PID)

# ht(SAU_with_PD, 'Переходная характеристика ПД-регулятора')
# ht(SAU_with_PID, 'Переходная характеристика ПИД-регулятора')
# pol(SAU_with_PD)
# pol(SAU_with_PID)
loghar(SAU_with_PID)
