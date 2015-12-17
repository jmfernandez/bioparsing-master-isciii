#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Prácticas de Python 2.7 y bases de datos biológicas
	Script de parseado de entradas en formato SWISSPROT
	Máster en Bioinformática y Biología Computacional, ENS-ISCIII
	Curso: 2015-2016
	Asignatura: Big Data Parsing and Processing
	Autor: José María Fernández
'''

from __future__ import print_function
import sys
import io
import re

# Comprobación del número de parámetros de entrada
if __name__ == '__main__':
	if len(sys.argv)>1:
		# Procesamiento de cada fichero
		for filename in sys.argv[1:]:
			try:
				# Estamos abriendo el fichero con el encoding 'latin-1'
				# Para text mining lo recomendable es el encoding 'utf-8'
				with io.open(filename,'r',encoding="latin-1") as infile:
					print("Procesando fichero ",filename)
					
					# Inicialización de variables
					acc = []
					id = ''
					lastdate = ''
					description = ''
					sequence = ''
					molw = ''
					readingseq = False
					
					for line in infile:
						# Lo primero, quitar el salto de línea
						line = line.rstrip('\n')
						
						# Detección del final del registro
						if re.search('^//',line) is not None:
							# Cuando se ha terminado de leer un
							# registro hay que proceder a guardar
							# los datos en la base de datos
							
							if description == '':
								description = None
							
							# Aquí es donde ya tenemos los datos enteros de una entrada
							# y podríamos enviarlos a otras funciones, programas, almacenarlos
							# etc...
							# Para demostrar que llega aquí, hacemos una impresión de comprobación
							print("ACC: {0} ; ID: {1} ; Last: {2}".format(acc[0],id,lastdate))
							print("All accession numbers: ",', '.join(acc))
							
							# Y ahora, toca restaurar las variables a sus valores por defecto
							acc = []
							id = ''
							lastdate = ''
							description = ''
							sequence = ''
							molw = ''
							readingseq = False
						# ¿Estoy leyendo una secuencia?
						elif readingseq:
							# Quito todos los espacios intermedios 
							line = re.compile(r"\s+").sub('',line)
							
							# Y concateno
							sequence += line
							
						# Como no la estoy leyendo, busco los patrones apropiados
						else:
							seqmatch = re.search(r"^SQ.+[^0-9](\d+) MW",line)
							if seqmatch is not None:
								# Extracción del peso molecular
								# y comienzo de secuencia
								molw = seqmatch.group(1)
								
								readingseq = True
							else:
								idmatch = re.search(r"^ID   ([a-zA-Z0-9_]+)",line)
								if idmatch is not None:
									# Identificador
									id = idmatch.group(1)
								else:
									dtmatch = re.search(r"^DT   (\d{2}-[A-Z]{3}-\d{4}),",line)
									if dtmatch is not None:
										# Fecha de la última actualización
										lastdate = dtmatch.group(1)
									else:
										acmatch = re.search(r"^AC   (.+)",line)
										if acmatch is not None:
											# Los accnumber, que pueden estar en varias líneas
											ac = acmatch.group(1)
											# Elimino los espacios y quito el posible último punto y coma
											ac = re.compile(r"\s+").sub('',ac).rstrip(';')
											
											# Rompo por los puntos y coma, y
											# añado a la lista de accnumber
											acc.extend(ac.split(';'))
										else:
											dematch = re.search(r"^DE   RecName: Full=(.+);",line)
											if dematch is not None:
												# La descripción, que puede estar en varias líneas
												if description != '':
													description += ', EC '
												description += dematch.group(1)
			except IOError as e:
				print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
				#raise
			except:
				print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
				raise
		
	else:
		raise AssertionError("Debes introducir al menos un fichero con formato SW.")
