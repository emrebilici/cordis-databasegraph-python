# cordis-databasegraph-python
This project include two python files: databasewriting.py and creatinggraph.py

databasewriting.py is parsing the cordis projects webpage and getting informations about projects. Then, this informations is writing a database with postgresql.

creatinggraph.py is basically creating a networkx graph. This graph gets its informations from database.

## Getting Started
First you should install python3.x.

And you should postgresql.

Unless you have some library, you should install them.

For databasewriting.py

- BeautifulSoup
- psycopg2
- requests
- networkx
- re

For creatinggraph.py

- json
- json_graph
- psycopg2
- networkx

You can install with pip these libraries 

```
pip install psycopg2
```
for other libraries:
```
pip install [libraryname]
```

## Introduction to databasewriting.py
After created a database with postgresql then we connect to database.
```python
try:
    conn = psycopg2.connect(database = "deneme", user = "postgres", host = "localhost", password ="1478")
except:
    print("unable to connect")
```

While we try to do something with database, we use cursor:

```python
cur = conn.cursor()
```
Now we can use ```cur``` for database operation.

 **My code first create tables. If database have already these table, you should delete create table rows**
```python
cur.execute("CREATE TABLE COMPANY ( ID SERIAL PRIMARY KEY, CONAME TEXT, CO_COUNTRY TEXT, CO_ACTIVITY text, unique(coname) );")
cur.execute("CREATE TABLE PROJECTS ( name TEXT, call TEXT, coordinatorname TEXT, topic text, totalcost bigint, eucontribution bigint, fundingscheme text, recordno INT PRIMARY KEY, country TEXT, lastupdate DATE, project_text TEXT);")
cur.execute("CREATE TABLE PROJECTS_COMPANY (PRO_ID INT REFERENCES PROJECTS(recordno), COMPANY_ID INT REFERENCES COMPANY(ID), unique(pro_id, company_id)) ;")
```
### Parsing and writing to database 




