# Biological data parsing

Different python 2.7 examples for bioinformatic students, showing the advantages of putting all the parsing code in an iterator, abstracting from the origin:

0. Initial case, where the Uniprot SW parsing code is mixed with the program (program [uniprotParse-v0.py](uniprotParse-v0.py))

  ```bash
  python2 uniprotParse-v0.py samples/UniProt-Sample.txt
  ```

1. Uniprot SW parsing code has been moved to an iterator class (program [uniprotParse.py](uniprotParse.py)):

  ```bash
  python2 uniprotParse.py samples/UniProt-Sample.txt
  ```

2. Variant from previous script, where file opening is done outside the iterator (program [uniprotParse-alt.py](uniprotParse-alt.py))):

  ```bash
  python2 uniprotParse-alt.py samples/UniProt-Sample.txt
  ```

3. Variant from previous script, which parses compressed file (program [uniprotParseCompressed.py](uniprotParseCompressed.py)):

  ```bash
  gzip -9c samples/UniProt-Sample.txt > samples/UniProt-Sample.txt.gz
  python2 uniprotParseCompressed.py samples/UniProt-Sample.txt.gz
  ```

4. Variant from previous script, which parses network resource (program [uniprotParseHTTP.py](uniprotParseHTTP.py)):

  ```bash
  python2 uniprotParseHTTP.py http://www.uniprot.org/uniprot/Q2K3L7.txt
  ```
  
  If you want to test with a random UniProt SW entry from human, open next link in your browser: [http://www.uniprot.org/uniprot/?query=reviewed:yes&random=yes](http://www.uniprot.org/uniprot/?query=reviewed:yes+AND+organism:9606&random=yes)
  
  and then copy the full URL, adding `.txt` suffix.
  
  If you want to test with a random UniProt TrEMBL entry, open next link in your browser: [http://www.uniprot.org/uniprot/?query=reviewed:no&random=yes](http://www.uniprot.org/uniprot/?query=reviewed:no&random=yes)
  
  and then copy the full URL, adding `.txt` suffix.

5. Script which parses a UniProt XML network resource using DOM (program [uniprotParseHTTP_XML.py](uniprotParseHTTP_XML.py)):

  ```bash
  python2 uniprotParseHTTP_XML.py http://www.uniprot.org/uniprot/Q2K3L7.xml
  ```

6. Getting JSON content from internet, and parsing, using next official example from Ensembl: [https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client](https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client)

7. Parsing something more complex, like a PDB file (program [pdbParse.py](pdbParse.py)). Uncompression is done using an external program, showing the design pattern of fetching the content from a program:

  ```bash
  python2 pdbParse.py samples/2Q5W.pdb.gz
  ```
