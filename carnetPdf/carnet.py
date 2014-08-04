from fpdf import FPDF
import dbf
import os

class CrearNxxmast:
    def __init__(self):
        '''La Clase CrearNxxMast esta hecha solo para uso exclusivo
        del Hospital Coromoto ya que alli es donde se encuentran 
        los datos de los empleados que se le entregaran los carnet,
        las tablas que usan estan hechas en VisualFoxPro'''
        
    def dbf2List(self, tabla, parametros=''):
        '''Consulta las tablas de VFP y devuelve una
        lista con los datos'''

        useTabla = dbf.Table(tabla)
        useTabla.open()
        consulta = 'select * where status == "1"'
        busqueda = useTabla.query(consulta)
        lista = [reg for reg in busqueda]
        return lista
    
    def tablaNxxmast(self):
        '''Este metodo hace una union de las diferentes tablas que
        usan los sistemas del Hospital Coromoto'''

        nxxMast = []
        rutaArchivoDbf = '/media/serv_coromoto/Nomina/asencwin/nominaw/ncsmast.dbf'
        rutaArchivoDbf2 = '/media/serv_coromoto/Nomina/asencwin/nominaw/ncmmast.dbf'
        rutaArchivoDbf3 = '/media/serv_coromoto/Nomina/asencwin/nominaw/nepmast.dbf'
        rutaArchivoDbf4 = '/media/serv_coromoto/Nomina/asencwin/nominaw/nmdmast.dbf'
        rutaArchivoDbf5 = '/media/serv_coromoto/Nomina/asencwin/nominaw/nnmmast.dbf'
    
        cs = self.dbf2List(rutaArchivoDbf)
        nxxMast.extend(cs)
    
        cm = self.dbf2List(rutaArchivoDbf2)
        nxxMast.extend(cm)
    
        ep = self.dbf2List(rutaArchivoDbf3)
        nxxMast.extend(ep)
    
        md = self.dbf2List(rutaArchivoDbf4)
        nxxMast.extend(md)
    
        nm = self.dbf2List(rutaArchivoDbf5)
        nxxMast.extend(nm)        
        return nxxMast
    
    def buscarFicha(self, ficha):
        '''Metodo que permite buscar una Ficha
        en la tabla del nxxmast.dbf basado en la 
        ficha pasada como parametro'''

        self.fichaBuscar = ficha
        self.ficha = '00000'
        self.nombre = 'DESCONOCIDO,'
        self.tipov = 'X'
        self.cedula = 0
        
        reg = self.tablaNxxmast()
        for f in reg:            
            if  f[1] == self.fichaBuscar:
                self.ficha, self.nombre, self.tipov, self.cedula = f[1], f[2], f[3], f[4]
                print(self.ficha, self.nombre, self.tipov, self.cedula)
        
        return self.ficha, self.nombre, self.tipov, self.cedula

    
class DetrasMyPDF(FPDF):
    def __init__(self, datosPersonal):
        '''Parametros recibidos:1, Tipo Lista (ficha, nombre, tipov, cedula)
        Se ejecuta el metodo __init__ de la clase DetrasMyPDF()'''

        #Se ejecuta el init de la clase Padre
        FPDF.__init__(self, orientation='P',unit='mm',format=(55,84))
        
        #Se guarda el parametro pasado
        self.datosPersonal = datosPersonal
                
    def devuelveDatos(self):
        '''Solo para uso internet'''
        return self.datosPersonal

    def footer(self):
        ''' Pie de Pagina, obtiene la cedula de 
        la variable Global self.cedula'''

        self.ficha, self.nombre, self.tipov, self.cedula = self.datosPersonal
        ced = '*{0}*'.format(self.ficha)

        #Codigo de Barra        
        self.add_font('ean3', '', r"/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/free3of9/fre3of9x.ttf", uni=True)        
        self.set_font('ean3', '', 24)
        self.set_text_color(0,0,0)
        self.set_y(-20)
        self.cell(0, 7, ced , align="C")

    def header(self):
        ''' La cabecera toma las variables Globales'''
        
class DetrasReportTablePDF:
    '''Clase que permite imprimir la parte trasera del Carnet '''

    def __init__(self, datosPersonal):
        '''Parametros recibidos:1, Tipo Lista (ficha, nombre, tipov, cedula)'''

        self.datosPersonal = datosPersonal
        self.pdf = DetrasMyPDF(self.datosPersonal)

    def imprimir(self):
        ''' Imprime en el carnet los datos del empleado tomandolos 
        de las variables globales generadas en el metodo buscarFicha()'''

        self.ficha, self.nombre, self.tipov, self.cedula = self.pdf.devuelveDatos()
        ficha = self.ficha
        cedula = self.cedula

        cabe1 = 'FICHA: {0}'.format(ficha)
        cabe2 = 'C.I.: {0}'.format(cedula)
        cabe3 = 'VALIDO SOLO COMO DOCUMENTO DE '
        cabe3a = 'IDENTIFICACION INTERNO. SU USO INDEBIDO'
        cabe3b = 'NO REPRESENTA NINGUNA RESPONSABILIDAD'
        cabe3c = 'PARA EL HOSPITAL COROMOTO.'''
        cabe4 = 'ESTE DOCUMENTO ES PROPIEDAD DE LA INSTITUCION.'
        
        self.pdf.add_page()

        #Ficha
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.set_text_color(0,0,0)
        self.pdf.cell(0,12,cabe1,0,1,'C')
        
        #Cedula
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.set_text_color(0,0,0)
        self.pdf.cell(0,1,cabe2,0,1,'C')
        
        #Advertencia
        self.pdf.set_font('Arial', 'B', 5)
        self.pdf.cell(0,25, cabe3, 0, 0, 'C')
        self.pdf.ln(2)
        self.pdf.cell(0,25, cabe3a, 0, 0, 'C')
        self.pdf.ln(2)
        self.pdf.cell(0,25, cabe3b, 0, 0, 'C')
        self.pdf.ln(2)
        self.pdf.cell(0,25, cabe3c, 0, 0, 'C')
        self.pdf.ln(3)
        self.pdf.cell(0,25, cabe4, 0, 0, 'C')
        self.pdf.ln(2)

        self.pdf.output('DETRAS.PDF','F')

