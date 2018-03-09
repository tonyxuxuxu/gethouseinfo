import sys
import re
import csv
import urllib

from bs4 import BeautifulSoup


def get_bsobj(url):
    page = urllib.urlopen(url)
    if page.getcode() == 200:
        html = page.read()
        bsobj = BeautifulSoup(html, "html5lib")
        return bsobj
    else:
        print "error"
        sys.exit()


def get_house_info_list(url):
    house_info_list = []
    bsobj = get_bsobj(url)
    if not bsobj:
        return None

    house_list = bsobj.find_all("li", {"class":"clear"})

    for house in house_list:

        title = house.find("div", {"class":"title"}).get_text().encode("utf-8")
        info = house.find("div",{"class":"houseInfo"}).get_text().split("|")

        block = info[0].strip().encode("utf-8")
        house_type = info[1].strip().encode("utf-8")

        size_info = info[2].strip()
        size = re.findall(r"\d+",size_info)[0]

        prize_info = house.find("div", {"class":"totalPrice"}).span.get_text()
        price = re.findall(r"\d+", prize_info)[0]

        house_info_list.append({
            "title": title,
            "price": int(price),
            "size": int(size),
            "block": block,
            "house_type": house_type,
        })

        return house_info_list

def house(url):
    house_info_list = []

    for i in range(3):
        new_url = url + 'pg' +str(i+1)
        house_info_list.extend(get_house_info_list(new_url))

        if house_info_list:
            with open("./house.csv", "wb+") as f:
                writer = csv.writer(f, delimiter="|")
                for house_info in house_info_list:
                    title = house_info.get("title")
                    price = house_info.get("price")
                    size = house_info.get("size")
                    block = house_info.get("block")
                    house_type = house_info.get("house_type")

                    writer.writerow([title, int(price), int(size), block, house_type])
                    print block, price, size