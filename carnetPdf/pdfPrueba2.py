#Realizado Por:Carlos Alberto Garcia Diaz

from fpdf import FPDF

#defino el Marco de Trabajo en Centimetros
#pdf = FPDF('P', 'cm',(5500,8400))
#pdf = FPDF(orientation='P',unit='in',format=(2.2, 3.2))
pdf = FPDF(orientation='P',unit='mm',format=(55,85))

#Creo la pagina
pdf.add_page()

imgBandera = "Bandera.JPG"
imgFondo = "FONDOCARNET.jpg"
imgLogo = "HOSPITALC.JPG"
imgFoto = '/media/serv_coromoto/NominaShc/FotosE/F0011951.jpg'

apellidos = 'GARCIA DIAZ'
nombres = 'CARLOS ALBERTO'

#Agrego las Imagenes
pdf.image(imgFondo, 0,0,55,85)
pdf.image(imgBandera,0,10,60,10.5)

pdf.ln(13)
#Primer Texto y tipo de letra
pdf.set_font('Arial', 'B', 7)
pdf.set_text_color(255,0,0)
pdf.cell(w=0,h=0,txt='REPUBLICA BOLIVARIANA DE VENEZUELA',border=0,ln=1,align='C')

#Segundo Texto y tipo de letra
pdf.set_font('Arial', 'B', 9)
pdf.set_text_color(255,0,0)
pdf.cell(w=0,h=7,txt='PDV SERVICIOS DE SALUD S.A.',border=0,ln=1,align='C')

#Imagen del Logo
pdf.image(imgLogo,5, 29, w=9, h=12)

#Tercer Texto y tipo de letra
pdf.set_font('Arial', 'B', 12)
pdf.cell(0,4, 'HOSPITAL', 0, 1, 'C')
pdf.cell(0,8,'COROMOTO', 0, 1, 'C')

#Imagen de la Foto
pdf.image(imgFoto,15,42,w=25,h=33)
#pdf.ln(22)

#Segundo Texto y tipo de letra
pdf.set_font('Arial', 'B', 10)
pdf.cell(0,-15, apellidos, 0, 0, 'C')

pdf.output('PRUEBA.PDF', 'F')
