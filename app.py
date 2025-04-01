from flask import Flask, render_template, request, jsonify, redirect, url_for
from backend.controllers.transacciones_controller import TransaccionesController
from backend.controllers.reportes_controller import ReportesController
from backend.controllers.impuestos_controller import ImpuestosController
from backend.controllers.cuentas_controller import CuentasController
from backend.controllers.inventario_controller import InventarioController
from backend.controllers.nomina_controller import NominaController
from backend.controllers.proveedores_controller import ProveedoresController
from backend.controllers.categoria_controller import CategoriaController
from backend.controllers.clientes_controller import ClientesController
app = Flask(__name__)

# Rutas para el panel principal
@app.route('/')
def index():
    # Obtener resumen para el dashboard
    balance = ReportesController.generar_balance()
    proximos_impuestos = ImpuestosController.listar_proximos_vencimientos()
    cuentas_por_cobrar = CuentasController.listar_cuentas_por_cobrar()
    cuentas_por_pagar = CuentasController.listar_cuentas_por_pagar()
    
    return render_template('index.html', 
                          balance=balance,
                          proximos_impuestos=proximos_impuestos,
                          cuentas_por_cobrar=cuentas_por_cobrar,
                          cuentas_por_pagar=cuentas_por_pagar)

# Rutas para transacciones
@app.route('/transacciones')
def listar_transacciones():
    filtros = {}
    if 'fecha_inicio' in request.args and 'fecha_fin' in request.args:
        filtros['fecha_inicio'] = request.args.get('fecha_inicio')
        filtros['fecha_fin'] = request.args.get('fecha_fin')
    if 'tipo' in request.args:
        filtros['tipo'] = request.args.get('tipo')
    
    transacciones = TransaccionesController.listar(filtros)
    return render_template('transacciones/lista.html', transacciones=transacciones)

@app.route('/transacciones/nueva', methods=['GET', 'POST'])
def nueva_transaccion():
    if request.method == 'POST':
        datos = request.form
        TransaccionesController.crear(datos)
        return redirect(url_for('listar_transacciones'))
    
    # Obtener datos necesarios para el formulario
    categorias = CategoriaController.listar()
    cuentas = CuentasController.listar()
    clientes = ClientesController.listar()
    proveedores = ProveedoresController.listar()
    
    return render_template('transacciones/formulario.html',
                          categorias=categorias,
                          cuentas=cuentas,
                          clientes=clientes,
                          proveedores=proveedores)

# Rutas para reportes
@app.route('/reportes/balance')
def reporte_balance():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    balance = ReportesController.generar_balance(fecha_inicio, fecha_fin)
    return render_template('reportes/balance.html', balance=balance)

@app.route('/reportes/estado-resultados')
def reporte_estado_resultados():
    periodo = request.args.get('periodo', 'mensual')
    
    estado = ReportesController.estado_resultados(periodo)
    return render_template('reportes/estado_resultados.html', estado=estado)

@app.route('/reportes/flujo-efectivo')
def reporte_flujo_efectivo():
    periodo = int(request.args.get('periodo', 30))
    
    flujo = ReportesController.flujo_efectivo(periodo)
    return render_template('reportes/flujo_efectivo.html', flujo=flujo)

# Rutas para impuestos
@app.route('/impuestos')
def listar_impuestos():
    impuestos = ImpuestosController.listar()
    return render_template('impuestos/lista.html', impuestos=impuestos)

@app.route('/impuestos/nuevo', methods=['GET', 'POST'])
def nuevo_impuesto():
    if request.method == 'POST':
        datos = request.form
        ImpuestosController.crear(datos)
        return redirect(url_for('listar_impuestos'))
    
    return render_template('impuestos/formulario.html')

# Rutas para nómina
@app.route('/nomina')
def listar_nomina():
    empleados = NominaController.listar_empleados()
    return render_template('nomina/lista.html', empleados=empleados)

@app.route('/nomina/calcular', methods=['GET', 'POST'])
def calcular_nomina():
    if request.method == 'POST':
        periodo = request.form.get('periodo')
        NominaController.calcular_nomina(periodo)
        return redirect(url_for('ver_nomina', periodo=periodo))
    
    return render_template('nomina/formulario_calculo.html')

@app.route('/nomina/periodo/<periodo>')
def ver_nomina(periodo):
    detalles = NominaController.obtener_nomina_periodo(periodo)
    return render_template('nomina/detalle_periodo.html', detalles=detalles, periodo=periodo)

# API endpoints para AJAX
@app.route('/api/dashboard/resumen')
def api_dashboard_resumen():
    balance = ReportesController.generar_balance()
    return jsonify(balance)

if __name__ == '__main__':
    app.run(debug=True)