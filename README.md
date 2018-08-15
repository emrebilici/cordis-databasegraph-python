# cordis-databasegraph-python
This project include two python files: databasewriting.py and creatinggraph.py

databasewriting.py is parsing the cordis projects webpage and getting informations about projects. Then, this informations is writing a database with postgresql.

creatinggraph.py is basically creating a networkx graph. This graph gets its informations from database.

## Getting Started
First you should install python3.x.

And you should install postgresql.

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
For parsing the website, I assign the webpage url to ``` first_url ```

Since cordis project results has 50 pages, I use ```while(l<50)```

Every step of ```while```, I increase the page number with ```first_url = first_url + "&p=" +str(l)```

Below code in every page is taking the project record no and this allows us to go to the this project's webpage

```python
    source = requests.get(first_url, verify = True).text
    soup = BeautifulSoup(source, "lxml")
    
    """souplist includes all project record no in one page"""
    souplist = soup.findAll("div", {"class" : "js-booklet-link-add"})
    
    """m assigned to just number part of record no"""
    m = re.findall("project_......+?_en", str(souplist))
    m = m[::2]
    
    """this part is splitting from text part"""
    for k in m:
        m1 = str(m[i]).split("project_")
        m2.append(m1[1])
        i=i+1
    """at last project_list includes that all projects websites in one page"""
    for b in m2:	
	    project_list.append("https://cordis.europa.eu/project/rcn/"+m2[j])
	    j = j+1
```

```project_list``` includes all project websites in one page. So, I will use this with for loop to get specific information about one project.

Inside of the ```for k in project_list``` loop, I parsing the some information about project, and its companies. It means there are nested loops. 

Also, I insert the information about project, which I parse, into a database table named as projects 

In ```for element in parti``` loop, -```parti``` means the company list of the one project- I keep an permanent array ```company``` and it provides that checking the company has alredy added to database table. Since, one company can be associated more than one project. If one company is in the ```company``` list, it cant be added to database. 

In ```for element in parti``` loop, we write company informations -for one project- to database table named also as company.
```python
cur.execute("INSERT INTO COMPANY(CONAME, CO_COUNTRY, CO_ACTIVITY) VALUES('{0}', '{1}', '{2}') on conflict (coname) do nothing;" .format( parti[count4], parti_country[count4], parti_activity_type[count4]))
```
Above code show how company info writing to database. 

To avoid conflict about company in the database table, I use ```on conflict (coname)```.    

```on conflict(...)``` methods allows that.

Also in ```for element in parti``` loop, I insert the company id and project record no into ```projects_company``` table for company and project relation.  

## Images from Database
This is projects table: 
![alt text](https://github.com/emrebilici/cordis-databasegraph-python/blob/master/projects.JPG)

This is company table:
![alt text](https://github.com/emrebilici/cordis-databasegraph-python/blob/master/company.JPG)

This is projecst_company table:
![alt text](https://github.com/emrebilici/cordis-databasegraph-python/blob/master/projects_company.JPG)



