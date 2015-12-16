#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Prácticas de Python 2.7 y bases de datos biológicas
	Programa pdbParse.py (parseado de ficheros PDB)
	Máster en Bioinformática y Biología Computacional, ENS-ISCIII
	Curso: 2015-2016
	Asignatura: Big Data Parsing and Processing
	Autor: José María Fernández
'''

from __future__ import print_function
import sys
import re
import subprocess
import time

'''
Tabla de correspondencia entre los códigos IUPAC de aminoácidos
formato 3 letras, a códigos de 1 letra. No incluye aminoácidos
exóticos o infrecuentes como p.ej. selenocisteína o selenometionina
'''
three2one = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'ASX': 'B',
    'CYS': 'C',
    'GLU': 'E',
    'GLN': 'Q',
    'GLX': 'Z',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V'
}

class PDBParser(object):
	def __init__(self,filenames):
		self.filenames = filenames
	
	def __iter__(self):
		# Hacemos un iterador, para no perder la posición
		self.files = iter(self.filenames)
		
		return self
	
	#def __next__(self):
	def next(self):
		for filename in self.files:	
			# Si se pone el comando a ejecutar en una sola línea, sin array, hay que poner shell=True
			pdb = subprocess.Popen(['gunzip','-c',filename],stdout=subprocess.PIPE,universal_newlines=True)
			print("Procesando fichero ",filename)
		
			try:
				# Inicialización de variables
				pdbid = None
				pdbdate = None
				title = ''
				compndBuff = ''
				isCompnd = False
				
				# Vamos a guardar las moléculas en un array
				# aunque se podrían guardar sin problemas en un hash
				pdbmolecule = []
				
				# Las cadenas las vamos a guardar en otro hash separado,
				# para poder almacenar fácilmente la secuencia y las referencias
				# de forma anidada
				pdbchain = {}
				
				# Estructura alternativa, sin anidamiento
				# pdbchainSeqs = {}
				# pdbchainAccs = {}
				
				# ¡A leer el fichero PDB!
				for line in pdb.stdout:
					line = line.rstrip('\n')

					# Detección usando expresión regular
					if re.search('^HEADER ',line) is not None:
						###########################################################
						# Estilo que seguiríamos si no tuviéramos manuales de PDB #
						###########################################################
						line = line.rstrip()
						
						tok = re.split(r"[ \t]+",line)
						
						pdbid = tok[-1]
						pdbdate = tok[-2]
						
						########################################
						# Estilo siguiendo los manuales de PDB #
						########################################
						# pdbid = line[62:66]
						# pdbdate = line[50:59]
						
					# Detección usando index (recomendable para búsqueda de
					# patrones exactos en ficheros de varios GB)
					elif line.startswith('TITLE '):
						#######################################
						# Estilo usando expresiones regulares #
						#######################################
						# titlematch = re.search(r"^TITLE +[0-9]*( ?.*[^ ]) *$",line)
						# title += titlematch.group(1)
						
						line = line.rstrip()
						title += line[10:]
					elif line.startswith('COMPND '):
						# Como COMPND tiene sub-registros e información
						# distribuídos en varias líneas, mejor ir guardando
						# todo en una variable para más tarde procesarlo
						
						# Así se pasa de
						#
						# COMPND    MOL_ID: 1;                                                            
						# COMPND   2 MOLECULE: MOLYBDENUM COFACTOR BIOSYNTHESIS PROTEIN A;                
						# COMPND   3 CHAIN: A, B;                                                         
						# COMPND   4 SYNONYM: MOAA;                                                       
						# COMPND   5 ENGINEERED: YES                                                      
						#
						# a
						#
						# MOL_ID: 1; MOLECULE: MOLYBDENUM COFACTOR BIOSYNTHESIS PROTEIN A; CHAIN: A, B; SYNONYM: MOAA; ENGINEERED: YES
						
						
						isCompnd = True
						line = line.rstrip()
						
						compndBuff += line[10:]
					else:
						# Vamos a procesar lo que venía de COMPND
						if isCompnd:
							# Pero, ¡sólo una vez!
							isCompnd = False
						
							# Cada sub-registro de molécula empieza con MOL_ID
							mol = compndBuff.split('MOL_ID: ')
							for moltok in mol:
								# Saltamos posibles elementos vacíos
								if moltok == '':
									continue
								
								# Cada línea tiene el MOL_ID, un MOLECULE y un CHAIN
								molmatch = re.search(r"^([0-9]+); MOLECULE: ([^;]+); CHAIN: ([^;]+)",moltok)
								
								# Obtengamos los nombres de las cadenas, que
								# van separadas por comas
								# y tal vez algún espacio
								chains = re.split(r"\s*,\s*",molmatch.group(3))
								
								# Con los nombres de cadena preparamos el terreno
								# para lo que leeremos más adelante, secuencia
								# y array de referencias a UniProt
								for chain in chains:
									pdbchain[chain] = {
										'seq': '',
										'accs': []
									}
									# Aquí podríamos haber usado hashes separados, uno
									# para la secuencia y otro para los accessions
									# en lugar de hashes anidados
									# pdbchainSeqs[chain] = ''
									# pdbchainAccs[chain] = []
								
								# Guardemos el moldid, su descripción, y las cadenas
								# en un hash
								pdbmolecule.append({'molid': molmatch.group(1),'moldesc': molmatch.group(2),'chains': chains})
	    
						# Las líneas SEQRES, que tienen el nombre de cadena y 
						# los resíduos a guardar
						# SEQRES   3 B  340  ARG CYS ASP TYR CYS MET PRO LYS GLU VAL PHE GLY ASP          
						seqmatch = re.search(r"^SEQRES +\d+ *([^ ]) *\d* ([^ ].*[^ ])",line)
						matched = seqmatch is not None
						
						dbmatch = None if matched else re.search(r"^DBREF +[^ ]+ ([^ ]) +\d+ +\d+ +UNP +([^ ]+)",line)
						
						if seqmatch is not None:
							chain = seqmatch.group(1)

							# Almacenamos en un array los resíduos
							residues = re.split(r" +",seqmatch.group(2))

							# Guardaremos aquí temporalmente la secuencia
							seqbuf = ''
							for residue in residues:
								# Detectemos si tenemos correspondencia
								# Si no la hay, almacenemos una X
								# Esto pasa con aminoácidos exóticos, con
								# resíduos que no son aminoácidos (ADN, ARN)
								# y algunas moléculas
								seqbuf += three2one.get(residue,'X')
							
							# para ir acumulándola en su sitio
							pdbchain[chain]['seq'] += seqbuf

							# alternativa
							# pdbchainSeqs[chain] += seqbuf
						# Y ahora, nos quedaremos con la cadena y el accession
						# pero sólo con los de UniProt
						# DBREF  1TV8 B    1   340  UNP    P65388   MOAA_STAAN       1    340
						elif dbmatch is not None:
							chain = dbmatch.group(1)
							acc = dbmatch.group(2)
							
							# Usamos un array porque podría haber más de un accession asociado
							# a una cadena (por ejemplo, en el caso de quimeras)
							pdbchain[chain]['accs'].append(acc)
							
							# alternativa
							# pdbchainAccs[chain].append(acc)
				
				# Al final devolvemos todo lo recopilado
				return pdbid,pdbdate,title,pdbmolecule,pdbchain
				
				# alternativa
				# return pdbid,pdbdate,title,pdbmolecule,pdbchainSeqs,pdbchainAccs
				
			except IOError as e:
				print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
				#raise
			finally:
				if pdb.returncode is None:
					# Primer intento de terminación, educado
					pdb.terminate()
					time.sleep(1)
					if pdb.returncode is None:
						# Segundo intento de terminación, forzado
						pdb.kill()
		
		# Se cierra la lista de ficheros procesado
		self.files = None
		# Y como hemos terminado, lo indicamos
		raise StopIteration
		
		
# Comprobación del número de parámetros de entrada
if __name__ == '__main__':
	if len(sys.argv)>1:
		# Procesamiento de cada fichero
		try:
			# alternativa
			# for pdbid,pdbdate,title,pdbmolecule,pdbchainSeqs,pdbchainAccs in PDBParser(sys.argv[1:]):
			for pdbid,pdbdate,title,pdbmolecule,pdbchain in PDBParser(sys.argv[1:]):
				# Aquí es donde tendremos que procesar, filtrar, imprimir ...
				print("PDB: {0} Date: {1} Title: {2}".format(pdbid,pdbdate,title))
				print("Mols ({0})".format(len(pdbmolecule)))
				
				# Aquí pondríamos el resto de datos
				for pdbmol in pdbmolecule:
					molid = pdbmol['molid']
					print("\tMOL ID: {0}".format(molid))
					# Ahora, ¡a por las cadenas!
					chains = pdbmol['chains']
					print("\tChains ({0})".format(len(chains)))
					
					for chain in chains:
						# Recuperamos el hash anidado
						chaindata = pdbchain[chain]
						
						seq = chaindata['seq']
						accs = chaindata['accs']
						
						# alternativa
						# seq = pdbchainSeqs[chain]
						# accs = pdbchainAccs[chain]
						
						# Aquí se procesaría cada dato
						print("\t\tAccessions: {0}".format(", ".join(accs)))
						print("\t\tSequence Length: {0}".format(len(seq)))
		except:
			print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
			raise
		
	else:
		raise AssertionError("Debes introducir al menos un fichero comprimido con formato PDB.")
