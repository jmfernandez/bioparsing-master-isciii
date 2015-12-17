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
from Bio import SeqIO

# Comprobación del número de parámetros de entrada
if __name__ == '__main__':
	if len(sys.argv)>1:
		# Procesamiento de cada fichero
		for filename in sys.argv[1:]:
			try:
				print("Procesando fichero ",filename)
				# SeqIO.parse admite nombres de fichero, manejadores de fichero, etc...
				# Los formatos soportados están documentados en
				# http://biopython.org/wiki/SeqIO#File_Formats
				# El formato de los registros obtenidos varía de formato a formato.
				# La documentación de los registros de SwissProt está disponible en
				# http://biopython.org/DIST/docs/api/Bio.SwissProt.Record-class.html
				for seq_record in SeqIO.parse(filename, "swiss"):
					# Como 'seq_record.id' sólo devuelve el primer accession
					# hay que recurrir a esto:
					acc = seq_record.annotations['accessions']
					id = seq_record.name
					lastdate = seq_record.annotations['date_last_annotation_update']
					description = seq_record.description
					# La secuencia es un objeto Seq de Biopython, que permite muchas operaciones
					sequence = str(seq_record.seq)
					# Esta información no la devuelve BioPython
					# molw =
					
					# Impresión de comprobación
					print("ACC: {0} ; ID: {1} ; Last: {2}".format(acc[0],id,lastdate))
					print("All accession numbers: ",', '.join(acc))
			except IOError as e:
				print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
				#raise
			except:
				print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
				raise
		
	else:
		raise AssertionError("Debes introducir al menos un fichero que apunte a un recurso con formato SW.")
