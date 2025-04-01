from ..models.clientes import Cliente

class ClientesController:
    @staticmethod
    def crear(datos):
        cliente = Cliente(
            nombre=datos.get('nombre'),
            rfc=datos.get('rfc'),
            direccion=datos.get('direccion'),
            telefono=datos.get('telefono'),
            email=datos.get('email')
        )
        return cliente.guardar()
    
    @staticmethod
    def actualizar(id, datos):
        cliente = Cliente.obtener_por_id(id)
        if not cliente:
            return False
        
        cliente.nombre = datos.get('nombre', cliente.nombre)
        cliente.rfc = datos.get('rfc', cliente.rfc)
        cliente.direccion = datos.get('direccion', cliente.direccion)
        cliente.telefono = datos.get('telefono', cliente.telefono)
        cliente.email = datos.get('email', cliente.email)
        cliente.activo = datos.get('activo', cliente.activo)
        
        return cliente.guardar()
    
    @staticmethod
    def listar(solo_activos=True):
        return Cliente.listar(solo_activos)
    
    @staticmethod
    def obtener_por_id(id):
        return Cliente.obtener_por_id(id)
    
    @staticmethod
    def eliminar(id):
        return Cliente.eliminar(id)