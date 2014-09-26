import sys
import dbf
import bottle
from bottle import default_app, run, get, post, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from websocket import create_connection
from carnetPdf import carnet

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

@get('static/<filename:path>')
def static(filename): 
    return bottle.static_file(filename, root='static/')

@get('/')
def index():
    return template('index')

@get('/empleados')
def index2():
    return template('CarnetPdfEmpleados')

@post('/buscarCarnet')
def buscaCarnet(listaFichaCedula):
    self.listaFichaCedula = listaFichaCedula
    print(listaFichaCedula)



run(host='127.0.0.1', port=8080, server=GeventWebSocketServer)
