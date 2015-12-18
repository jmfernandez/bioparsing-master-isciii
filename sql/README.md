Inserting in a SQL database
===========================

If the extraction of content requires inserting your data in a relational database, you need to write some additional code, like the connection to the database and the sentences to insert the data. In Python, all the database drivers must adhere to DB-API 2.0 standard.

This directory contains just an example of that task using a variation of the parsing code from the example programs in the parent directory.

For SQLite database loading example, we use `sqlite3` shell, a database schema stored in [initial10.sql](initial10.sql) and the program [uniprotInsert-sqlite.py](uniprotInsert-sqlite.py)

```bash
# Let's create the database in the file swissentries.db
# from its definition in initial10.sql
sqlite3 swissentries.db < initial10.sql
# Now, let's insert all the entries in [../samples/UniProt-Sample.txt](../samples/UniProt-Sample.txt)
python2 uniprotInsert-sqlite.py swissentries.db ../samples/UniProt-Sample.txt
# You can check the contents of SWISSENTRY table with this command
echo 'SELECT * FROM SWISSENTRY;' | sqlite3 swissentries.db
```
