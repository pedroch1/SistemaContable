from ..models.cuentas import Cuenta
from ..models.transacciones import Transaccion
from datetime import datetime, timedelta

class CuentasController:
    @staticmethod
    def crear(datos):
        cuenta = Cuenta(
            nombre=datos.get('nombre'),
            tipo=datos.get('tipo'),
            saldo=float(datos.get('saldo', 0)),
            moneda=datos.get('moneda', 'USD')
        )
        return cuenta.guardar()
    
    @staticmethod
    def actualizar(id, datos):
        cuenta = Cuenta.obtener_por_id(id)
        if not cuenta:
            return False
        
        cuenta.nombre = datos.get('nombre', cuenta.nombre)
        cuenta.tipo = datos.get('tipo', cuenta.tipo)
        cuenta.saldo = float(datos.get('saldo', cuenta.saldo))
        cuenta.moneda = datos.get('moneda', cuenta.moneda)
        cuenta.activa = datos.get('activa', cuenta.activa)
        
        return cuenta.guardar()
    
    @staticmethod
    def listar(solo_activas=True):
        return Cuenta.listar(solo_activas)
    
    @staticmethod
    def obtener_por_id(id):
        return Cuenta.obtener_por_id(id)
    
    @staticmethod
    def listar_cuentas_por_cobrar(dias_vencimiento=None):
        """Lista las cuentas por cobrar, opcionalmente filtrando por días de vencimiento"""
        conn = Cuenta.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT cpc.*, c.nombre as cliente_nombre 
        FROM cuentas_por_cobrar cpc
        JOIN clientes c ON cpc.cliente_id = c.id
        WHERE cpc.estado = 'pendiente'
        """
        
        params = []
        if dias_vencimiento:
            fecha_limite = datetime.now() - timedelta(days=dias_vencimiento)
            query += " AND cpc.fecha_vencimiento <= %s"
            params.append(fecha_limite)
        
        query += " ORDER BY cpc.fecha_vencimiento"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results
    
    @staticmethod
    def listar_cuentas_por_pagar(dias_vencimiento=None):
        """Lista las cuentas por pagar, opcionalmente filtrando por días de vencimiento"""
        conn = Cuenta.get_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT cpp.*, p.nombre as proveedor_nombre 
        FROM cuentas_por_pagar cpp
        JOIN proveedores p ON cpp.proveedor_id = p.id
        WHERE cpp.estado = 'pendiente'
        """
        
        params = []
        if dias_vencimiento:
            fecha_limite = datetime.now() - timedelta(days=dias_vencimiento)
            query += " AND cpp.fecha_vencimiento <= %s"
            params.append(fecha_limite)
        
        query += " ORDER BY cpp.fecha_vencimiento"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results