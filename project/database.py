import mysql.connector
from pydantic import BaseModel
from typing import List, Optional
from contextlib import contextmanager
from typing import Generator

# Configuración de la conexión a la base de datos
db_connection_params = {
    "host": "devops0001.mysql.database.azure.com",
    "user": "devops",
    "password": "#braian987",
    "database": "devops"
}

# Definición de los modelos
class Modulo(BaseModel):
    id: Optional[int] = None
    nombre: str
    duracion: int
    nivel: str

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    precio: float
    duracion: int

# Contexto para la conexión a la base de datos
@contextmanager
def db_connection() -> Generator:
    connection = None
    try:
        connection = mysql.connector.connect(**db_connection_params)
        cursor = connection.cursor()
        yield connection, cursor
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

# Funciones para gestionar módulos

def create_modulo_table():
    with db_connection() as (connection, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modulos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                duracion INT,
                nivel VARCHAR(255)
            )
        ''')
        connection.commit()

def insert_modulo(modulo: Modulo):
    with db_connection() as (connection, cursor):
        query = "INSERT INTO modulos (nombre, duracion, nivel) VALUES (%s, %s, %s)"
        values = (modulo.nombre, modulo.duracion, modulo.nivel)
        cursor.execute(query, values)
        connection.commit()

def get_all_modulos() -> List[Modulo]:
    with db_connection() as (connection, cursor):
        cursor.execute("SELECT id, nombre, duracion, nivel FROM modulos")
        modulos = []
        for row in cursor.fetchall():
            modulo = Modulo(id=row[0], nombre=row[1], duracion=row[2], nivel=row[3])
            modulos.append(modulo)
        return modulos

def update_modulo(id: int, modulo: Modulo):
    with db_connection() as (connection, cursor):
        query = "UPDATE modulos SET nombre = %s, duracion = %s, nivel = %s WHERE id = %s"
        values = (modulo.nombre, modulo.duracion, modulo.nivel, id)
        cursor.execute(query, values)
        connection.commit()

def delete_modulo(id: int):
    with db_connection() as (connection, cursor):
        query = "DELETE FROM modulos WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        connection.commit()

# Funciones para gestionar cursos

def create_curso_table():
    with db_connection() as (connection, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                descripcion TEXT,
                precio FLOAT,
                duracion INT
            )
        ''')
        connection.commit()

def insert_curso(curso: Curso):
    with db_connection() as (connection, cursor):
        query = "INSERT INTO cursos (titulo, descripcion, precio, duracion) VALUES (%s, %s, %s, %s)"
        values = (curso.titulo, curso.descripcion, curso.precio, curso.duracion)
        cursor.execute(query, values)
        connection.commit()

def get_all_cursos() -> List[Curso]:
    with db_connection() as (connection, cursor):
        cursor.execute("SELECT id, titulo, descripcion, precio, duracion FROM cursos")
        cursos = []
        for row in cursor.fetchall():
            curso = Curso(id=row[0], titulo=row[1], descripcion=row[2], precio=row[3], duracion=row[4])
            cursos.append(curso)
        return cursos

def update_curso(id: int, curso: Curso):
    with db_connection() as (connection, cursor):
        query = """
            UPDATE cursos 
            SET titulo = %s, descripcion = %s, precio = %s, duracion = %s 
            WHERE id = %s
        """
        values = (curso.titulo, curso.descripcion, curso.precio, curso.duracion, id)
        cursor.execute(query, values)
        connection.commit()