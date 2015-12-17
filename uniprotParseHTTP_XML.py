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
import xml.dom.minidom
from xml.dom.minidom import Node

UNIPROT_NS = "http://uniprot.org/uniprot"

def getTextContentFromElement(el):
	content = ''
	for child in el.childNodes:
		if child.nodeType == Node.TEXT_NODE or child.nodeType == Node.CDATA_SECTION_NODE:
			content += child.data
	
	return content

class SWParserXML(object):
	def __init__(self,filehandle):
		self.document = xml.dom.minidom.parse(filehandle)
	
	def __iter__(self):
		# Para poder iterar entre entrada y entrada, usamos un iterador
		self.entries = iter(self.document.getElementsByTagNameNS(UNIPROT_NS,"entry"))
		
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
		for xml_entry in self.entries:
			# Obtención de los accession numbers
			id = getTextContentFromElement(xml_entry.getElementsByTagNameNS(UNIPROT_NS,"name").item(0))
			acc = list(map(lambda acc_el: getTextContentFromElement(acc_el), xml_entry.getElementsByTagNameNS(UNIPROT_NS,"accession")))
			lastdate = xml_entry.getAttribute('modified')
			description = ', '.join(map(lambda full_el: getTextContentFromElement(full_el), xml_entry.getElementsByTagNameNS(UNIPROT_NS,"fullName")))
			sequenceNode = xml_entry.getElementsByTagNameNS(UNIPROT_NS,"sequence").item(0)
			sequence = getTextContentFromElement(sequenceNode)
			molw = sequenceNode.getAttribute('mass')
			
			return acc,id,lastdate,description,sequence,molw
			
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
				for acc,id,lastdate,description,sequence,molw in SWParserXML(uri_handle):
					
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
		raise AssertionError("Debes introducir al menos una URI que apunte a un recurso con formato UniProt XML.")
