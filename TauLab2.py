import matplotlib.pyplot as plt
import control.matlab as matlab
from control.xferfcn import TransferFunction
import numpy as np
import math
import sympy as sp
from fractions import Fraction
from sympy.solvers import solve
from sympy import Symbol


def init():
    print("1. Ввод обратной связи")
    print("Жесткая обратная связь: Wос = kос ")
    koc = 0.340982142857143 #float(input("Введите коэффициент обратной связи kос: "))
    Toc = 2 #float(input("Введите постоянную времени обратной связи Tос: "))
    W1 = matlab.tf([koc], [1])
    print("2. Ввод генератора")
    Tg = 6.4 #float(input("Введите постоянную времени генератора Tg: "))
    W2 = matlab.tf([1], [Tg, 1])
    print("3. Ввод турбины")
    print("Паровая турбина: knm/(Tnm*p+1)")
    knm = 1 #float(input("Введите коэффициент knm: "))
    Tnm = 7 #float(input("Введите коэффициент Tnm: "))
    W3 = matlab.tf([knm], [Tnm, 1])
    print("4. Ввод исполнительного устройства")
    ky = 24 #float(input("Введите коэффициент ky: "))
    Ty = 5 #float(input("Введите постоянную времени Ty: "))
    W4 = matlab.tf([ky], [Ty, 1])
    return W1, W2, W3, W4


def ht(SAY):
     [y, x] = matlab.step(SAY)
     plt.grid(True)
     title = "Переходная характеристика"
     plt.plot(x, y, "red")
     plt.title(title)
     plt.xlabel("Время")
     plt.ylabel("Амплитуда")


def pol(SAU):
     pols = matlab.pole(SAU)
     rez="Система устойчива"
     print("Полюса: ", pols)
     for i in pols:
         if i.real > 0:
             rez="Система неустойчива, т.к. действительное значение полюса больше 0"
             break
         elif i.real==0:
             rez="Система находится на границе устойчивости"
     print(rez)


def kritNaikv(razSAU):
     matlab.nyquist(razSAU)
     plt.grid(True)
     plt.title('Диаграмма Найквиста')
     plt.xlabel('Re(s)')
     plt.ylabel('Im(s)')
     plt.show()


def loghar(razSAU):
     matlab.bode(razSAU)
     axes = plt.gcf().get_axes()
     axes[0].set_title("ЛАЧХ")
     axes[1].set_title("ЛФЧХ")
     plt.xlabel("Частота (рад/с)")
     plt.show()


def kritMikh(d):
    d = d[::-1]
    j = sp.I
    omega = sp.symbols("w")
    for i in range(len(d)):
        d[i] = d[i] * (j * omega) ** i
    x = np.arange(0, 1, 0.005)
    mc = []
    for i in x:
        summ = 0
        for k in d:
            summ += k.subs(omega, i)
        mc.append(summ)

    real = [sp.re(x) for x in mc]
    imaginary = [sp.im(x) for x in mc]
    Cross = False
    NumOfCross = 0
    for i in range(len(mc)-1):
        if ((real[i]<=0 and real[i+1]>=0)) or ((real[i]>=0 and real[i+1]<=0)) and Cross == False:
            NumOfCross+=1
            Cross = True
        if ((imaginary[i]<=0 and imaginary[i+1]>=0)) or ((imaginary[i]>=0 and imaginary[i+1]<=0)) and Cross == True:
            NumOfCross+=1
            Cross = False
    if NumOfCross !=3:
        print("Критерий Михайлова: Система неустойчива")
    else:
        print("Критерий Михайлова: Система устойчива")

    plt.title('Годограф Михайлова')
    ax = plt.gca()
    ax.plot(real, imaginary)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    plt.xlim(-50, 200)
    plt.ylim(-25,10)
    plt.xlabel("re")
    plt.ylabel("im")
    plt.show()


def kritGurv(d,nu):
    x = Symbol('x')
    st = "Система устойчива"
    dr1=[]
    dr2=[]
    for i in range(0, len(d),2):
        dr2.append(d[i])
    for i in range(1, len(d)+1,2):
        dr1.append(d[i])
    fr=[]
    fr.append(dr1)
    fr.append(dr2)
    print(fr)
    det = np.linalg.det(fr)
    print(det)
    if det<0 or fr[0][0]<0 or fr[1][0]<0:
        st = 'Критерий Гурвица: Система неустойчива'
    else:
        st = 'Критерий Гурвица: Система устойчива'
    print(st)
    fr[0][1]=1+nu*x
    kos = solve(fr[0][0]*fr[1][1]-fr[0][1]*fr[1][0],x)
    print("Предельное значение коэффициента обратной связи: ", kos[0])


w1, w2, w3, w4 = init()
razSAU = matlab.series(w1, w2, w3, w4)
SAU = matlab.feedback(w2 * w3 * w4, w1, -1)
print(SAU)
n = [float(x) for x in SAU.num[0][0]]
d = [float(x) for x in SAU.den[0][0]]
nu=n[len(n)-1]


ht(SAU)
plt.show()
pol(SAU)
kritNaikv(razSAU)
loghar(razSAU)
kritMikh(d)
st = kritGurv(d,nu)
