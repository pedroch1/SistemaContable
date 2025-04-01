import mysql.connector
from ..config import DB_CONFIG
from datetime import datetime, timedelta
class Impuesto:
    def __init__(self, id=None, nombre=None, porcentaje=None, descripcion=None, 
                 fecha_vencimiento=None, periodicidad=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.porcentaje = porcentaje
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.periodicidad = periodicidad  # mensual, trimestral, anual
        self.activo = activo

    @staticmethod
    def get_conexion():
        return mysql.connector.connect(**DB_CONFIG)

    def guardar(self):
        conn = self.get_conexion()
        cursor = conn.cursor()
        
        if self.id:
            # Actualizar
            query = """
            UPDATE impuestos 
            SET nombre = %s, porcentaje = %s, descripcion = %s, 
                fecha_vencimiento = %s, periodicidad = %s, activo = %s
            WHERE id = %s
            """
            cursor.execute(query, (
                self.nombre, self.porcentaje, self.descripcion,
                self.fecha_vencimiento, self.periodicidad, self.activo, self.id
            ))
        else:
            # Insertar
            query = """
            INSERT INTO impuestos 
            (nombre, porcentaje, descripcion, fecha_vencimiento, periodicidad, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.nombre, self.porcentaje, self.descripcion,
                self.fecha_vencimiento, self.periodicidad, self.activo
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return self.id

    @classmethod
    def listar_proximos_vencimientos(cls, dias=30):
        """Lista impuestos que vencen en los próximos días"""
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        hoy = datetime.now()
        fecha_limite = hoy + timedelta(days=dias)
        
        query = """
        SELECT * FROM impuestos 
        WHERE activo = 1 AND fecha_vencimiento BETWEEN %s AND %s
        ORDER BY fecha_vencimiento
        """
        
        cursor.execute(query, (hoy, fecha_limite))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [cls(**data) for data in results]