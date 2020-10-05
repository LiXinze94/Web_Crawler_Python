import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import json
import time
import random

def get_demand():
    global beds_num, min_price, max_price, price_tag, pet_friendly
    if input("Need filter? \n Enter 'Y' or 'N' \n") == 'N':
        beds_num = 'S'
        price_tag = ''
        pet_friendly = 'N'
    else:
        beds_num = input("How many beds you need? \n Enter 'S' for all type, '1,2,3,4' for beds \n")
        min_price = input("Set a min price: \n")
        max_price = input("Set a max price: \n")
        pet_friendly = input("Do you have pets? \n Enter 'C' for cats, 'D' for dogs, 'A' for all, 'N' for none \n")
        price_tag = '{0}-{1}_price/'.format(min_price, max_price)

def target_url(url):
    global beds_num, min_price, max_price, price_tag, pet_friendly, d_beds, d_pets
    new_url = url + d_beds[beds_num] + price_tag + d_pets[pet_friendly]
    return new_url

def get_data(t_url):
    ua_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36', }
    State, City, Address, Aptnum, BD, BA, Sqft, Price = [], [], [], [], [], [], [], []
    file_name = input("Input a file name: \n")

    hh = rq.get(t_url, headers=ua_header)
    time.sleep(random.random() * 5)
    ss = BeautifulSoup(hh.text, "html.parser")
    tar = ss.find_all("div", {"data-testid": "search-results-pagination"})
    t = tar[0].find("ul")
    for i, child in enumerate(t.children):
        if i == len(list(t.children)) - 2:
            max_page = child.text


    for i in range(1, int(max_page)+1):
        newurl = t_url + str(i) + "_p/"
        html = rq.get(newurl, headers=ua_header)
        time.sleep(random.random() * 5)
        soup = BeautifulSoup(html.text, "html.parser")

        div_target = soup.find_all("div", {"data-testid": "search-result-list-container"})
        print("Page_{0}_complete".format(i))

        for j in range(0, 30):
            try:
                info = div_target[0].find("div", {"data-testid": "srp-home-card-{0}".format(j)})
            except Exception:
                continue
            try:
                Price.append(info.find("div", {"data-testid": "property-price"}).text)
            except Exception:
                Price.append("NULL")
            try:
                BD.append(info.find("div", {"data-testid": "property-beds"}).text)
            except Exception:
                BD.append("NULL")
            try:
                BA.append(info.find("div", {"data-testid": "property-baths"}).text)
            except Exception:
                BA.append("NULL")
            try:
                Sqft.append(info.find("div", {"data-testid": "property-floorSpace"}).text)
            except Exception:
                Sqft.append("NULL")
            try:
                Address.append(info.find("div", {"data-testid": "property-street"}).text)
            except Exception:
                Address.append("NULL")
            try:
                City.append(info.find("div", {"data-testid": "property-region"}).text)
            except Exception:
                City.append("NULL")


    data = pd.DataFrame({'City': City,
                         'Address': Address,
                         'BD': BD,
                         'BA': BA,
                         'Sqft': Sqft,
                         'Price': Price})
    data.to_csv('{0}.csv'.format(file_name), encoding='utf8')

if __name__ == '__main__':
    or_url = 'https://www.trulia.com/for_rent/Los_Angeles,CA/'
    d_beds = {'S':'', '1':'1p_beds/', '2':'2p_beds/', '3':'3p_beds/', '4':'4p_beds/'}
    d_pets = {'C':'cats_pets/', 'D':'lg_dogs,sm_dogs_pets/', 'A':'cats,lg_dogs,sm_dogs_pets/', 'N':''}

    get_demand()
    new_url = target_url(or_url)
    get_data(new_url)