from fpdf import FPDF
import dbf
import os

class CrearNxxmast:
    def __init__(self):
        ''' '''
        
    def dbf2List(self, tabla, parametros=''):
        useTabla = dbf.Table(tabla)
        useTabla.open()
        consulta = 'select * where status == "1"'
        busqueda = useTabla.query(consulta)
        lista = [reg for reg in busqueda]
        return lista
    
    def tablaNxxmast(self):
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
    
class MyPDF(FPDF):
    def __init__(self):
        ''' Se ejecuta el metodo __init__ de la clase MyPDF()
        y se e pasa como parametro el tamano del carnet'''
        FPDF.__init__(self, orientation='P',unit='mm',format=(55,85))

    def buscarFicha(self, ficha):
        '''Metodo que permite buscar una Ficha
        en la tabla del nxxmast.dbf'''
        
        self.fichaBuscar = ficha
        self.ficha = '00000'
        self.nombre = 'DESCONOCIDO,'
        self.tipov = 'X'
        self.cedula = 0
        
        nx = CrearNxxmast()
        reg = nx.tablaNxxmast()
        for f in reg:            
            if  f[1] == self.fichaBuscar:
                self.ficha, self.nombre, self.tipov, self.cedula = f[1], f[2], f[3], f[4]
                print(self.ficha, self.nombre, self.tipov, self.cedula)
                        
    def footer(self):
        ''' Pie de Pagina, obtiene el nombre y el apellido de 
        la variable Global self.nombre'''
        
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
        
        imgBandera = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/Bandera.JPG"
        imgFondo = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/FONDOCARNET.jpg"
        imgLogo = "/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/img/HOSPITALC.JPG"
        imgFoto = '/media/serv_coromoto/NominaShc/FotosE/F00{0}.JPG'.format(str(self.ficha))

        #Agrego las Imagenes de cabecera
        self.image(imgFondo, 0,11,w=55,h=81)
        self.image(imgBandera,0,10,w=55,h=11)
        
        #Imagen de la Foto, solo se agrega si existe la imagen
        if os.path.isfile(imgFoto):
            #self.image(imgFoto,15,42,w=25,h=33)
            self.image(imgFoto,15,41,w=25.54,h=29.30)
        
        #Imagen del Logo
        self.image(imgLogo,5, 29, w=9, h=12)
        
        
class ReportTablePDF:

    def __init__(self):
        self.pdf = MyPDF()
        self.pdf.buscarFicha('11951')

    def imprimir(self):  
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

pdf = ReportTablePDF()
pdf.imprimir()

