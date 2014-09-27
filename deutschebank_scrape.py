#Python 3, BeautifulSoup4

from bs4 import BeautifulSoup
import urllib.request
import time

url_countries = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=countries&_="

url_cities = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=cities&country=%s&_="

url_branches = "https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=branches&country=%s&city=%s&_="

url_branch ="https://secure.deutsche-bank.de/cc/locationsfinder/en/xml.do?type=division&id=%s&_="




def scrape_branch_info(branch_id):
    req_branch = urllib.request.urlopen(url_branch % branch_id)
    data_branch = req_branch.read().decode('utf-8')
    xml_branch = BeautifulSoup(data_branch,features="xml")

    element_branch = xml_branch.find_all("element")
    if len(element_branch) > 0 :
        html_branch = BeautifulSoup(element_branch[0].getText())

        table_branch = html_branch.find("table")
        rows_branch = table_branch.find_all("tr", recursive=False)

        print("(")
        for row in rows_branch:
            cols = row.find_all("td")
            left = cols[0]
            right = cols[1]

            left_text = ""
            for string in left.stripped_strings:
                left_text = left_text+ string.replace("\u00A0"," "),end=""
                print(left_text)

            print("---->",end="")
    
            right_text = ""
            for string in right.stripped_strings:
                right_text = right_text + string.replace("\u00A0"," "))
                print(right_text)

            #Some branches have multiple offices and diff info for them, we
            #need to stop scraping when we find another tag with class=table_hl

            print()
        print(")")

            

    


#complex example
scrape_branch_info("73222")
exit()

req_countries = urllib.request.urlopen(url_countries)
data_countries = req_countries.read().decode('utf-8')
xml_countries = BeautifulSoup(data_countries,features="xml")

country_ids = xml_countries.find_all("value")

for country_node in country_ids:
    country_id = country_node.getText()
    
    print(country_id)

    req_cities = urllib.request.urlopen(url_cities % country_id)
    data_cities = req_cities.read().decode('utf-8')
    xml_cities = BeautifulSoup(data_cities,features="xml")
    
    city_ids = xml_cities.find_all("value")

    for city_node in city_ids:
        city_id = city_node.getText()

        print("-> "+city_id)

        req_branches = urllib.request.urlopen(url_branches % (country_id, 
                                              city_id))
        data_branches = req_branches.read().decode('utf-8')
        xml_branches = BeautifulSoup(data_branches,features="xml")
        
        branches_ids = xml_branches.find_all("value")
        
        for branch_node in branches_ids:
            branch_id = branch_node.getText()
            print("branch: "+branch_id)
            scrape_branch_info(branch_id)

        time.sleep(2)
