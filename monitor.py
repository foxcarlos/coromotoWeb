import sys
import dbf
import bottle
from bottle import default_app, run, get, post, template, error
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from websocket import create_connection
from carnetPdf import carnet
from time import sleep
import webbrowser
import os

users = set()

def llamar(pac):    
    ws = create_connection("ws://localhost:8080/websocket")
    
    #pac = raw_input('ingrese el paciente a llamar:')
    ws.send(pac)
    result =  ws.recv()
    print "Received '%s'" % result
    ws.close()

def buscarEnDbf(control):
    '''DBF Consultar la tabla especialidad que se encuentra en una tabla de VFP
    para obtner la descripcion de la especialidad y el telefono a donde se debe llamar'''

    #campo = 'file_dbf'
    #tabladbf = self.fc.get('RUTAS', campo)
    
    #tabladbf = '/media/serv_coromoto/digitado/data/dgtcabe.dbf'
    tabladbf = '/home/cgarcia/.wine/drive_c/dgtcabe.DBF'

    print tabladbf
    #tabladbf = archv_dbf
    try:
        tabla_especial = dbf.Table(tabladbf)
        tabla_especial.open()
    except:
        #self.logger.error('Error al abrir la tabla DBF')
        #sys.exit()
        print('error al intentar abrir la tabla')

    #Buscar el codigo de la especialidad
    cadSql = "select * where control == '{0}'".format(control)
    buscar = tabla_especial.query(cadSql)
    if len(buscar) >0:
        for reg in buscar:
            #print(reg)
            print(reg[1])
            controlb = reg[1]
            tipo = reg[3]
            cedula = reg[4]
            nombre = reg[6]
            sexo = reg[11]
            edad = reg[12]
        return controlb, tipo, cedula, nombre, sexo, edad
    else:
        return []


@error(404)
def error404(error):
    return 'Error no se consiguio la pagina'

'''@bottle.route('/download/<filename:path>')
def download(filename):
    return bottle.static_file(filename, root='/path/to/static/files', download=filename)
'''

@get('/static/<filename:path>')
def static(filename): 
    return bottle.static_file(filename, root='static/')

@bottle.route('/delante/<ficha>')
def delante(ficha='desconocido'):
    ficha2 = ficha   
    archivo = "{0}_Delante.PDF".format(ficha2)
    return bottle.static_file(archivo, root='static/file/carnets/')

@bottle.route('/detras/<ficha>')
def detras(ficha='desconocido'):
    ficha2 = ficha   
    archivo = "{0}_Detras.PDF".format(ficha2)
    return bottle.static_file(archivo, root='static/file/carnets/')

@get('/')
def index():
    return template('index')

@get('/empleados')
def empleados():
    return template('CarnetPdfEmpleados')

@post('/empleados')
def buscaCedulaFicha():
    fotoImg = ''
    rutaFotosE = 'static/file/fotose'

    nombre = bottle.request.forms.get('nombre')
    ficha = bottle.request.forms.get('ficha')
    
    nxxMast = carnet.CrearNxxmast()
    datos = nxxMast.buscarFicha(ficha)
    ficha, apellido, nombre, tipov, cedula, cargo, departamento = datos
    
    #Permite buscar el archivo de a foto del Empleado
    #para devolver su nombre real
    listaArchivo = os.listdir(rutaFotosE)
    for f in listaArchivo:
        if ficha in f:
            fotoImg = f

    foto = os.path.join(rutaFotosE, fotoImg)
    if not os.path.isfile(foto):
        foto = ''
    
    print(foto)
    pdfDelante = carnet.DelanteReportTablePDF(datos)
    pdfDelante.imprimir()
    
    pdfDetras = carnet.DetrasReportTablePDF(datos)
    pdfDetras.imprimir()

    return template('CarnetPdfEmpleados', {'ficha':ficha, 'nombre':nombre, 'apellido':apellido, 'cargo':cargo, 'departamento':departamento, 'foto':foto})

run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)
