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
from DISClib.ADT import orderedmap as om
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Inicializa el analizador.
    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'dateIndex': None}

    analyzer['ufos'] = lt.newList('SINGLE_LINKED')

    # -----------------------------------------------------
    # Se crean indices (Maps) por los siguientes criterios:
    # -----------------------------------------------------

    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare)

    return analyzer


# Funciones para agregar informacion al catalogo


def addUFO(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)

    return analyzer


# Funciones para creacion de datos

# Funciones de consulta

# Funciones de comparación


def compare():
    pass


# Funciones de ordenamiento
