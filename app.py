

from flask import Flask, Response

from flask import request, render_template

import random
import sys
import os
app = Flask(__name__)
size = 8


@app.route('/juego')
def hello_world():
    turno = request.args.get('turno')

    estado = request.args.get('estado')

    result = iniciar(turno, estado)
    
    
    return result


def obtenerTablero(estado):
    tablero = []
    for i in range(size):
        tablero.append([' '] * size)
    cont = 0
    for i in range(8):
        for j in range(8):
            if estado[cont] == '2':
                tablero[i][j] = ' '
            else:
                tablero[i][j] = estado[cont]

            cont += 1

    return tablero


def estaEnTablero(x, y):

    return x >= 0 and x < size and y >= 0 and y < size


def esJugadaValida(tablero, baldosa, comienzox, comienzoy):

    if tablero[comienzox][comienzoy] != ' ' or not estaEnTablero(comienzox, comienzoy):
        return False

    tablero[comienzox][comienzoy] = baldosa

    if baldosa == '1':
        otraBaldosa = '0'
    else:
        otraBaldosa = '1'

    baldosasAConvertir = []
    for direcciónx, direccióny in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = comienzox, comienzoy
        x += direcciónx
        y += direccióny
        if estaEnTablero(x, y) and tablero[x][y] == otraBaldosa:

            x += direcciónx
            y += direccióny
            if not estaEnTablero(x, y):
                continue
            while tablero[x][y] == otraBaldosa:
                x += direcciónx
                y += direccióny
                if not estaEnTablero(x, y):
                    break
            if not estaEnTablero(x, y):
                continue
            if tablero[x][y] == baldosa:

                while True:
                    x -= direcciónx
                    y -= direccióny
                    if x == comienzox and y == comienzoy:
                        break
                    baldosasAConvertir.append([x, y])

    tablero[comienzox][comienzoy] = ' '
    if len(baldosasAConvertir) == 0:
        return False
    return baldosasAConvertir


def obtenerJugadasValidas(tablero, baldosa):

    jugadasValidas = []

    for x in range(size):
        for y in range(size):
            if esJugadaValida(tablero, baldosa, x, y) != False:
                jugadasValidas.append([x, y])
    return jugadasValidas


def esEsquina(x, y):

    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def obtenerNuevoTablero():

    tablero = []
    for i in range(size):
        tablero.append([' '] * size)

    return tablero


def obtenerCopiaTablero(tablero):

    replicaTablero = obtenerNuevoTablero()

    for x in range(size):
        for y in range(size):
            replicaTablero[x][y] = tablero[x][y]

    return replicaTablero


def hacerJugada(tablero, baldosa, comienzox, comienzoy):

    baldosasAConvertir = esJugadaValida(tablero, baldosa, comienzox, comienzoy)

    if baldosasAConvertir == False:
        return False

    tablero[comienzox][comienzoy] = baldosa
    for x, y in baldosasAConvertir:
        tablero[x][y] = baldosa
    return True


def obtenerPuntajeTablero(tablero):

    puntajex = 0
    puntajeo = 0
    for x in range(size):
        for y in range(size):
            if tablero[x][y] == '1':
                puntajex += 1
            if tablero[x][y] == '0':
                puntajeo += 1
    return {'1': puntajex, '0': puntajeo}


def obtenerJugadaComputadora(tablero, baldosaComputadora):

    jugadasPosibles = obtenerJugadasValidas(tablero, baldosaComputadora)

    random.shuffle(jugadasPosibles)

    for x, y in jugadasPosibles:
        if esEsquina(x, y):
            return [x, y]

    mejorPuntaje = -1
    for x, y in jugadasPosibles:
        print("entro al for")
        replicaTablero = obtenerCopiaTablero(tablero)
        hacerJugada(replicaTablero, baldosaComputadora, x, y)
        puntaje = obtenerPuntajeTablero(replicaTablero)[baldosaComputadora]
        if puntaje > mejorPuntaje:
            print("entro al if del for")
            mejorJugada = [x, y]
            mejorPuntaje = puntaje
    return mejorJugada


def iniciar(turno, estado):
    tableroPrincipal = obtenerTablero(estado)
    if turno == '1':
        print('es uno')
        otraBaldosa = '0'
        x, y = obtenerJugadaComputadora(tableroPrincipal, '1')
    else:
        otraBaldosa = '1'
        x, y = obtenerJugadaComputadora(tableroPrincipal, '0')
    return str(x) + str(y)
