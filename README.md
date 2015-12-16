# Biological data parsing

Different python 2.7 examples for bioinformatic students, showing the advantages of putting all the parsing code in an iterator, abstracting from the origin:

1. Uniprot SW format from a file (program [uniprotParse.py](uniprotParse.py)):

  ```bash
  python2 uniprotParse.py samples/UniProt-Sample.txt
  ```

2. Variant from previous script (program [uniprotParse-alt.py](uniprotParse-alt.py))):

  ```bash
  python2 uniprotParse-alt.py samples/UniProt-Sample.txt
  ```

3. Parsing compressed file (program [uniprotParseCompressed.py](uniprotParseCompressed.py)):

  ```bash
  gzip -9c samples/UniProt-Sample.txt > samples/UniProt-Sample.txt.gz
  python2 uniprotParseCompressed.py samples/UniProt-Sample.txt.gz
  ```

4. Parsing network resource (program [uniprotParseHTTP.py](uniprotParseHTTP.py)):

  ```bash
  python2 uniprotParseHTTP.py http://www.uniprot.org/uniprot/Q2K3L7.txt
  ```

5. Getting JSON content from internet, and parsing, using next official example from Ensembl: [https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client](https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client)

6. Parsing something more complex, like a PDB file (program [pdbParse.py](pdbParse.py)). Uncompression is done using an external program, showing the design pattern of fetching the content from a program:

  ```bash
  python2 pdbParse.py samples/2Q5W.pdb.gz
  ```
