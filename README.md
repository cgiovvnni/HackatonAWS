# HackatonAWS


Archivos:

* conect.py:
Archivo con las funciones necesarias para generar las llaves para poder generar los objetos tipo cliente 

* transcribe.py:
Genera un cliente de tipo transcribe
También contiene una función que inicia la transcripción de un texto

* obtenerTexto.py:
Ayuda al archivo transcribe.py para determinar el momento en que la trascripción termina y regresa el texto y los items para poder ocupar el texto en otra función o para poder determinar la confianza de cada palabra

* comprehend.py:
Genera un cliente de tipo comprehend 
También contiene una función que inicia la comprensión de un texto 

* s3.py
Genera un cliente de tipo S3
También contiene una función para borrar un archivo de determinado bucket