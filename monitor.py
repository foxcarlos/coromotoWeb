import sys
import bottle
from bottle import default_app, run, get, post, template, error
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from carnetPdf import carnet
from time import sleep
import webbrowser
import os

users = set()

@error(404)
def error404(error):
    return 'Error no se consiguio la pagina'

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
    
    pdfDelante = carnet.DelanteReportTablePDF(datos)
    pdfDelante.imprimir()
    
    pdfDetras = carnet.DetrasReportTablePDF(datos)
    pdfDetras.imprimir()

    return template('CarnetPdfEmpleados', {'ficha':ficha, 'nombre':nombre, 'apellido':apellido, 'cargo':cargo, 'departamento':departamento, 'foto':foto})

run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)
