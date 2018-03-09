import sys
import csv

from urllib import urlopen
from bs4 import BeautifulSoup
from house_info import house

def get_city_dict():

    city_dict = {}

    with open("citys.csv", "r") as f:
        reader = csv.reader(f)
        for city in reader:
            city_dict[city[0]] = city[1]
        return city_dict


def get_district_dict(url):

    district_dict = {}

    html = urlopen(url).read()
    bsobj = BeautifulSoup(html, "html5lib")
    roles = bsobj.find("div", {"data-role":"ershoufang"}).findChildren("a")

    for role in roles:
        district_url = role.get("href").encode("utf-8")
        district_name = role.get_text().encode("utf-8")
        district_dict[district_name] = district_url
    return district_dict


def run():

    city_dict = get_city_dict()

    for city in city_dict.keys():
        print city

    input_city = raw_input("please input the city name ")
    city_url = city_dict.get(input_city)

    if not city_url:
        print "error input"
        sys.exit()

    ershoufang_city_url = city_url + "ershoufang"
    district_dict = get_district_dict(ershoufang_city_url)

    for district in district_dict.keys():
        print district

    input_district = raw_input("please input district: ")
    district_url = district_dict.get(input_district)

    if not district_url:
        print "input error"
        sys.exit()

    house_info_url = city_url + district_url[1:]
    print(house_info_url)
    house(house_info_url)

if __name__ =="__main__":
    run()