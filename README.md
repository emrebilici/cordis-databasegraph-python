# cordis-databasegraph-python
This project include two python files: databasewriting.py and creatinggraph.py

databasewriting.py is parsing the cordis projects webpage and getting informations about projects. Then, this informations is writing a database with postgresql.

creatinggraph.py is basically creating a networkx graph. This graph gets its informations from database.

## Getting Started
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

You can install with pip 

'''
pip install psycopg2
'''

'''
pip install libraryname
'''
