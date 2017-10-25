# -*- coding: UTF-8 -*-
import numpy as np
from tkinter import *

import NeuroMatrix as nm

varColor = ["#DA909F", "#DCCA54", "#389299"]

txtResult = [Text, Text, Text]
cpt = "Здесь будут результаты по {0} из наиболее возможных заболеваний при выбранном наборе симптомов";

# ============ Пересчет вывода

def RecalcCommand(i):
    def callback(i):
        for k in range(1, nm.lslLen):
            nm.si[k] = float(ss[k].get())
        CalcEmpty() if sum(nm.si) == 9.0 else CalcSi(nm.si)
    return callback


def RecalcAllCommand():
    def callback():
        for k in range(1, nm.lslLen):
            nm.si[k] = float(ss[k].get())
        CalcEmpty() if sum(nm.si) == 9.0 else CalcSi(nm.si)
    return callback

def RecalcAll():
    for k in range(1, nm.lslLen):
        nm.si[k] = float(ss[k].get())
    CalcEmpty() if sum(nm.si) == 9.0 else CalcSi(nm.si)
    return

def CalcEmpty():
    diag="При выбранном наборе симптомов Вы практически здоровы"
    for i in range(0, 3):
        txtResult[i].delete(1.0, 50.0)
        txtResult[i].insert(CURRENT, diag)
    return

def CalcSi(si):
    sim = si / 9.
    # print si
    # умножение вектора симтомов на оценочную матрицу
    di = np.dot(nm.dm, sim)

    dimax = [0, 0, 0]
    armax = [0, 0, 0]

    # определение номеров наиболее подходящих диагнозов
    for i in range(0, 3):
        dimax[i] = di.max()
        armax[i] = np.argmax(di, axis=0)
        di[armax[i]] = 0
        # print( dimax, armax)

    # Какое-то шаманство
    dms = dimax[0] + dimax[1] + dimax[2]
    dimax[0] = dimax[0] / dms
    dimax[1] = dimax[1] / dms
    dimax[2] = dimax[2] / dms

    # Вывод
    for i in range(0, 3):
        txtResult[i].delete(1.0, 50.0)
        res = str(nm.diag[armax[i]]) + "\n - С коэффициенто уверенности \n К = " + str(dimax[i])
        txtResult[i].insert(CURRENT, res)

    # Перерисовка картинок
    for i in range(1, nm.lslLen):
        for j in range(0, 3):
            #cbtn = Button(framel, height=15, bitmap='warning', width=20)
            #cbtn.grid(row=i + 1, column=j)
            #color = varColor[j] if nm.sii[i - 1, armax[j]] == 1 else 'white'
            #cbtn.config(bg=color)
            cbtn = Label(framel, height=15, bitmap='warning', width=20)
            cbtn.grid(row=i + 1, column=j)
            color = varColor[j] if nm.sii[i - 1, armax[j]] == 1 else 'white'
            cbtn.config(bg=color)

#  ОСНОВНАЯ ПРОГА
root = Tk()
root.title("Диагностика аутоимунных заболеваний")


# ЛЕВО   подсвечивание симптоматики цветные квадратики
framel = Frame(root, bd=5)
framel.grid(row=0, column=0)

for i in range(0, 3):
    Label(framel, text=i + 1, fg='red').grid(row=0, column=i)
    for j in range(1, nm.lslLen):
        b = Label(framel, height=15, bitmap='warning', width=20, bg='white')
        b.grid(row=j + 1, column=i)


# ЦЕНТР Описание вывода
framec = Frame(root, bd=5)
framec.grid(row=0, column=1)

Label(framec, text="Выраженность", fg='red').grid(row=0, column=0)
Label(framec, text="Симптомы", fg='red').grid(row=0, column=1)

# Ползунки
ss = {}
for i in range(1, nm.lslLen):
    Label(framec, text=nm.sl[i], width=18, bd=2).grid(row=i + 1, column=1)
    ss[i] = DoubleVar()
    ss[i].set(nm.si[i])
    ss[i] = Scale(framec, orient=HORIZONTAL, length=100, from_=0., to=9., variable=ss[i],
                  sliderlength=15, showvalue=0, highlightthickness=0, width=12, bd=1, command=RecalcCommand(i))
    ss[i].grid(row=i + 1, column=0)


# ПРАВО - результат
framer = Frame(root, bd=5)
framer.grid(row=0, column=2)

evbut = Button(framer, text="ДИАГНОСТИКА", width=20, command=RecalcAllCommand(), fg='red')
evbut.grid(row=0, column=0)

for i in range(0, 3):
    cpt = "Здесь будут результаты по {0} из наиболее возможных заболеваний при выбранном наборе симптомов";
    cptEnum = ["первому", "второму", "третьему"]
    txtResult[i] = Text(framer, width=40, height=8, bg=varColor[i])
    txtResult[i].grid(row=i + 1, column=0)
    txtResult[i].insert(CURRENT, cpt.format(cptEnum[i]))

#RecalcAll();

root.mainloop()

