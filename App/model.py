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
                'dateIndex': None,
                'longitudeIndex': None}

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

    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpDates)

    analyzer['longitudeIndex'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmpCoordinates)

    return analyzer


# Funciones para agregar informacion al catalogo


def addUFO(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    addCity(analyzer, ufo)
    addDuration(analyzer, ufo)
    addTime(analyzer, ufo)
    addDateTime(analyzer['dateIndex'], ufo)
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
        lst = lt.newList('ARRAY_LIST')
        count = 0
        data = {'count': count, 'ufos': lst, 'DateTime': dateTime}
        mp.put(cityIndex, city, data)

    entry = mp.get(cityIndex, city)
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
        ufos = lt.newList('ARRAY_LIST')
        om.put(timeIndex, time, ufos)

    entry = om.get(timeIndex, time)
    ufos = me.getValue(entry)
    lt.addLast(ufos, ufo)
    sortDates(ufos)


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
        latitudeMap = om.newMap(omaptype='RBT', )
        om.put(longitudeIndex, longitude, latitudeMap)

    entry = om.get(longitudeIndex, longitude)
    latitudeMap = me.getValue(entry)
    addLatitude(latitudeMap, ufo)


def addLatitude(map, ufo):
    latitude = ufo['latitude']
    latitude = round(float(latitude), 2)
    ispresent = om.contains(map, latitude)

    if ispresent:
        pass
    else:
        sightings = lt.newList('ARRAY_LIST')
        om.put(map, latitude, sightings)

    entry = om.get(map, latitude)
    lst = me.getValue(entry)
    lt.addLast(lst, ufo)


# Funciones de consulta


def getCitySightings(analyzer, city):
    """
    Retorna el número total de ciudades con avistamientos, el total de
    avistamientos en city y los avistamientos en city
    ordenados cronológicamente
    """
    cityIndex = analyzer['cityIndex']
    N_cities = lt.size(mp.keySet(cityIndex))
    pair = mp.get(cityIndex, city)
    if pair is not None:
        data = me.getValue(pair)
        lst = om.valueSet(data['DateTime'])
        ufos = lt.newList('ARRAY_LIST')
        for it in lt.iterator(lst):
            for ufo in lt.iterator(it):
                lt.addLast(ufos, ufo)
        return True, N_cities, data['count'], ufos
    else:
        return False, N_cities


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


def getSightingsByTime(analyzer, minHM, maxHM):
    timeIndex = analyzer['timeIndex']
    maxTime = om.maxKey(timeIndex)
    entry = om.get(timeIndex, maxTime)
    MaxTimeUFOs = me.getValue(entry)
    N_MaxTime = lt.size(MaxTimeUFOs)

    values = om.values(timeIndex, minHM, maxHM)
    ufos = lt.newList('ARRAY_LIST')
    for lst in lt.iterator(values):
        for ufo in lt.iterator(lst):
            lt.addLast(ufos, ufo)

    return maxTime, N_MaxTime, ufos


def getSightingsByDate(analyzer, minDate, maxDate):
    dateIndex = analyzer['dateIndex']
    oldDate = om.minKey(dateIndex)
    entry = om.get(dateIndex, oldDate)
    ufos = me.getValue(entry)
    N_oldDate = lt.size(ufos)

    values = om.values(dateIndex, minDate, maxDate)
    ufos = lt.newList('ARRAY_LIST')
    for lst in lt.iterator(values):
        for ufo in lt.iterator(lst):
            lt.addLast(ufos, ufo)

    return oldDate.date(), N_oldDate, ufos


def getSightingsByCoordinates(analyzer, minLon, maxLon, minLat, maxLat):
    lonIndex = analyzer['longitudeIndex']
    values = om.values(lonIndex, minLon, maxLon)
    ufos = lt.newList('ARRAY_LIST')

    for latMap in lt.iterator(values):
        values2 = om.values(latMap, minLat, maxLat)
        for lst in lt.iterator(values2):
            for ufo in lt.iterator(lst):
                lt.addLast(ufos, ufo)

    return ufos


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


def cmpTimes(time1, time2):
    """
    Esta función compara dos llaves de fechas.
    """
    if time1 == time2:
        return 0
    elif time1 > time2:
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


def cmpCoordinates(coord1, coord2):
    """
    Esta función compara dos llaves de longitudes.
    """
    if coord1 == coord2:
        return 0
    elif coord1 < coord2:
        return 1
    else:
        return -1


def compareDates(ufo1, ufo2):
    """
    Compara las fechas de dos avistamientos.
    """
    date1 = datetime.fromisoformat(ufo1['datetime'])
    date2 = datetime.fromisoformat(ufo2['datetime'])
    return date1 < date2

# Funciones de ordenamiento


def sortDates(lst):
    mg.sort(lst, compareDates)
