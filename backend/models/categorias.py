import mysql.connector
from ..config import DB_CONFIG

class Categoria:
    def __init__(self, id=None, nombre=None, tipo=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # 'ingreso', 'gasto'
        self.descripcion = descripcion

    @staticmethod
    def get_conexion():
        return mysql.connector.connect(**DB_CONFIG)

    def guardar(self):
        conn = self.get_conexion()
        cursor = conn.cursor()
        
        if self.id:
            # Actualizar categoría existente
            query = """
            UPDATE categorias 
            SET nombre = %s, tipo = %s, descripcion = %s
            WHERE id = %s
            """
            cursor.execute(query, (self.nombre, self.tipo, self.descripcion, self.id))
        else:
            # Insertar nueva categoría
            query = """
            INSERT INTO categorias 
            (nombre, tipo, descripcion)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.nombre, self.tipo, self.descripcion))
            self.id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return self.id

    @classmethod
    def obtener_por_id(cls, id):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM categorias WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return cls(**result)
        return None

    @classmethod
    def listar(cls, tipo=None):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM categorias"
        params = []
        
        if tipo:
            query += " WHERE tipo = %s"
            params.append(tipo)
        
        query += " ORDER BY nombre"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [cls(**data) for data in results]