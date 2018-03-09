# -*- coding: utf-8 -*-
# filename: citys.py

import csv

from urllib import urlopen
from bs4 import BeautifulSoup

url = "https://cd.lianjia.com"

html = urlopen(url).read()

bsobj = BeautifulSoup(html, "html5lib")

city_tags = bsobj.find("div", {"class":"fc-main clear"}).findChildren("a")



with open("./citys.csv", "w") as f:
    writ = csv.writer(f)
    for city_tag in city_tags:
        city_url = city_tag.get("href").encode("utf-8")
        city_name = city_tag.get_text().encode("utf-8")
        writ.writerow((city_name, city_url))
        print city_name, city_url