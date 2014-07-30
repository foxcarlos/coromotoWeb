from fpdf import FPDF
import dbf

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
        
        return self.ficha, self.nombre, self.tipov, self.cedula
                        
    def footer(self):
        ''' Pie de Pagina, obtiene la cedula de 
        la variable Global self.cedula'''
        
        ced = '*{0}*'.format(self.cedula)

        #Codigo de Barra        
        self.add_font('ean3', '', r"/home/cgarcia/desarrollo/python/coromotoWeb/carnetPdf/free3of9/fre3of9x.ttf", uni=True)        
        self.set_font('ean3', '', 21)
        self.set_text_color(0,0,0)
        self.set_y(-20)
        self.cell(0, 7, ced , align="C")

    def header(self):
        ''' La cabecera toma las variables Globales'''
        
class ReportTablePDF:

    def __init__(self):
        self.pdf = MyPDF()
        listaDevuelta = self.pdf.buscarFicha('11951')
        self.ficha, self.nombre, self.tipov, self.cedula = listaDevuelta

    def imprimir(self):
        ''' Imprime en el carnet los datos del empleado tomandolos 
        de las variables globales generadas en el metodo buscarFicha()'''

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

pdf = ReportTablePDF()
pdf.imprimir()

