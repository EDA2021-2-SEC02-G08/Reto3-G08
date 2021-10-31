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


def printUFO(ufo):
    ufo = ufo['elements'][0]
    print('Fecha y hora: ' + ufo['datetime'] +
          '. Ciudad: ' + ufo['city'] +
          '. País: ' + ufo['country'] +
          '. Duración (segundos): ' + ufo['duration (seconds)'] +
          '. Forma del objeto: ' + ufo['shape'])


def printCitySightings(analyzer, city):
    """
    Esta función imprime el requerimiento 1.
    """
    # ----------------------------------------------------------------------
    cityIndex = analyzer['cityIndex']
    total = lt.size(mp.keySet(cityIndex))
    print('\nHay ' + str(total) +
          ' ciudades donde se han reportado avistamientos.')
    # ----------------------------------------------------------------------
    entry = mp.get(cityIndex, city)
    value = me.getValue(entry)
    print('Se han reportado ' + str(value['count']) + ' avistamientos en ' +
          city + '.')
    # ----------------------------------------------------------------------
    print('\nLos primero y ultimos tres avistamientos en esta ciudad son: ')
    ufos = om.valueSet(value['DateTime'])


ufosfile = 'UFOS//UFOS-utf8-small.csv'
controlador = None


def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información de avistamientos")
    print("3- Consultar los avistamientos en una ciudad")
    print("4- Consultar los avistamientos por duración")
    print("5- Consultar avistamientos por hora / minutos del día")
    print("6- Consultar los avistamientos en un rango de fechas")
    print("7- Consultar los avistamientos de una zona geográfica")


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
        printCitySightings(analyzer, city)

    else:
        sys.exit(0)

sys.exit(0)
