import matplotlib.pyplot as plt
import control.matlab as matlab
import numpy
import math
import colorama as color


def control(string):
    ctrl = input(string)
    if ctrl == "exit":
        print("Выход из программы! Хорошего дня!")
        exit(0)
    return ctrl


def choice():   # звенья
    inerialessUnitName = "Безинерционное звено"
    aperiodicUnitName = "Апериодическое звено"
    integrUnitName = "Интегрирующее звено"
    iddefUnitName = "Идеально дифференцирующее звено"
    realdifUnitName = "Реально дифференцирующее звено"

    needNewChoice = True

    while needNewChoice:  # условия
        print(color.Style.RESET_ALL)
        userInput = control("Введите номер команды: \n"
                      "1 - " + inerialessUnitName + "; \n"
                      "2 - " + aperiodicUnitName + "; \n"
                      "3 - " + integrUnitName + "; \n"
                      "4 - " + iddefUnitName + "; \n"
                      "5 - " + realdifUnitName + "; \n")
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = "Безинерционное звено"
            elif userInput == 2:
                name = "Апериодическое звено"
            elif userInput == 3:
                name = "Интегрирующее звено"
            elif userInput == 4:
                name = "Идеально дифференцирующее звено"
            elif userInput == 5:
                name = "Реально дифференцирующее звено"
            else:
                print(color.Fore.RED + "\nНедопустимое значение! ")
                needNewChoice = True
        else:
            print(color.Fore.RED + "\nПожалуйста, введите числовое значение! ")
            needNewChoice = True
    return name


def getUnit(name):  # коэффициенты звеньев

    while True:
        k = control("Введите коэффициент k: ")
        t = control("Введите коэффициент t: ")
        try:
            k=float(k)
            t=float(t)
            if name == "Безинерционное звено":
                unit = matlab.tf([k], [1])
            elif name == "Апериодическое звено":
                unit = matlab.tf([k], [t, 1])
            elif name == "Интегрирующее звено":
                if t==0:
                    unit = matlab.tf([k], [1, 0])
                else:
                    unit = matlab.tf([1], [t, 1])
            elif name == "Идеально дифференцирующее звено":
                if t==0:
                    unit = matlab.tf([k, 0], [1/100000, 1])
                else:
                    unit = matlab.tf([t, 0], [1/100000, 1])
            elif name == "Реально дифференцирующее звено":
                unit = matlab.tf([k, 0], [t, 1])
            break
        except ValueError:
            print(color.Fore.RED + "\nПожалуйста, введите числовое значение!: ")
    return unit


def graph(num, title, y, x): #график
    plt.subplot(2, 1, num)
    plt.grid(True)
    if title == "Переходная характеристика":
        plt.plot(x, y, "purple")
    elif title == "Импульсная характеристика":
        plt.plot(x, y, "green")
    plt.title(title)
    plt.ylabel("Амплитуда")
    plt.xlabel("Время (с)")


print("\nДля выхода из программы введите: 'exit'")

while True:
    unitName = choice()
    unit = getUnit(unitName)

    timeLine = []
    for i in range (0, 10000):
        timeLine.append(i/1000)

    [y, x] = matlab.step(unit, timeLine)  # единичное воздействие
    graph(1, "Переходная характеристика", y, x)
    [y, x] = matlab.impulse(unit, timeLine)
    graph(2, "Импульсная характеристика", y, x)
    plt.show()
    matlab.bode(unit, dB=False)
    plt.plot()
    plt.show()
