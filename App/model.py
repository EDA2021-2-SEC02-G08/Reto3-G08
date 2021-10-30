"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mg
import datetime
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Inicializa el analizador.
    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'cityIndex': None}

    analyzer['ufos'] = lt.newList('SINGLE_LINKED')

    # -----------------------------------------------------
    # Se crean indices (Maps) por los siguientes criterios:
    # -----------------------------------------------------

    analyzer['cityIndex'] = mp.newMap(2000,
                                      maptype='PROBING',
                                      loadfactor=0.75)

    return analyzer


# Funciones para agregar informacion al catalogo


def addUFO(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    addCity(analyzer, ufo)

    return analyzer


# Funciones para creacion de datos


def addCity(analyzer, ufo):
    """
    Esta función crea la siguiente estructura de datos por ciudad:
    {key: 'city', value:{'count': count, 'DateTime': BTS}}
    """
    city = ufo['city']
    date = ufo['datetime']
    cityIndex = analyzer['cityIndex']
    city_exists = mp.contains(cityIndex, city)

    if city_exists:
        pass
    else:
        dateTime = om.newMap(omaptype='RBT',
                             comparefunction=cmpDates)
        count = 0
        data = {'count': count, 'DateTime': dateTime}
        mp.put(cityIndex, city, data)

    pair = mp.get(cityIndex, city)
    value = me.getValue(pair)
    addDateTime(value['DateTime'], ufo)

    pair = om.get(value['DateTime'], date)
    arrayList = me.valueSet(pair)

    size = 0
    for element in lt.iterator(arrayList):
        size += lt.size(element)

    value['count'] = size


def addDateTime(map, UFO):
    """
    {key: date, value: [ufos]}
    """
    date_time = UFO['datetime']
    DateTime = datetime.fromisoformat(date_time)
    entry = om.get(map, DateTime)
    if entry is None:
        sightings = lt.newList('SINGLE_LINKED')
        om.put(map, DateTime, sightings)
        entry = om.get(map, DateTime)
        dateentry = me.getValue(entry)
    else:
        dateentry = me.getValue(entry)
    lt.addLast(dateentry, UFO)


# Funciones de consulta


"""
def getCitySightings(analyzer, city):
    cityIndex = analyzer['cityIndex']
    N_cities = lt.size(mp.keySet(cityIndex))
    pair = mp.get(cityIndex, city)
    if pair is not None:
        data = me.getValue(pair)
        sortDate(data['ufos'])
        return True, N_cities, data['count'], data['ufos']
    else:
        return False, N_cities
"""


# Funciones de comparación


def cmpCity(city1, city2):
    return city1['count'] > city2['count']


def cmpDates(datetime1, datetime2):
    """
    Compara dos fechas
    """
    date1 = datetime1['datetime']
    date2 = datetime2['datetime']

    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


# Funciones de ordenamiento


def sortCity(list):
    mg.sort(list, cmpCity)


"""
def sortDate(list):
    mg.sort(list, cmpDate)
"""
