from ..models.transacciones import Transaccion
from datetime import datetime, timedelta

class ReportesController:
    @staticmethod
    def generar_balance(fecha_inicio=None, fecha_fin=None):
        """Genera un balance general para el período especificado"""
        if not fecha_inicio:
            fecha_inicio = datetime.now().replace(day=1)
        if not fecha_fin:
            fecha_fin = datetime.now()
        
        # Obtener todas las transacciones en el período
        filtros = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        }
        transacciones = Transaccion.listar(filtros)
        
        # Calcular totales
        ingresos = sum(t.monto for t in transacciones if t.tipo == 'ingreso')
        gastos = sum(t.monto for t in transacciones if t.tipo == 'gasto')
        balance = ingresos - gastos
        
        # Agrupar por categorías
        categorias_ingresos = {}
        categorias_gastos = {}
        
        for t in transacciones:
            if t.tipo == 'ingreso':
                categorias_ingresos[t.categoria_id] = categorias_ingresos.get(t.categoria_id, 0) + t.monto
            else:
                categorias_gastos[t.categoria_id] = categorias_gastos.get(t.categoria_id, 0) + t.monto
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ingresos_total': ingresos,
            'gastos_total': gastos,
            'balance': balance,
            'categorias_ingresos': categorias_ingresos,
            'categorias_gastos': categorias_gastos,
            'transacciones': transacciones
        }
    
    @staticmethod
    def estado_resultados(periodo='mensual'):
        """Genera un estado de resultados para el período especificado"""
        hoy = datetime.now()
        
        if periodo == 'mensual':
            fecha_inicio = hoy.replace(day=1)
        elif periodo == 'trimestral':
            mes_actual = hoy.month
            trimestre_inicio = ((mes_actual - 1) // 3) * 3 + 1
            fecha_inicio = hoy.replace(month=trimestre_inicio, day=1)
        elif periodo == 'anual':
            fecha_inicio = hoy.replace(month=1, day=1)
        else:
            fecha_inicio = hoy - timedelta(days=30)
        
        return ReportesController.generar_balance(fecha_inicio, hoy)
    
    @staticmethod
    def flujo_efectivo(periodo=30):
        """Genera un reporte de flujo de efectivo para los últimos días especificados"""
        hoy = datetime.now()
        fecha_inicio = hoy - timedelta(days=periodo)
        
        # Obtener transacciones agrupadas por día
        filtros = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': hoy
        }
        
        transacciones = Transaccion.listar(filtros)
        
        # Agrupar por día
        dias = {}
        for t in transacciones:
            fecha_str = t.fecha.strftime('%Y-%m-%d')
            if fecha_str not in dias:
                dias[fecha_str] = {'ingresos': 0, 'gastos': 0, 'balance': 0}
            
            if t.tipo == 'ingreso':
                dias[fecha_str]['ingresos'] += t.monto
            else:
                dias[fecha_str]['gastos'] += t.monto
            
            dias[fecha_str]['balance'] = dias[fecha_str]['ingresos'] - dias[fecha_str]['gastos']
        
        # Organizar como serie temporal
        serie_temporal = []
        fecha_actual = fecha_inicio
        while fecha_actual <= hoy:
            fecha_str = fecha_actual.strftime('%Y-%m-%d')
            if fecha_str in dias:
                serie_temporal.append({
                    'fecha': fecha_str,
                    'ingresos': dias[fecha_str]['ingresos'],
                    'gastos': dias[fecha_str]['gastos'],
                    'balance': dias[fecha_str]['balance']
                })
            else:
                serie_temporal.append({
                    'fecha': fecha_str,
                    'ingresos': 0,
                    'gastos': 0,
                    'balance': 0
                })
            fecha_actual += timedelta(days=1)
        
        return serie_temporal