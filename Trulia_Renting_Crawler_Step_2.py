import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import json
import time
import random

ua_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',}
url = "https://www.trulia.com/for_rent/Los_Angeles,CA/0-3000_price/lg_dogs,sm_dogs_pets/"
State, City, Address, Aptnum, BD, BA, Sqft, Price = [], [], [], [], [], [], [], []
for i in range(1,104):
    newurl = url + str(i)+ "_p/"
    html=rq.get(newurl,headers=ua_header)
    time.sleep(random.random()*5)
    soup = BeautifulSoup(html.text, "html.parser")

    div_target = soup.find_all("div",{"data-testid":"search-result-list-container"})
    print("Page_{0}_complete".format(i))

    for j in range(0,30):
        try:
            info = div_target[0].find("div",{"data-testid":"srp-home-card-{0}".format(j)})
        except Exception:
            break
        try:
            Price.append(info.find("div",{"data-testid":"property-price"}).text)
        except Exception:
            Price.append("NULL")
        try:
            BD.append(info.find("div",{"data-testid":"property-beds"}).text)
        except Exception:
            BD.append("NULL")
        try:
            BA.append(info.find("div",{"data-testid":"property-baths"}).text)
        except Exception:
            BA.append("NULL")
        try:
            Sqft.append(info.find("div",{"data-testid":"property-floorSpace"}).text)
        except Exception:
            Sqft.append("NULL")
        try:
            Address.append(info.find("div",{"data-testid":"property-street"}).text)
        except Exception:
            Address.append("NULL")
        try:
            City.append(info.find("div",{"data-testid":"property-region"}).text)
        except Exception:
            City.append("NULL")




#    print("\n",info,"\n",info.replace("- $", "- ").split("$")[1].split("/mo")[0])
#    Price.append(info.replace("- $", "- ").split("$")[1].split("/mo")[0])
#    BD.append(info.split("/mo")[1].split("bd")[0].split("1ba")[0])
#    print(info.split("/mo")[1].split("bd")[0].split("1ba")[0])

#    print(info.split("bd")[1].split("ba")[0])
#for div in div_target.children:
#    print(div, "\n", "\n")
#    info = div.find_all("div",{"data-testid":"srp-home-card-{0}".format(i)})
#    i += 1
#    for div in info:
#        print(div.text,"\n")

data = pd.DataFrame({'City':City,
                     'Address':Address,
                     'BD':BD,
                     'BA':BA,
                     'Sqft':Sqft,
                     'Price':Price})

data.to_csv('Trulia_renting_house_8.csv',encoding='utf8')