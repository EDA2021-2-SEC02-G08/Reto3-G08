"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
import sys
import controller
from datetime import time
from datetime import datetime
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada...
"""


# Funciones de impresión


def printUFO(ufo):
    print('Fecha y hora: ' + ufo['datetime'] +
          '. Ciudad: ' + ufo['city'] +
          '. País: ' + ufo['country'] +
          '. Duración (segundos): ' + ufo['duration (seconds)'] +
          '. Forma del objeto: ' + ufo['shape'])


def printFirstAndLast(lst):
    i = 1
    while i <= 3:
        ufo = lt.getElement(lst, i)
        printUFO(ufo)
        i += 1

    i = -2
    while i <= 0:
        ufo = lt.getElement(lst, i)
        printUFO(ufo)
        i += 1


def printDuration(analyzer, result):
    """
    Esta función imprime el requerimiento 2.
    """
    durationIndex = analyzer['durationIndex']
    size = om.size(durationIndex)
    print('\nHay un total de ' + str(size) +
          ' diferentes duraciones de avistamientos UFO')
    # -----------------------------------------------------------
    max_key = om.maxKey(durationIndex)
    entry = om.get(durationIndex, max_key)
    value = me.getValue(entry)
    print('\nEl avistamiento UFO más largo es: ' +
          '\nDuración (segundos): ' + str(max_key) +
          '. Contador: ' + str(value['count']))
    # -----------------------------------------------------------
    print('\nHay un total de ' + str(result[1]) +
          ' avistamientos en este rango de duraciones')
    # -----------------------------------------------------------
    print('\nLos primero y ultimos tres avistamientos en este rango son: ')
    ufos = result[0]

    printFirstAndLast(ufos)


def printMenu():
    print("\nBienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información de avistamientos")
    print("3- Consultar los avistamientos en una ciudad")
    print("4- Consultar los avistamientos por duración")
    print("5- Consultar avistamientos por hora / minutos del día")
    print("6- Consultar los avistamientos en un rango de fechas")
    print("7- Consultar los avistamientos de una zona geográfica")


"""
Menu principal
"""


while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("\nInicializando....")
        analyzer = controller.init()

    elif inputs == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(analyzer)

    elif inputs == 3:
        city = str(input('\nIngrese la ciudad: '))
        result = controller.getSightingsByCity(analyzer, city)
        found = result[0]
        total = result[1]
        print('\nHay ' + str(total) +
              ' ciudades donde se han reportado avistamientos.')
        if found:
            N_sighthings = result[2]
            ufos = result[3]
            print('Se han reportado ' + str(N_sighthings) +
                  ' avistamientos en ' + city + '.')
            printFirstAndLast(ufos)
        else:
            print('No se encontró la ciudad ' + city + '.')

    elif inputs == 4:
        min_key = float(input('\nIngrese el límite inferior: '))
        max_key = float(input('Ingrese el límite superior: '))
        result = controller.getDuration(analyzer, min_key, max_key)
        printDuration(analyzer, result)

    elif inputs == 5:
        minTime = str(input('\nIngrese el límite inferior (HH:MM): '))
        maxTime = str(input('\nIngrese el límite superior (HH:MM): '))
        minTime = time.fromisoformat(minTime)
        maxTime = time.fromisoformat(maxTime)
        result = controller.getSightingsByTime(analyzer, minTime, maxTime)
        print('La hora más tardía en la que se registró un avistamiento es:')
        print(result[0], 'con ' + str(result[1]) + ' avistamientos.')
        printFirstAndLast(result[2])

    elif inputs == 6:
        minDate = str(input('\nIngrese el límite inferior (AAAA-MM-DD): '))
        maxDate = str(input('\nIngrese el límite superior (AAAA-MM-DD): '))
        minDate + ' 00:00'
        maxDate + ' 23:59'
        minDate = datetime.fromisoformat(minDate)
        maxDate = datetime.fromisoformat(maxDate)
        result = controller.getSightingsByDate(analyzer, minDate, maxDate)
        print('La fecha más antigua en la que se registró un avistamiento es:')
        print(result[0], 'con ' + str(result[1]) + ' avistamientos.')
        printFirstAndLast(result[2])

    elif inputs == 7:
        pass

    else:
        sys.exit(0)

sys.exit(0)
