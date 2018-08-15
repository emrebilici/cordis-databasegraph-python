import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json


try:
    conn = psycopg2.connect(database = "deneme", user = "postgres", host = "localhost", password ="1478")
except:
    print("unable to connect")

cur = conn.cursor()
G = nx.Graph()
sayi =0
"""
Select count(*) From PROJECTS
Select distinct(pid) From Proejcts
"""
cur.execute("Select Distinct pro_id from projects_company")
projeler = cur.fetchall()
cur.execute("select distinct call from projects")
call_list = cur.fetchall()
project_list = []
callicin =[]

for k in call_list:
    co_list =[]
    cur.execute("select recordno from projects where call='{0}'".format(k[0]))
    projects_from_call = cur.fetchall()
    for i in projects_from_call:
        cur.execute("SELECT DISTINCT COMPANY_ID FROM PROJECTS_COMPANY WHERE PRO_ID='{0}'".format(i[0]))
        companies = cur.fetchall()
        for element in companies:
            co_list.append(element[0])
     
    callicin.append({"value": k[0], "co_nodes": co_list })


for i in projeler:
    """
    cur.execute("SELECT PRO_ID FROM PROJECTS_COMPANY WHERE NUM='{0}'" .format(sayi))
    pro_id = cur.fetchone()
    """
    cur.execute("SELECT DISTINCT COMPANY_ID FROM PROJECTS_COMPANY WHERE PRO_ID='{0}'".format(i[0]))
    com = cur.fetchall()
    
    cur.execute("select name,call,topic,totalcost,eucontribution, fundingscheme, project_text from projects where recordno='{0}'".format(i[0]))
    pro_det = cur.fetchall()
    project_list.append({"pro_rec_no": i[0], "value": pro_det[0][0], "totalcost": pro_det[0][3], "EUcontribution": pro_det[0][4],"call": pro_det[0][1],"topic":pro_det[0][2] ,"fundscheme": pro_det[0][5], "project_text": pro_det[0][6] })
        
    
    pro_nodes_list = []
    count = 0
    for j in com:
        pro_nodes_list.append(com[count][0])
        project_list[sayi]["pro_nodes"] = pro_nodes_list
        count2=0
        cur.execute("select coname from company where id='{0}'".format(com[count][0]))
        coname1 = cur.fetchone()
        cur.execute("select co_country from company where id='{0}'".format(com[count][0]))
        co_country = cur.fetchone()
        cur.execute("select co_activity from company where id='{0}'".format(com[count][0]))
        co_activity = cur.fetchone()
        cur.execute("select count (*) from projects_company where company_id='{0}';".format(com[count][0]))
        bulunma_sayisi = cur.fetchone()

        cur.execute("select pro_id from projects_company where company_id='{0}';".format(com[count][0]))
        pro_resp_to_company = cur.fetchall()
        baglanti_sayisi=0
        for k in pro_resp_to_company:
            cur.execute("select count (*) from projects_company where pro_id='{0}';".format(k[0]))
            baglanti = cur.fetchone()
            baglanti_sayisi += baglanti[0]-1
            
            
        
        G.add_node(com[count][0], data= com[count][0], value = coname1[0], country = co_country[0], activity = co_activity[0] ,kackez = bulunma_sayisi[0], baglanti= baglanti_sayisi)
        
        
        for i in com:
            if com[count][0] != com[count2][0]:
                if G.has_edge(com[count][0], com[count2][0]):
                    G[com[count][0]][com[count2][0]]['weight'] += 1
                else:
                    G.add_edge(com[count][0], com[count2][0], weight=1)
            else :
                """G.add_node(com[count][0], kackez = nx.get_node_attributes(G,"kackez")[com[count][0]] + 1 )"""
                                
            count2 = count2 +1
        count = count +1
        
    sayi+=1
    
    
    
pos = nx.spring_layout(G)           
labels = nx.get_edge_attributes(G,'weight')
nx.draw(G,pos)
nx.draw_networkx_edge_labels(G,pos,edge_labels = labels)

data = json_graph.node_link_data(G)

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r- m

    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0 , n1):
        L[i] = arr[l + i]
 
    for j in range(0 , n2):
        R[j] = arr[m + 1 + j]
 
    i = 0    
    j = 0     
    k = l    
 
    while i < n1 and j < n2 :
        if L[i]['data'] <= R[j]['data']:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
 

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
 
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr,l,r):
    if l < r:
 
        # Same as (l+r)/2, but avoids overflow for
        # large l and h
        m = (l+(r-1))//2
 
        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)
        
mergeSort(data['nodes'],0,len(data['nodes'])-1)
data["projects"] = project_list
data["pro_codes"] = callicin

with open("deneme.json", "w") as outfile:
    json.dump(data, outfile)

