﻿"""
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
from datetime import datetime
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Inicializa el analizador.
    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'cityIndex': None}

    analyzer['ufos'] = lt.newList('ARRAY_LIST')

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
    {key: 'city', value:{'count': count, 'DateTime': RBT}}
    """
    city = ufo['city']
    # date = ufo['datetime']
    cityIndex = analyzer['cityIndex']
    ispresent = mp.contains(cityIndex, city)

    if ispresent:
        pass
    else:
        dateTime = om.newMap(omaptype='RBT',
                             comparefunction=cmpDates)
        count = 0
        data = {'count': count, 'DateTime': dateTime}
        mp.put(cityIndex, city, data)

    entry = mp.get(cityIndex, city)
    value = me.getValue(entry)
    addDateTime(value['DateTime'], ufo)

    """
    pair = om.get(value['DateTime'], date)
    arrayList = me.valueSet(pair)

    size = 0
    for element in lt.iterator(arrayList):
        size += lt.size(element)

    value['count'] = size
    """


def addDateTime(map, ufo):
    """
    Esta función crea la siguiente estructura de datos Map Ordered:
    {key: datetime, value: [ufos]}
    """
    dateTime = ufo['datetime']
    ispresent = om.contains(map, dateTime)

    if ispresent:
        pass
    else:
        sightings = lt.newList('ARRAY_LIST')
        om.put(map, dateTime, sightings)

    entry = om.get(map, dateTime)
    arrayList = me.getValue(entry)
    lt.addLast(arrayList, ufo)


# Funciones de consulta


# Funciones de comparación


def cmpDates(ufo1, ufo2):
    """
    Esta función compara dos fechas.
    """
    date1 = ufo1['datetime']
    date2 = ufo2['datetime']

    datetime1 = datetime.fromisoformat(date1)
    datetime2 = datetime.fromisoformat(date2)

    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


def cmpDuration(ufo1, ufo2):
    """
    Esta función compara dos duraciones.
    """
    duration1 = ufo1['duration (seconds)']
    duration2 = ufo2['duration (seconds)']

    if duration1 == duration2:
        return 0
    elif duration1 > duration2:
        return 1
    else:
        return -1


# Funciones de ordenamiento
