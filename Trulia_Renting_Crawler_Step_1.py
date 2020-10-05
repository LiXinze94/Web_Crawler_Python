import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import json

ua_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',}
url = "https://www.trulia.com/for_rent/Los_Angeles,CA/"

html=rq.get(url,headers=ua_header)
soup = BeautifulSoup(html.text, "html.parser")
State, City, Address, Aptnum, BD, BA, Sqft, Price = [],[],[],[],[],[],[],[]
for i, child in enumerate(soup.div.children):
    if i ==1:
        level1 = child
for i, child in enumerate(level1.children):
    if i ==1:
        level2 = child
for i, child in enumerate(level2.children):
    if i ==0:
        level3 = child
for i, child in enumerate(level3.children):
    if i ==0:
        level4 = child
for i, child in enumerate(level4.children):
    if i ==1:
        level5 = child
for i, child in enumerate(level5.children):
    try:
        Price.append(child.find('div',{'data-testid':'property-price'}).get_text())
    except Exception:
        Price.append("NULL")
    try:
        BD.append(child.find('div',{'data-testid':'property-beds'}).get_text())
    except Exception:
        BD.append("NULL")
    try:
        BA.append(child.find('div',{'data-testid':'property-baths'}).get_text())
    except Exception:
        BA.append("NULL")
    try:
        Sqft.append(child.find('div',{'data-testid':'property-floorSpace'}).get_text())
    except Exception:
        Sqft.append("NULL")
    try:
        Address.append(child.find('div',{'data-testid':'property-street'}).get_text())
    except Exception:
        Address.append("NULL")
    try:
        City.append(child.find('div',{'data-testid':'property-region'}).get_text())
    except Exception:
        City.append("NULL")

#for i in list(range(0,30)):
#    property = soup.findAll('div',{'data-testid':'srp-home-card-{0}'.format(i)})
#    print(property)
#for i, child in enumerate(level5.children):
#    if i ==0:
#        print(json.loads(child.find('script', {'type': 'application/ld+json'}).get_text()))
#    if i == 0:
#        info = json.loads(child.find('script', {'type': 'application/ld+json'}).get_text()).get("address").get("addressLocality").get("addressRegion").get("postalCode").get("streetAddress")
#        print("postalCode",info["address"]["postalCode"])
data = pd.DataFrame({'City':City,
                     'Address':Address,
                     'BD':BD,
                     'BA':BA,
                     'Sqft':Sqft,
                     'Price':Price})

data.to_csv('Trulia_renting_house.csv',encoding='utf8')