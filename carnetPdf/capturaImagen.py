#!/usr/bin/env python

from SimpleCV import Camera, Display, Image
from time import sleep

#Se inicializa la camara
camara = Camera()

#Se captura una imagen usando la camara

imagen = camara.getImage()

#Se salva la imagen en un archivo
imagen.save("/home/cgarcia/captura.png")

#imagen.show()
sleep(2)

