#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
	Prácticas de Python DB-API 2.0 (PEP-249) y bases de datos biológicas
	Script de inserción de entradas en formato SWISSPROT en la base de datos
'''

from __future__ import print_function
import sys
import io
import re
import sqlite3 as dbi

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
				
				# Impresión de comprobación
				print("ACC: {0} ; ID: {1} ; Last: {2}".format(acc[0],id,lastdate))
				
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
	if len(sys.argv)>2:
		dbfile=sys.argv[1]
		# Apertura de la conexión con la base de datos
		try:
			conn = dbi.connect(dbfile)
			# Esto sirve para que cada sentencia se ejecute inmediatamente
			#conn.autocommit = True
		except dbi.Error as e:
			print("Ha habido un problema al conectar a la base de datos: ",e.diag.message_primary,file=sys.stderr)
			raise
		
		# Procesamiento de cada fichero
		with conn:
			for filename in sys.argv[2:]:
				# Estamos abriendo el fichero con el encoding 'latin-1'
				# Para text mining lo recomendable es el encoding 'utf-8'
				with io.open(filename,'r',encoding="latin-1") as filehandle:
					print("Procesando fichero ",filename)
					try:
						# Obtención de un cursor para enviar operaciones a la base de datos
						cur = conn.cursor()
						for acc,id,lastdate,description,sequence,molw in SWParser(filehandle):
							# Preparación de las operaciones de inserción a realizar repetidamente
							# (Debería hacer un chequeo aquí, para comprobar que funcionan)
							cur.execute('INSERT INTO SWISSENTRY VALUES (?,?,?,?,?,?)',(acc[0],id,lastdate,description,sequence,molw))
							for accnumber in acc:
								cur.execute('INSERT INTO ACCNUMBERS(main_accnumber,accnumber) VALUES (?,?)',(acc[0],accnumber))
					except dbi.Error as e:
						print("Error al insertar en la base de datos: ",e.args[0],file=sys.stderr)
						raise
					except IOError as e:
						print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
						#raise
					except:
						print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
						raise
		
	else:
		raise AssertionError("Debes introducir una base de datos y al menos un fichero con formato SW.")
