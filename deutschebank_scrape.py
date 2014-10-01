#Python 3, BeautifulSoup4

from bs4 import BeautifulSoup
import urllib.request
import time

import sqlite3

url_countries = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=countries&_="

url_cities = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=cities&country=%s&_="

url_branches = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=branches&country=%s&city=%s&_="

url_branch ="https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=division&id=%s&_="



debugging = True
def info(*args, **blargs):
    if debugging:
        print(*args, **blargs)



sql = sqlite3.connect('deutschebank.sqlite3')
cursor = sql.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS BranchInfo(id TEXT, detail TEXT, "
            "value TEXT)")


def scrape_branch_info(branch_id):
    info("Scraping branch ID " + branch_id)

    req_branch = urllib.request.urlopen(url_branch % branch_id)
    data_branch = req_branch.read().decode('utf-8')
    xml_branch = BeautifulSoup(data_branch,features="xml")

    element_branch = xml_branch.find_all("element")
    if len(element_branch) > 0 :
        html_branch = BeautifulSoup(element_branch[0].getText())

        table_branch = html_branch.find("table")
        rows_branch = table_branch.find_all("tr", recursive=False)

        info("(")
        collecting_data = False
        for row in rows_branch:
            cols = row.find_all("td")
            left = cols[0]
            right = cols[1]

            #don't collect data for specialized offices
            if collecting_data and left.find(attrs={"class":"table_hl"}):
                break

            left_text = ""
            for string in left.stripped_strings:
                left_text = left_text+ string.replace("\u00A0"," ")
                info(left_text, end="")

            info("---->",end="")
    
            right_text = ""
            right_table = right.find("table")
            if right_table:
                right_text = right.decode_contents()
            else:
                for string in right.stripped_strings:
                    right_text = right_text + string.replace("\u00A0"," ") + "\n"

            info(right_text)

            if len(right_text) > 0 and len(left_text) > 0:
                collecting_data = True
                cursor.execute("INSERT INTO BranchInfo VALUES(?,?,?)",
                                (branch_id, left_text, right_text));

            info()
        info(")")

            


##complex example
#scrape_branch_info("73222")
#sql.commit()
#sql.close()    
#exit()

req_countries = urllib.request.urlopen(url_countries)
data_countries = req_countries.read().decode('utf-8')
xml_countries = BeautifulSoup(data_countries,features="xml")

country_ids = xml_countries.find_all("value")

for country_node in country_ids:
    country_id = country_node.getText()
    
    info("Country: "+country_id)

    req_cities = urllib.request.urlopen(url_cities % country_id)
    data_cities = req_cities.read().decode('utf-8')
    xml_cities = BeautifulSoup(data_cities,features="xml")
    
    city_ids = xml_cities.find_all("value")

    for city_node in city_ids:
        city_id = city_node.getText()

        info("-> city "+city_id)

        req_branches = urllib.request.urlopen(url_branches % (country_id, 
                                              city_id))
        data_branches = req_branches.read().decode('utf-8')
        xml_branches = BeautifulSoup(data_branches,features="xml")
        
        branches_ids = xml_branches.find_all("value")
        
        for branch_node in branches_ids:
            branch_id = branch_node.getText()
            info("branch: "+branch_id)
            scrape_branch_info(branch_id)
            time.sleep(0.9)
            
        time.sleep(0.4)



    time.sleep(0.4)
