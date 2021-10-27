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
# from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mg
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
    {key: 'city', value:{'count': count, 'ufos': [ufos]}}
    """
    city = ufo['city']
    cityIndex = analyzer['cityIndex']
    city_exists = mp.contains(cityIndex, city)

    if city_exists:
        pass
    else:
        arrayList = lt.newList('ARRAY_LIST')
        count = 0
        data = {'count': count, 'ufos': arrayList}
        mp.put(cityIndex, city, data)

    pair = mp.get(cityIndex, city)
    value = me.getValue(pair)
    lt.addLast(value['ufos'], ufo)
    value['count'] = lt.size(value['ufos'])


# Funciones de consulta


def rankingCity(analyzer):
    cityIndex = analyzer['cityIndex']
    cities = mp.valueSet(cityIndex)
    sortCity(cities)

    return cities


# Funciones de comparación


def cmpCity(city1, city2):
    return city1['count'] > city2['count']


def cmpDate(date1, date2):
    pass


# Funciones de ordenamiento


def sortCity(list):
    mg.sort(list, cmpCity)


def sortDate(list):
    mg.sort(list, cmpDate)