#######################################################################################
#Apartir de aqui se imprime la parte delantera del Carnet
#######################################################################################

class DelanteMyPDF(FPDF):
    def __init__(self, datosPersonal):
        '''Parametros recibidos:1, Tipo Lista (ficha, nombre, tipov, cedula)
        Se ejecuta el metodo __init__ de la clase DetrasMyPDF()'''

        #Se Ejecuta el metodo Init de la Case Padre
        FPDF.__init__(self, orientation='P',unit='mm',format=(55,85))
        
        #Se guarda el parametro pasado
        self.datosPersonal = datosPersonal
                
    def devuelveDatos(self):
        return self.datosPersonal

    def footer(self):
        ''' Pie de Pagina, obtiene el nombre y el apellido de 
        la variable Global self.nombre'''

        self.ficha, self.nombre, self.tipov, self.cedula = self.datosPersonal
       
        NyA = self.nombre.split(',')
        apellidos = NyA[0].strip()
        nombres = NyA[1].strip()
        
        #Agrego Nombre del Empleado y lo ubico en el pie de pagina
        self.set_font('Arial', 'B', 10)
        self.set_y(-10)      
        self.cell(0, 7, apellidos, align="C")
        self.ln(2)
        self.cell(0, 11, nombres, align="C") 

    def header(self):
        ''' La cabecera toma las variables Globales'''

        self.ficha, self.nombre, self.tipov, self.cedula = self.datosPersonal
        imgBandera = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/Bandera.JPG"
        imgFondo = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/FONDOCARNET.jpg"
        imgLogo = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/HOSPITALC.JPG"
        imgFoto = '/media/serv_coromoto/NominaShc/FotosE/F00{0}.JPG'.format(str(self.ficha))

        #Agrego las Imagenes de cabecera
        self.image(imgFondo, 0,11,w=55,h=81)
        self.image(imgBandera,0,10,w=55,h=11)
        
        #Imagen de la Foto, solo se agrega si existe la imagen
        if os.path.isfile(imgFoto):
            self.image(imgFoto,15,41,w=25.54,h=29.30)
        
        #Imagen del Logo
        self.image(imgLogo,5, 29, w=9, h=12)

class DelanteReportTablePDF:
    def __init__(self, datosPersonal):
        '''Parametros recibidos:1, Tipo Lista (ficha, nombre, tipov, cedula)'''

        self.datosPersonal = datosPersonal
        self.pdf = DelanteMyPDF(self.datosPersonal)

    def imprimir(self):
        ''' Imprime en el carnet los datos del empleado tomandolos 
        de las variables globales generadas en el metodo buscarFicha()'''
        
        cabe1 = 'REPUBLICA BOLIVARIANA DE VENEZUELA'
        cabe2 = 'PDV SERVICIOS DE SALUD S.A.'
        cabe3 = 'HOSPITAL'
        cabe4 = 'COROMOTO'
        
        self.pdf.add_page()
        self.pdf.ln(13)

        #Primer Texto y tipo de letra
        self.pdf.set_font('Arial', 'B', 7)
        self.pdf.set_text_color(255,0,0)
        self.pdf.cell(w=0,h=0,txt=cabe1,border=0,ln=1,align='C')
        
        #Segundo Texto y tipo de letra
        self.pdf.set_font('Arial', 'B', 9)
        self.pdf.set_text_color(255,0,0)
        self.pdf.cell(w=0,h=7,txt=cabe2,border=0,ln=1,align='C')
        
        #Tercer Texto y tipo de letra
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0,4, cabe3, 0, 1, 'C')
        self.pdf.cell(0,8, cabe4, 0, 1, 'C')
        
        #Imagen de la Foto
        #self.pdf.image(self.imgFoto,15,42,w=25,h=33)
        self.pdf.output('PRUEBA.PDF','F')  


if __name__ == '__main__':
    ficha = raw_input('Ingrese el Numero de Ficha:')
    nxxMast = CrearNxxmast()
    datos = nxxMast.buscarFicha(ficha)
    
    pdfDelante = DelanteReportTablePDF(datos)
    pdfDelante.imprimir()
    
    pdfDetras = DetrasReportTablePDF(datos)
    pdfDetras.imprimir()

