from ..models.proveedores import Proveedor

class ProveedoresController:
    @staticmethod
    def crear(datos):
        proveedor = Proveedor(
            nombre=datos.get('nombre'),
            rfc=datos.get('rfc'),
            direccion=datos.get('direccion'),
            telefono=datos.get('telefono'),
            email=datos.get('email')
        )
        return proveedor.guardar()
    
    @staticmethod
    def actualizar(id, datos):
        proveedor = Proveedor.obtener_por_id(id)
        if not proveedor:
            return False
        
        proveedor.nombre = datos.get('nombre', proveedor.nombre)
        proveedor.rfc = datos.get('rfc', proveedor.rfc)
        proveedor.direccion = datos.get('direccion', proveedor.direccion)
        proveedor.telefono = datos.get('telefono', proveedor.telefono)
        proveedor.email = datos.get('email', proveedor.email)
        proveedor.activo = datos.get('activo', proveedor.activo)
        
        return proveedor.guardar()
    
    @staticmethod
    def listar(solo_activos=True):
        return Proveedor.listar(solo_activos)
    
    @staticmethod
    def obtener_por_id(id):
        return Proveedor.obtener_por_id(id)
    
    @staticmethod
    def eliminar(id):
        return Proveedor.eliminar(id)