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
# from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
import sys
import controller
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Funciones de impresión


def rankingCity(analyzer, ranking, city):
    size = lt.size(ranking)
    cityIndex = analyzer['cityIndex']
    pair = mp.get(cityIndex, city)
    value = me.getValue(pair)
    print('Hay un total de ' + str(size) +
          ' diferentes ciudades con avistamientos UFO\n')
    print('El TOP 5 de ciudades con más avistamientos UFO son:')

    i = 1
    while i <= 5:
        data = lt.getElement(ranking, i)
        print(data['ufos']['elements'][0]['city'] + ' - ' + str(data['count']))
        i += 1

    print('\nHay un total de ' + str(lt.size(value['ufos'])) + ' en: ' +
          str(city))
    print('Los primeros tres y últimos tres en esta ciudad son: ')


ufosfile = 'UFOS//UFOS-utf8-small.csv'
controlador = None


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Contar los avistamientos en una ciudad")
    print("4- Contar los avistamientos por duración")
    print("5- Contar avistamientos por hora / minutos del día")
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una zona geográfica")


catalog = None


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
        controller.loadData(analyzer, ufosfile)

    elif inputs == 3:
        city = str(input('Ingrese la ciudad: '))
        ranking = controller.rankingCity(analyzer)
        rankingCity(analyzer, ranking, city)

    else:
        sys.exit(0)

sys.exit(0)
