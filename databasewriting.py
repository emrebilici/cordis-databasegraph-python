import networkx as nx
import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import time
import matplotlib.pyplot as plt



try:
    conn = psycopg2.connect(database = "deneme", user = "postgres", host = "localhost", password ="1478")
except:
    print("unable to connect")

cur = conn.cursor()

cur.execute("CREATE TABLE COMPANY ( ID SERIAL PRIMARY KEY, CONAME TEXT, CO_COUNTRY TEXT, CO_ACTIVITY text, unique(coname) );")
cur.execute("CREATE TABLE PROJECTS ( name TEXT, call TEXT, coordinatorname TEXT, topic text, totalcost bigint, eucontribution bigint, fundingscheme text, recordno INT PRIMARY KEY, country TEXT, lastupdate DATE, project_text TEXT);")
cur.execute("CREATE TABLE PROJECTS_COMPANY (PRO_ID INT REFERENCES PROJECTS(recordno), COMPANY_ID INT REFERENCES COMPANY(ID), unique(pro_id, company_id)) ;")

start_time = time.time()

co_idint = 0
l = 0
""" YOU CAN ADJUST FROM HERE THE URL to reach more detailed projects. WEBSITE ALLOWS YOU EDIT QUERY LIKE 'programme/code=H2020' ."""
""" Check the website and look at 'edit query' which is on the left of the page.  """
first_url = "https://cordis.europa.eu/projects/result_en?q=programme/code=H2020+AND+contenttype=project&srt=contentUpdateDate%3Adecreasing&num=100"
num_co = 0
company =[]

