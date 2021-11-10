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
 """


import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del catálogo


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analyzer = model.newAnalyzer()

    return analyzer


# Funciones para la carga de datos


def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + 'UFOS/UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")

    for ufo in input_file:
        model.addUFO(analyzer, ufo)

    return analyzer


# Funciones de ordenamiento


# Funciones de consulta sobre el catálogo

def getSightingsByCity(analyzer, city):
    return model.getCitySightings(analyzer, city)


def getDuration(analyzer, min_key, max_key):
    return model.getDuration(analyzer, min_key, max_key)


def getSightingsByTime(analyzer, minTime, maxTime):
    return model.getSightingsByTime(analyzer, minTime, maxTime)


def getSightingsByDate(analyzer, minDate, maxDate):
    return model.getSightingsByDate(analyzer, minDate, maxDate)


def getSightingsByCoordinates(analyzer, minLon, maxLon, minLat, maxLat):
    return model.getSightingsByCoordinates(analyzer, minLon, maxLon, minLat,
                                           maxLat)
