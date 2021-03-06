#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Prácticas de Python 2.7 y bases de datos biológicas
	Script de parseado de entradas en formato SWISSPROT a partir de datos en red
	Máster en Bioinformática y Biología Computacional, ENS-ISCIII
	Curso: 2015-2016
	Asignatura: Big Data Parsing and Processing
	Autor: José María Fernández
'''

from __future__ import print_function
import sys
import io
import re
import urllib2

class SWParser(object):
	def __init__(self,filehandle):
		self.filehandle = filehandle
	
	def __iter__(self):
		
		return self
	
	#def __next__(self):
	def next(self):
		# Inicialización de variables
		acc = []
		id = ''
		lastdate = ''
		description = ''
		sequence = ''
		molw = ''
		readingseq = False
		for line in self.filehandle:
			# Lo primero, quitar el salto de línea
			line = line.rstrip('\n')
			
			# Detección del final del registro
			if re.search('^//',line) is not None:
				# Cuando se ha terminado de leer un
				# registro hay que proceder a guardar
				# los datos en la base de datos
				
				if description == '':
					description = None
				
				return acc,id,lastdate,description,sequence,molw
			
			# ¿Estoy leyendo una secuencia?
			if readingseq:
				# Quito todos los espacios intermedios 
				line = re.compile(r"\s+").sub('',line)
				
				# Y concateno
				sequence += line
				
			# Como no la estoy leyendo, busco los patrones apropiados
			else:
				seqmatch = re.search(r"^SQ.+[^0-9](\d+) MW",line)
				matched = seqmatch is not None
				
				idmatch = None if matched else re.search(r"^ID   ([a-zA-Z0-9_]+)",line)
				matched = matched or idmatch is not None
				
				dtmatch = None if matched else re.search(r"^DT   (\d{2}-[A-Z]{3}-\d{4}),",line)
				matched = matched or dtmatch is not None
				
				acmatch = None if matched else re.search(r"^AC   (.+)",line)
				matched = matched or acmatch is not None
				
				dematch = None if matched else re.search(r"^DE   RecName: Full=(.+);",line)
				matched = matched or dematch is not None
				
				if matched:
					if seqmatch is not None:
						# Extracción del peso molecular
						# y comienzo de secuencia
						molw = seqmatch.group(1)
						
						readingseq = True
					elif idmatch is not None:
						# Identificador
						id = idmatch.group(1)
					elif dtmatch is not None:
						# Fecha de la última actualización
						lastdate = dtmatch.group(1)
					elif acmatch is not None:
						# Los accnumber, que pueden estar en varias líneas
						ac = acmatch.group(1)
						# Elimino los espacios y quito el posible último punto y coma
						ac = re.compile(r"\s+").sub('',ac).rstrip(';')
						
						# Rompo por los puntos y coma, y
						# añado a la lista de accnumber
						acc.extend(ac.split(';'))
					elif dematch is not None:
						# La descripción, que puede estar en varias líneas
						if description != '':
							description += ', EC '
						description += dematch.group(1)
		
		# No lo cerramos nosotros, porque podría no ser un fichero
		# self.filehandle.close()
		
		# Y como hemos terminado, lo indicamos
		raise StopIteration


# Comprobación del número de parámetros de entrada
if __name__ == '__main__':
	if len(sys.argv)>1:
		# Procesamiento de cada fichero
		for input_uri in sys.argv[1:]:
			uri_handle = None
			try:
				uri_handle = urllib2.urlopen(input_uri)
				print("Procesando URI ",input_uri)
				for acc,id,lastdate,description,sequence,molw in SWParser(uri_handle):
					
					# Impresión de comprobación
					print("ACC: {0} ; ID: {1} ; Last: {2}".format(acc[0],id,lastdate))
					print("All accession numbers: ",', '.join(acc))
			except IOError as e:
				print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
				#raise
			except:
				print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
				raise
			finally:
				if uri_handle is not None:
					# Siempre hay que cerrar los recursos que se vayan a quedar abiertos
					# (ficheros, conexiones a internet, conexiones a bases de datos, ...)
					uri_handle.close()
					
		
	else:
		raise AssertionError("Debes introducir al menos una URI que apunte a un recurso con formato SW.")
