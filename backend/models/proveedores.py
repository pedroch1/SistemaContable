import mysql.connector
from ..config import DB_CONFIG
from datetime import datetime

class Proveedor:
    def __init__(self, id=None, nombre=None, rfc=None, direccion=None, 
                 telefono=None, email=None, activo=True, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.rfc = rfc
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.activo = activo
        self.fecha_registro = fecha_registro or datetime.now()

    @staticmethod
    def get_conexion():
        return mysql.connector.connect(**DB_CONFIG)

    def guardar(self):
        conn = self.get_conexion()
        cursor = conn.cursor()
        
        if self.id:
            # Actualizar proveedor existente
            query = """
            UPDATE proveedores 
            SET nombre = %s, rfc = %s, direccion = %s, telefono = %s, 
                email = %s, activo = %s
            WHERE id = %s
            """
            cursor.execute(query, (
                self.nombre, self.rfc, self.direccion, self.telefono,
                self.email, self.activo, self.id
            ))
        else:
            # Insertar nuevo proveedor
            query = """
            INSERT INTO proveedores 
            (nombre, rfc, direccion, telefono, email, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.nombre, self.rfc, self.direccion, self.telefono,
                self.email, self.activo
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return self.id

    @classmethod
    def obtener_por_id(cls, id):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM proveedores WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return cls(**result)
        return None

    @classmethod
    def listar(cls, solo_activos=True):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM proveedores"
        if solo_activos:
            query += " WHERE activo = 1"
        
        query += " ORDER BY nombre"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [cls(**data) for data in results]

    @classmethod
    def eliminar(cls, id):
        conn = cls.get_conexion()
        cursor = conn.cursor()
        
        # En lugar de eliminar físicamente, marcamos como inactivo
        query = "UPDATE proveedores SET activo = 0 WHERE id = %s"
        cursor.execute(query, (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return cursor.rowcount > 0
