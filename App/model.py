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
from datetime import datetime
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Inicializa el analizador.
    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'cityIndex': None,
                'durationIndex': None,
                'timeIndex': None,
                'longitudeIndex': None
                }

    analyzer['ufos'] = lt.newList('ARRAY_LIST')

    # -----------------------------------------------------
    # Se crean indices (Maps) por los siguientes criterios:
    # -----------------------------------------------------

    analyzer['cityIndex'] = mp.newMap(2000,
                                      maptype='PROBING',
                                      loadfactor=0.75)

    analyzer['durationIndex'] = om.newMap(omaptype='RBT',
                                          comparefunction=cmpDurations)

    analyzer['timeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpTimes)

    analyzer['longitudeIndex'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmpLongitudes)

    return analyzer


# Funciones para agregar informacion al catalogo


def addUFO(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    addCity(analyzer, ufo)
    addDuration(analyzer, ufo)
    addTime(analyzer, ufo)
    addLongitude(analyzer, ufo)

    return analyzer


# Funciones para creacion de datos


def addCity(analyzer, ufo):
    """
    Esta función crea la siguiente estructura de datos por ciudad:
    {key: 'city', value:{'count': count, 'DateTime': RBT}}
    """
    city = ufo['city']
    cityIndex = analyzer['cityIndex']
    ispresent = mp.contains(cityIndex, city)

    if ispresent:
        pass
    else:
        dateTime = om.newMap(omaptype='RBT',
                             comparefunction=cmpDates)
        lst = lt.newList('SINGLE_LINKED')
        count = 0
        data = {'count': count, 'ufos': lst, 'DateTime': dateTime}
        mp.put(cityIndex, city, data)

    entry = om.get(cityIndex, city)
    value = me.getValue(entry)
    addDateTime(value['DateTime'], ufo)
    lt.addLast(value['ufos'], ufo)
    value['count'] = lt.size(value['ufos'])


def addDateTime(map, ufo):
    """
    Esta función crea la siguiente estructura de datos Map Ordered:
    {key: datetime, value: [ufos]}
    """
    dateTime = ufo['datetime']
    dateTime = datetime.fromisoformat(dateTime)
    ispresent = om.contains(map, dateTime)

    if ispresent:
        pass
    else:
        sightings = lt.newList('ARRAY_LIST')
        om.put(map, dateTime, sightings)

    entry = om.get(map, dateTime)
    arrayList = me.getValue(entry)
    lt.addLast(arrayList, ufo)


def addDuration(analyzer, ufo):
    """
    Esta función crea la siguiente estructura de datos Map Ordered:
    {key: duration, value: {count: count, ufos: [ufos]}
    """
    durationIndex = analyzer['durationIndex']
    duration = float(ufo['duration (seconds)'])
    ispresent = om.contains(durationIndex, duration)

    if ispresent:
        pass
    else:
        sightings = lt.newList('ARRAY_LIST')
        count = 0
        data = {'count': count, 'ufos': sightings}
        om.put(durationIndex, duration, data)

    entry = om.get(durationIndex, duration)
    value = me.getValue(entry)
    lt.addLast(value['ufos'], ufo)
    count = lt.size(value['ufos'])
    value['count'] = count


def addTime(analyzer, ufo):
    timeIndex = analyzer['timeIndex']
    time = datetime.fromisoformat(ufo['datetime']).time()
    ispresent = om.contains(timeIndex, time)

    if ispresent:
        pass
    else:
        dates = om.newMap(omaptype='RBT',
                          comparefunction=cmpDates)
        om.put(timeIndex, time, dates)

    entry = om.get(timeIndex, time)
    dates = me.getValue(entry)
    addDateTime(dates, ufo)


def addLongitude(analyzer, ufo):
    """
    Esta función crea la siguiente estructura de datos Map Ordered:
    {key: longitude, value: [ufos]}
    """
    longitudeIndex = analyzer['longitudeIndex']
    longitude = round(float(ufo['longitude']), 2)
    ispresent = om.contains(longitudeIndex, longitude)

    if ispresent:
        pass
    else:
        sightings = lt.newList('ARRAY_LIST')
        om.put(longitudeIndex, longitude, sightings)

    entry = om.get(longitudeIndex, longitude)
    arrayList = me.getValue(entry)
    lt.addLast(arrayList, ufo)
    sortLatitude(arrayList)


# Funciones de consulta


def getDuration(analyzer, min_key, max_key):
    """
    Retorna los avistamientos en un rango de duración.
    Retorna el total de avistamientos en este rango.
    """
    durationIndex = analyzer['durationIndex']
    values = om.values(durationIndex, min_key, max_key)
    arrayList = lt.newList('ARRAY_LIST')
    size = 0

    for element in lt.iterator(values):
        size += element['count']
        element = element['ufos']
        for sub_element in lt.iterator(element):
            lt.addLast(arrayList, sub_element)

    return arrayList, size


# Funciones de comparación


def cmpDates(datetime1, datetime2):
    """
    Esta función compara dos llaves de fechas.
    """
    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


def cmpTimes(datetime1, datetime2):
    """
    Esta función compara dos llaves de fechas.
    """
    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


def cmpDurations(duration1, duration2):
    """
    Esta función compara dos llaves de duraciones.
    """
    if duration1 == duration2:
        return 0
    elif duration1 > duration2:
        return 1
    else:
        return -1


def cmpLongitudes(longitude1, longitude2):
    """
    Esta función compara dos llaves de longitudes.
    """
    if longitude1 == longitude2:
        return 0
    elif longitude1 > longitude2:
        return 1
    else:
        return -1


def cmpLatitudes(ufo1, ufo2):
    """
    Esta función compara dos latitudes para ordenarlas.
    """
    latitude1 = round(float(ufo1['latitude']), 2)
    latitude2 = round(float(ufo2['latitude']), 2)

    return latitude1 > latitude2


# Funciones de ordenamiento


def sortLatitude(arrayList):
    mg.sort(arrayList, cmpLatitudes)
