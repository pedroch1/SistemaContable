from ..models.categorias import Categoria

class CategoriaController:
    @staticmethod
    def crear(datos):
        categoria = Categoria(
            nombre=datos.get('nombre'),
            tipo=datos.get('tipo'),
            descripcion=datos.get('descripcion')
        )
        return categoria.guardar()
    
    @staticmethod
    def actualizar(id, datos):
        categoria = Categoria.obtener_por_id(id)
        if not categoria:
            return False
        
        categoria.nombre = datos.get('nombre', categoria.nombre)
        categoria.tipo = datos.get('tipo', categoria.tipo)
        categoria.descripcion = datos.get('descripcion', categoria.descripcion)
        
        return categoria.guardar()
    
    @staticmethod
    def listar(tipo=None):
        return Categoria.listar(tipo)
    
    @staticmethod
    def obtener_por_id(id):
        return Categoria.obtener_por_id(id)
    
    @staticmethod
    def eliminar(id):
        return Categoria.eliminar(id)