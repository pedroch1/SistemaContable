import mysql.connector
from ..config import DB_CONFIG

class Cuenta:
    def __init__(self, id=None, nombre=None, tipo=None, saldo=0, 
                 moneda='USD', activa=True):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # 'banco', 'efectivo', 'tarjeta', etc.
        self.saldo = saldo
        self.moneda = moneda
        self.activa = activa

    @staticmethod
    def get_conexion():
        return mysql.connector.connect(**DB_CONFIG)

    def guardar(self):
        conn = self.get_conexion()
        cursor = conn.cursor()
        
        if self.id:
            # Actualizar cuenta existente
            query = """
            UPDATE cuentas 
            SET nombre = %s, tipo = %s, saldo = %s, moneda = %s, activa = %s
            WHERE id = %s
            """
            cursor.execute(query, (
                self.nombre, self.tipo, self.saldo, self.moneda, self.activa, self.id
            ))
        else:
            # Insertar nueva cuenta
            query = """
            INSERT INTO cuentas 
            (nombre, tipo, saldo, moneda, activa)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.nombre, self.tipo, self.saldo, self.moneda, self.activa
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
        
        query = "SELECT * FROM cuentas WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return cls(**result)
        return None

    @classmethod
    def listar(cls, solo_activas=True):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM cuentas"
        if solo_activas:
            query += " WHERE activa = 1"
        
        query += " ORDER BY nombre"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [cls(**data) for data in results]

    @classmethod
    def actualizar_saldo(cls, id, monto, es_ingreso=True):
        """Actualiza el saldo de una cuenta"""
        cuenta = cls.obtener_por_id(id)
        if not cuenta:
            return False
        
        if es_ingreso:
            cuenta.saldo += monto
        else:
            cuenta.saldo -= monto
        
        return cuenta.guardar()
