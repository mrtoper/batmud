#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import re
import sys
import nlconfig


def cleanseString(str):
    str = re.sub(r'\s+', ' ', str.strip())
    return re.sub(r'[^\x00-\x7F]+','', str)


def getTableByClass(className):
    tbl = soup.find("table", {"class" : className})

    th = tbl.find("thead")
    row = th.findAll("tr")[0]
    cols = row.findAll("th")
    cols = [cleanseString(ele.text) for ele in cols if ele and ele.get("class") != ["bid"]]
    
    table = []
    table.append(cols)
    
    rows = tbl.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        cols = [cleanseString(ele.text) for ele in cols if ele and ele.get("class") != ["number", "bid"]]
        table.append(cols)
    return table

def printTable(tbl):
    print "\n".join("\t".join(x) for x in tbl if x)

#check nlconfig
if (not (nlconfig.username and nlconfig.password)):
    print "Set nlconfig.username and nlconfig.password first"
    sys.exit()

#login to site, get pool page
r = requests.post(
    'https://www.bat.org/ss/batlogin2.php', 
    data = { 'username' : nlconfig.username, 'password' : nlconfig.password })
pool = r.text

soup = BeautifulSoup(pool, "lxml")

#current pool - bids
print "*** BIDS ***"
printTable(getTableByClass("bidded"))

#unbidded
print "*** POOL ***"
printTable(getTableByClass("unbidded"))
