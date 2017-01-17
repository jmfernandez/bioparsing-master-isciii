#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
    Prácticas de Python 2.7 y bases de datos biológicas
    Script de parseado de ClinVar
    Máster en Bioinformática y Biología Computacional, ENS-ISCIII
    Curso: 2016-2017
    Asignatura: Big Data Parsing and Processing
    Autor: José María Fernández
'''

from __future__ import print_function
import sys
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        # El primer parámetro es el fichero de ClinVar
        # el segundo parámetro es el nombre del gen que vamos a buscar
        clinVarFile = sys.argv[1]
        geneName = sys.argv[2]

        try:
            clinvar = pd.read_table(clinVarFile)
            for index,row in clinvar.iterrows():
                assembly = row['Assembly']
                geneSymbol = row['GeneSymbol']
                if assembly == 'GRCh37' and geneSymbol == geneName:
                    varType = row['Type']
                    significance = row['ClinicalSignificance']
                    phenotypes = row['PhenotypeIDS']
                    chro = row['Chromosome']
                    start = row['Start']
                    stop = row['Stop']
                    refAllele = row['ReferenceAllele']
                    altAllele = row['AlternateAllele']
                    print("Gene {0}, varType {1}, chromosome {2}, start {3}, stop {4}, REF {5}, ALT {6}, significance {7}, phenotype ids {8}".format(geneSymbol, varType, chro, start, stop, refAllele, altAllele, significance, phenotypes))
        except IOError as e:
            print("Error de lectura de fichero {0}: {1}".format(e.errno, e.strerror),file=sys.stderr)
        except:
            print("Error inesperado: ", sys.exc_info()[0],file=sys.stderr)
            
            sys.exit(1)
    else:
        raise AssertionError("Debes introducir el fichero descargado de ClinVar y un nombre de gen")

