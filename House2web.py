# -*- coding: UTF-8 -*-
import numpy as np
import remi.gui as gui
from remi import start, App

import NeuroMatrix as nm

varColor = {}
varColor = ["#DA909F", "#DCCA54", "#389299"]


# ============ Пересчет вывода

def Recalc(i):
    def callback(i):
        for k in range(1, nm.lslLen):
            nm.si[k] = float(ss[k].get())
        CalcEmpty() if sum(nm.si) == 9.0 else CalcSi(nm.si)
    return callback

def RecalcAll():
    def callback():
        for k in range(1, nm.lslLen):
            nm.si[k] = float(ss[k].get())
        CalcEmpty() if sum(nm.si) == 9.0 else CalcSi(nm.si)
    return callback



def CalcEmpty():
    diag="При выбранном наборе симптомов Вы практически здоровы"
    d1.delete(1.0, 50.0)
    d2.delete(1.0, 50.0)
    d3.delete(1.0, 50.0)
    d1.insert(CURRENT, diag)
    d2.insert(CURRENT, diag)
    d3.insert(CURRENT, diag)
    return

def CalcSi(si):
    sim = si / 9.
    # print si
    # умножение вектора симтомов на оценочную матрицу
    di = np.dot(nm.dm, sim)

    # определение номеров наиболее подходящих диагнозов
    dimax1 = di.max()
    i1 = np.argmax(di, axis=0)
    di[i1] = 0
    # print( dimax1,i1)

    dimax2 = di.max()
    i2 = np.argmax(di, axis=0)
    di[i2] = 0
    # print( dimax2,i2)

    dimax3 = di.max()
    i3 = np.argmax(di, axis=0)
    # print( dimax3,i3)

    dms = dimax1 + dimax2 + dimax3
    dimax1 = dimax1 / dms
    dimax2 = dimax2 / dms
    dimax3 = dimax3 / dms

    ku = " - С коэффициенто уверенности \n К =="
    # Вывод
    d1.delete(1.0, 50.0)
    d2.delete(1.0, 50.0)
    d3.delete(1.0, 50.0)

    d11 = str(nm.diag[i1]) + '\n' + ku + str( dimax1)
    d22 = str(nm.diag[i2]) + '\n' + ku + str( dimax2)
    d33 = str(nm.diag[i3]) + '\n' + ku + str( dimax3)

    d1.insert(CURRENT, d11)
    d2.insert(CURRENT, d22)
    d3.insert(CURRENT, d33)

    # Перерисовка картинок
    for i in range(1, nm.lslLen):
        cbtn = Button(framel, bg='#ffaaf0', height=15, bitmap='warning', width=20)
        cbtn.grid(row=i + 1, column=0)
        color = varColor[0] if nm.sii[i - 1, i1] == 1 else 'white'
        cbtn.config(bg=color)

        cbtn = Button(framel, bg='#ffaaf0', height=15, bitmap='warning', width=20)
        cbtn.grid(row=i + 1, column=1)
        color = varColor[1] if nm.sii[i - 1, i2] == 1 else 'white'
        cbtn.config(bg=color)

        cbtn = Button(framel, bg='#ffaaf0', height=15, bitmap='warning', width=20)
        cbtn.grid(row=i + 1, column=2)
        color = varColor[2] if nm.sii[i - 1, i3] == 1 else 'white'
        cbtn.config(bg=color)
    return


# ================ ОСНОВНАЯ ПРОГА
class HouseApp(App):
    def __init__(self, *args):
        super(HouseApp, self).__init__(*args)

    def main(self):
        verticalContainer = gui.Widget(width=540, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px',
                                         style={'display': 'block', 'overflow': 'auto'})

        framel = gui.Widget(width=320, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        framec = gui.Widget(width=320, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        framer = gui.Widget(width=320, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        bpu = 2
        color = 'grey55' if bpu % 2 else 'khaki'
        t = {}
        button = {}
        ss = {}
        cbtn = [[0 for x in range(nm.lslLen)] for x in range(3)]

        # ============ ЛЕВО   подсвечивание симптоматики цветные квадратики ,cursor='heart',bg='white',relief=RAISED
        # Цикл кнопок
        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px',
                                         style={'display': 'block', 'overflow': 'auto'})

        for i in range(0, nm.lslLen):
            for j in range(0, 3):
                if i == 0:
                    label = gui.Label(j)
                    framel.append(label)
                else:
                    cbtn = gui.Button(width=20, height=15)
                    framel.append(cbtn)

        horizontalContainer.append(framel)
        horizontalContainer.append(framec)
        horizontalContainer.append(framer)

        verticalContainer.append(horizontalContainer)

        return verticalContainer

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)

    start(HouseApp, debug=True, address='0.0.0.0', start_browser=True)
