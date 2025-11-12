#IMPORTACIONES
import sqlite3
from pydantic import BaseModel
from typing import List

#conexion a una base de datos
NOMBRE_BASEDATOS="ranking.bd"
FUENTE_DATOS="fifa_ranking.json"

#modelo de datos (tabla)
#USAR CLASES que configuren la tabla
class Ranking(BaseModel):
    rango:int
    pais:str
    puntos:str

class CuerpoRanking(BaseModel):
    items:List[Ranking]

#operaciones o servicios que voy a exponer en el front

#Abrir conexion a bd
def crear_conexion():
    return sqlite3.connect(NOMBRE_BASEDATOS)
#Crear tabla que almacena el ranking si no existe
def crear_tabla():
    conexion=crear_conexion()
    cursor=conexion.cursor()
    cursor.execute("""
                    CREATE TABLA IF NOT EXISTS ranking_fifa(
                        rango INTEGER PRIMARY KEY,
                        pais TEXT NOT NULL,
                        puntos TEXT NOT NULL
                    )
                    """)
    conexion.commit()
    conexion.close()
    
#Modificar el ranking
def modificar_ranking(lista:List[Ranking]):
    conexion=crear_conexion()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM ranking_fifa")
    cursor.executemany(
        "INSERT INTO ranking_fifa (rango, pais, puntos) VALUES (?, ?, ?)",
        [(elementoDeLaLista.rango,elementoDeLaLista.pais,elementoDeLaLista.puntos)for elementoDeLaLista in lista]
    )
    # for item in lista:
    #     cursor.execute("INSERT INTO ranking_fifa (rango, pais, puntos) VALUES (?, ?, ?)",
    #                     (item.rango, item.pais, item.puntos))
    conexion.commit()
    conexion.close()

#Leer el ranking
def leer_ranking()->List[Ranking]:
    conexion=crear_conexion()
    cursor=conexion.cursor()
    cursor.execute("SELECT rango, pais, puntos FROM ranking_fifa ORDER BY rango ASC")
    filas=cursor.fetchall()
    conexion.close()
    return [{"rango":rango,"pais":pais,"puntos":puntos} for (rango, pais, puntos) in filas]

#construir los endpoinds