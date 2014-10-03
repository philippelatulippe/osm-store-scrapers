import nominatim
import sqlite3
from bs4 import BeautifulSoup
from time import sleep

sql = sqlite3.connect("deutschebank.sqlite3")
sql.row_factory = sqlite3.Row
cursor = sql.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS BranchPOI(id TEXT, place_id TEXT,"
            "data TEXT)")


nom = nominatim.Nominatim()


branches = cursor.execute("SELECT id FROM BranchInfo GROUP BY id")

for branch_id_row in branches:
    branch_id = branch_id_row[0]

    cursor2 = sql.cursor()
    
    attributes = cursor2.execute("SELECT * FROM BranchInfo WHERE id=?",
                                 [branch_id])

    branch = {}

    for attribute in cursor2:
        branch[attribute["detail"]] = attribute["value"]

    if branch.get("House Address"):
        #When I checked, all branches had a "House Address"
        address = branch.get("House Address").replace("\n",", ")

        print(address)

        if address.find("look under") >= 0:
            continue

        curpoi = sql.cursor()
    
        existing_data = cursor2.execute("SELECT * FROM BranchPOI WHERE id=?",
                                        [branch_id]).fetchone()

        if existing_data and existing_data["place_id"]:
            print("already found")
            continue

        places = nom.query(address);

        for place in places:
            if place["type"].find("bank") >= 0:
                print "found a bank"
            else:
                continue

            if place["display_name"].find("Deutsche Bank")

        sql.execute("REPLACE INTO BranchPOI VALUES(?,?,?) WHERE id = ?",
                    (branch_id, place_id, nomdata, branch_id))
        
        print("==========================================")
        sleep(1.0)
    




