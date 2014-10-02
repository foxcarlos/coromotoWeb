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
    return 'Nothing here, sorry'

'''@bottle.route('/download/<filename:path>')
def download(filename):
    return bottle.static_file(filename, root='/path/to/static/files', download=filename)
'''

@bottle.route('/delante')
def delante():
    ficha = bottle.request.forms.get('ficha')
    ficha2 = bottle.request.forms.get('ficha2')
    nombre2 = bottle.request.forms.get('nombre2')
    print('ficha',ficha)
    print('ficha2', ficha2)
    print('Nombre', nombre2)

    archivo = "{0}_Delante.PDF".format(ficha2)
    print('archivo', archivo)
    return bottle.static_file(archivo, root='static/')

@bottle.route('/detras')
def detras():
    ficha = bottle.request.forms.get('ficha2')
    archivo = "{0}_Detras.PDF".format(ficha)
    return bottle.static_file(archivo, root='static/')

@get('/')
def index():
    return template('index')

@get('/empleados')
def index2():
    return template('CarnetPdfEmpleados')

@post('/empleados')
def buscaCarnet():
    nombre = bottle.request.forms.get('nombre')
    ficha = bottle.request.forms.get('ficha')

    #self.listaFichaCedula = listaFichaCedula
    #print(nombre, ficha)

    nxxMast = carnet.CrearNxxmast()
    datos = nxxMast.buscarFicha(ficha)
    ficha, apellido, nombre, tipov, cedula, cargo, departamento = datos
    
    '''pdfDelante = carnet.DelanteReportTablePDF(datos)
    pdfDelante.imprimir()
    
    pdfDetras = carnet.DetrasReportTablePDF(datos)
    pdfDetras.imprimir()

    #Abrir los PDF
    sleep(5)
    url = "/home/cgarcia/desarrollo/python/coromotoWeb/{0}_Detras.PDF".format(ficha)
    url2 = "/home/cgarcia/desarrollo/python/coromotoWeb/{0}_Delante.PDF".format(ficha)
    webbrowser.open(url)
    webbrowser.open(url2)'''
    return template('CarnetPdfEmpleados', {'ficha':ficha, 'nombre':nombre, 'apellido':apellido, 'cargo':cargo, 'departamento':departamento})

run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)
