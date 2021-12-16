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
    kp1 = 0.12999
    Ti = 149.2
    Td = 0.54
    ki = matlab.tf([1], [Ti, 0])
    kdd = matlab.tf([Td, 0], [1])
    WPID = kp1 + ki + kdd
    return W1, W2, W3, WPD, WPID


def ht(SAU, title):
    print("Прямой метод оценки качества переходного процесса: \n")
    [y, t] = matlab.step(SAU)
    y_max = max(y)
    y_ust = y[-1]
    t_reg = None
    i_reg = None
    M = 0
    k = 0
    fi = 0
    t_max1 = 0
    y_max_2 = 0
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
            i_reg = i
            break
    print('Время регулирования: ', round(t_reg, 2), 'c')

    for i in range(0, i_reg, 1):
        if (y[i] < y_ust and y[i+1] > y_ust) or (y[i] > y_ust and y[i+1] < y_ust):
            M += 1
    print('Колебательность: ', M)

    if M>=2:
        for i in range(len(y)):
            if y[i-1]<y[i] and y[i+1]<y[i]:
                k+=1
            if k == 2:
                y_max_2 = y[i]
                fi = 100*(y_max-(y_max_2-y_ust))/y_max
                break
    elif M==1:
        y_max_2 = y_ust
        fi = 100*((y_max-y_max_2)/y_max)
    for i in range(len(y)):
        if y[i] == y_max:
            t_max1 = i
    print('Степень затухания: ', fi, ' % ', '\nВеличина первого максимума: ', y_max, ', время его достижения : ', t[t_max1] , 'c', '\n _____________________________________________________')
    print("\nИнтегральный метод оценки качества переходного процесса: \n")
    Ql = np.trapz(y - y_ust, t)
    Qm = np.trapz(np.abs(y - y_ust), t)
    print('Интегральная оценка: ', round(Ql, 2), '\nМодульная интегральная оценка: ', round(Qm, 2),'\n_____________________________________________________')
    plt.show()


def pol(SAU):
    print("\nКорневой метод оценки качества переходного процесса: \n")
    pols = matlab.pzmap(SAU, True, None, 'Нули и полюса САУ')
    n = max(pols[0])
    print('Время регулирования: ', round(3/(abs(sp.re(n))), 2), 'c')

    mu=0
    for i in range(len(pols[0])):
        if sp.im(pols[0][i]) != 0:
            if abs(sp.im(pols[0][i])/sp.re(pols[0][i])) > mu:
                mu = abs(sp.im(pols[0][i])/sp.re(pols[0][i]))

    sigma = math.exp(math.pi/mu)

    fi = 1 - math.exp(-2*math.pi/mu)
    print('Степень колебательности: ', round(mu, 2),'\nПеререгулирование: ', round(sigma, 2), '\nСтепень затухания: ', round(fi, 2)), '\nКорневой показатель колебательности: ', round(1/mu, 2)
    plt.grid(True)
    plt.show()
    print('_____________________________________________________')


def get_AFH(SAU):
    print("\nЧастотный метод оценки качества переходного процесса: \n")
    j = sp.I
    omega = sp.symbols("w")
    n = [float(x) for x in SAU.num[0][0]]
    d = [float(x) for x in SAU.den[0][0]]
    for i in reversed(range(len(d))):
        d[i] = d[i] * (j * omega) ** (len(d)-i-1)
    for i in reversed(range(len(n))):
        n[i] = n[i] * (j * omega) ** (len(n)-i-1)
    num_sum = 0
    den_sum = 0
    for num in n:
        num_sum += num
    for num in d:
        den_sum += num
    W = num_sum/den_sum
    A = sp.sqrt(sp.re(W)**2+sp.im(W)**2)
    x = np.linspace(0, 1, 100)
    y = []
    for num in x:
        y.append(A.subs(omega, num))
    print('Показатель колебательности М: ', max(y)/y[0])

    i_cr = 0
    for i in range(len(y)):
        if (y[i] > y[0] and y[i+1] < y[0]) and i!=0:
            i_cr = i
    w_sr = (x[i_cr]+x[i_cr+1])/2
    print('Время регулирования tрег: ', round(2*math.pi/w_sr, 2), 'c -', round(2*2*math.pi/w_sr, 2), ' c ')
    print('_____________________________________________________')
    plt.title('Амплитудно-частотная характеристика')
    plt.plot(x, y)
    plt.grid(True)
    plt.xlim(0, 1)
    plt.ylim(0, 1.2)
    plt.xlabel("Частота")
    plt.ylabel("Aмплитуда")
    plt.show()


def log_har(SAU):
    matlab.bode(SAU)
    axes = plt.gcf().get_axes()
    axes[0].set_title("ЛАЧХ")
    axes[1].set_title("ЛФЧХ")
    plt.xlabel("Частота (рад/с)")
    plt.show()


w1, w2, w3, wpd, wpid = init()
SAU_with_PD = matlab.feedback(w1 * w2 * w3 * wpd, 1, -1)
SAU_with_PID = matlab.feedback(w1 * w2 * w3 * wpid, 1, -1)
razSAU_PD = matlab.series(w1, w2, w3, wpd)
razSAU_PID = matlab.series(w1, w2, w3, wpid)

ht(SAU_with_PD, 'Переходная характеристика ПД-регулятора')
ht(SAU_with_PID, 'Переходная характеристика ПИД-регулятора')
pol(SAU_with_PD)
pol(SAU_with_PID)
get_AFH(SAU_with_PD)
get_AFH(SAU_with_PID)
log_har(razSAU_PD)
log_har(razSAU_PID)

