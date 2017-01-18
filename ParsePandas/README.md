Parsing a table with Pandas
===========================

We are going to use as input ClinVar database in tabular format.

The table is available at ClinVar FTP site ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/, with the name variant_summary.txt.gz : ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz

We are going to write two programs to get the variants from an specific gene in genome assembly GRCh37, one using [Pandas](http://pandas.pydata.org/)

For the task we need to look at the columns Assembly, GeneSymbol, ClinicalSignificance, PhenotypeIDS, Chromosome, Start, Stop, Type, ReferenceAllele, AlternateAllele
