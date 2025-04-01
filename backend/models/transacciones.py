import mysql.connector
from datetime import datetime
from ..config import DB_CONFIG

class Transaccion:
    def __init__(self, id=None, fecha=None, descripcion=None, monto=None, tipo=None, 
                 cuenta_id=None, categoria_id=None, cliente_proveedor_id=None):
        self.id = id
        self.fecha = fecha if fecha else datetime.now()
        self.descripcion = descripcion
        self.monto = monto
        self.tipo = tipo  # 'ingreso', 'gasto'
        self.cuenta_id = cuenta_id
        self.categoria_id = categoria_id
        self.cliente_proveedor_id = cliente_proveedor_id

    @staticmethod
    def get_conexion():
        return mysql.connector.connect(**DB_CONFIG)

    def guardar(self):
        conn = self.get_conexion()
        cursor = conn.cursor()
        
        if self.id:
            # Actualizar transacción existente
            query = """
            UPDATE transacciones 
            SET fecha = %s, descripcion = %s, monto = %s, tipo = %s, 
                cuenta_id = %s, categoria_id = %s, cliente_proveedor_id = %s
            WHERE id = %s
            """
            cursor.execute(query, (
                self.fecha, self.descripcion, self.monto, self.tipo,
                self.cuenta_id, self.categoria_id, self.cliente_proveedor_id, self.id
            ))
        else:
            # Insertar nueva transacción
            query = """
            INSERT INTO transacciones 
            (fecha, descripcion, monto, tipo, cuenta_id, categoria_id, cliente_proveedor_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.fecha, self.descripcion, self.monto, self.tipo,
                self.cuenta_id, self.categoria_id, self.cliente_proveedor_id
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
        
        query = "SELECT * FROM transacciones WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return cls(**result)
        return None

    @classmethod
    def listar(cls, filtros=None):
        conn = cls.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM transacciones"
        params = []
        
        if filtros:
            condiciones = []
            if 'fecha_inicio' in filtros and 'fecha_fin' in filtros:
                condiciones.append("fecha BETWEEN %s AND %s")
                params.extend([filtros['fecha_inicio'], filtros['fecha_fin']])
            if 'tipo' in filtros:
                condiciones.append("tipo = %s")
                params.append(filtros['tipo'])
            if 'categoria_id' in filtros:
                condiciones.append("categoria_id = %s")
                params.append(filtros['categoria_id'])
            
            if condiciones:
                query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY fecha DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [cls(**data) for data in results]

    @classmethod
    def eliminar(cls, id):
        conn = cls.get_conexion()
        cursor = conn.cursor()
        
        query = "DELETE FROM transacciones WHERE id = %s"
        cursor.execute(query, (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return cursor.rowcount > 0