while (l<50):
    
    m2 = []
    project_list = []
    i = 0
    j = 0
    
    participants = []
    
    l = l+1 
    first_url = first_url + "&p=" +str(l)

    source = requests.get(first_url, verify = True).text
    soup = BeautifulSoup(source, "lxml")
    
    souplist = soup.findAll("div", {"class" : "js-booklet-link-add"})

    m = re.findall("project_......+?_en", str(souplist))
    m = m[::2]
    for k in m:
        m1 = str(m[i]).split("project_")
        m2.append(m1[1])
        i=i+1

    for b in m2:	
	    project_list.append("https://cordis.europa.eu/project/rcn/"+m2[j])
	    j = j+1

    n=0
    
    proje_num = 1
    project_record_no = []
    for k in project_list:
        liste = []
        """partner_list=[]"""
        num_co = num_co + 1
        
        m3 = str(m2[n]).split("_en")
        project_record_no.append(m3[0])
        
        project_source = requests.get(project_list[n]).text
        project_soup = BeautifulSoup(project_source, "lxml")
        project_header = project_soup.select("div h1" )[1].text
        project_name = project_soup.select("div h2")[0].text
        
        """project_cost = project_soup.find("div" , {"class":"box-left"}).text"""
        """coo means coordinator name"""
        coo = project_soup.findAll("div", {"class": "name"})[0].text
        coo = coo.split("Participation ended")
        coo = coo[0]
        co_activity_type = project_soup.findAll("div", {"class": "contact"})[0].text
        parti_activity_type = project_soup.findAll("div", {"class": "contact"})[0:]
        parti_country = project_soup.findAll("div", {"class": "country"})[0:]
        """buradan itibaren administrative contactı atıyorum cunku activity typeı
        bulmam buna bagli.  contact class ların icini geziyorum ve bu fazla geliyo
        """
        for k in project_soup.findAll("div", {"class": "contact"})[0:]:
            if re.match("Administrative contact:+? ", k.text):
                k.extract()
        parti_activity_type = project_soup.findAll("div", {"class": "contact"})[0:]

        """attık"""
        

        """buradan sonra bos olan name classları atıyorum"""
        for k in project_soup.findAll("div", {"class":"name"})[0:]:
            if len(k.text)==0:
                k.extract()
        parti = project_soup.findAll("div", {"class":"name"})[0:]
        """attık"""

        project_text = project_soup.findAll("div", {"class": "tech"})[0].text
        project_text = project_text.split("\n")
        project_text = project_text[1]

        callforpro = project_soup.find("div", {"class":"box-right"}).text
        callfor = callforpro.split("Call for proposal:")
        call = callfor[1].split("See other projects for this call")
        call = call[0]
        call = call.replace("'","''")

        fund_scheme = callforpro.split("Funding scheme:")
        fundingscheme = fund_scheme[1]
        fundingscheme= fundingscheme.replace("'","''")

        protopic = callfor[0].split("Topic(s): ")
        topic1 = protopic[1].split("\n")
        topic = topic1[1]
        topic = topic.replace("'","''")
        
        
        eucontribution = project_soup.find("div", {"class":"box-left"}).text
        pro_contribution = eucontribution.split("EU contribution:")
        pro_cont1 = pro_contribution[1].split("\n")
        pro_cont = pro_cont1[0].split("EUR ")
        pro_cont = pro_cont[1].replace(" ","")
        pro_cont = pro_cont.split(",")
        pro_cont = pro_cont[0]

        p_totalcost = eucontribution.split("Total cost:")
        totalcost1 = p_totalcost[1].split("\n")
        totalcost= totalcost1[0].split("EUR ")
        totalcost = totalcost[1]
        totalcost = totalcost.replace(" ", "")
        totalcost = totalcost.split(",")
        totalcost = totalcost[0]
        
        

        count = 0

        for k in parti:
            parti[count] = parti[count].text
            participantname = parti[count].split("Participation ended")
            parti[count] = participantname[0]
            parti_country[count] = project_soup.findAll("div", {"class": "country"})[count].text
            parti_activity_type[count] = parti_activity_type[count].text
            parti_activity_split = parti_activity_type[count].split("Activity type: ")
            parti_activity_type[count] = parti_activity_split[1]
            
            count = count + 1

            
        parti_contribution = project_soup.findAll("p", {"class": "partipant-contribution"})[0:]
        count1 = 0

        for k in parti_contribution:
            parti_contribution[count1] = parti_contribution[count1].text
            parti_contribution[count1] = parti_contribution[count1].split("EU contribution: EUR ")
            parti_contribution[count1][1] = parti_contribution[count1][1].replace(" ", "")
            parti_contribution[count1][1] = parti_contribution[count1][1].replace(",","")
            count1 = count1 + 1
            
            
        contribution = project_soup.findAll("p", {"class": "partipant-contribution"})[0].text
        """cont = re.findall("\d+", contribution)
        cont_str = cont["""
 
        
        country = project_soup.findAll("div", {"class": "country"})[0].text
        """eu contribution da integer olarak almıyosun. onu ayırman lazım. yukarıda denemiştim"""
        
        last_upd = project_soup.find("p", {"class" : "hidPdf"}).text
        last_up = last_upd.split("\nLast updated on: ")
        lastupdate = last_up[1].split("    ")
        
        """last_up = re.findall("..........+?    ", last_update)"""
        
        
        """coordinatornameden ve projectnameden quoteleriatıyorum yoksa yine hata veriyor"""
        coo = coo.replace("'", "''")
        project_name = project_name.replace("'","''")
        project_text = project_text.replace("'","''")
        cur.execute("insert into projects ( name, call, coordinatorname, topic, totalcost, eucontribution, fundingscheme, recordno, country, lastupdate, project_text) values('{0}','{1}',quote_literal('{2}'), '{3}','{4}','{5}','{6}','{7}','{8}', '{9}', '{10}') on conflict (recordno) do nothing;" .format(project_name, call, coo, topic, totalcost, pro_cont, fundingscheme, project_record_no[n], country, lastupdate[0], project_text))
        


        """burada kıyaslama yapıp yoksa company liste atıyorum ve bir ID veriyorum"""
        count4 = -1
        sparti= []
        co_id = []
        for element in parti:
            element = element.replace("'","''")
            
            count4 = count4 + 1
            parti[count4] = parti[count4].replace("'","''")
            if element not in company:
                
                
                company.append(parti[count4])
                

                cur.execute("INSERT INTO COMPANY(CONAME, CO_COUNTRY, CO_ACTIVITY) VALUES('{0}', '{1}', '{2}') on conflict (coname) do nothing;" .format( parti[count4], parti_country[count4], parti_activity_type[count4]))
            
            
            cur.execute("INSERT INTO PROJECTS_COMPANY( PRO_ID, COMPANY_ID) VALUES ('{0}', (SELECT ID FROM COMPANY WHERE CONAME='{1}' limit 1)) on conflict (pro_id, company_id) do nothing ;".format( project_record_no[n], parti[count4] ))
      
        n= n+1
        conn.commit()
    
    print("%s" %(time.time()- start_time))
        
print("%s" %(time.time()- start_time))
