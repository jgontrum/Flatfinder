# -*- coding: utf-8 -*-
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

import urllib
import time
import sys
import re
from beautifulsoup4 import BeautifulSoup


def get_time_stamp():
    return time.strftime("%b %d %Y %H:%M:%S", time.localtime())


def parse(site, url):
    try:
        if site == 'eBay':
            return __eBay(url)
        elif site == 'WG1Zimmer':
            return __WG1Zimmer(url)
        elif site == 'WGWohnung':
            return __WGWohnung(url)
        elif site == 'WohnungsBoerse':
            return __WohnungsBoerse(url)
        elif site == 'Immowelt':
            return __Immowelt(url)
        elif site == 'ImmoScout24':
            return __ImmoScout24(url)
        elif site == 'Immonet':
            return __Immonet(url)
        else:
            print("Called with unknown website (" + str(site) + "). Leaving now.")
            sys.exit(1)
    except Exception as e:
        print("Failed to catch data for " + str(site) + " with URL " + str(url))


def __eBay(url):
    page = urllib.request.urlopen(url)
    ebay_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_ad = ebay_page.find("li", attrs={"class": "ad-listitem   "})
    # Title
    title = most_recent_ad.find("a", attrs={"class": "ad-title"})
    # URL
    link = "http://kleinanzeigen.ebay.de" + title.get('href')
    # Text
    text = title.get_text()
    # Rent
    rent = most_recent_ad.find("strong").get_text()
    # Location
    location = most_recent_ad.find("h3").get_text(" ")
    # Process data
    return {"title": text, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __WG1Zimmer(url):
    page = urllib.request.urlopen(url)
    wg_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_ad = wg_page.find("div", attrs={"class": "list-details-ad-wrapper CLR "})
    # URL
    link = "http://www.wg-gesucht.de/" + most_recent_ad.find("h2").find("a").get("href")
    title = most_recent_ad.find("h2").find("a").get_text().strip()
    # Rent
    rent_raw = most_recent_ad.find("strong", attrs={"class": "list-details-ad-price"})
    rentList = rent_raw.find("a").get_text().split()
    if len(rentList) == 3:
        rent = rentList[2]
    else:
        rent = " ".join(rentList)
    # Location
    locationList = most_recent_ad.find("p").get_text().strip().split("\n")
    if len(locationList) == 2:
        location = locationList[0].strip()
    else:
        location = " ".join(locationList)
    # Process data
    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __WGWohnung(url):
    page = urllib.request.urlopen(url)
    wg_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_ad = wg_page.find("div", attrs={"class": "list-details-ad-wrapper CLR "})
    # URL
    link = "http://www.wg-gesucht.de/" + most_recent_ad.find("h2").find("a").get("href")
    title = most_recent_ad.find("h2").find("a").get_text().strip()
    # Rent
    rent_raw = most_recent_ad.find("strong", attrs={"class": "list-details-ad-price"})
    rent_list = rent_raw.find("a").get_text().split()
    if len(rent_list) == 3:
        rent = rent_list[2]
    else:
        rent = " ".join(rent_list)
    # Location
    location_list = most_recent_ad.find("p").get_text().strip().split("\n")
    if len(location_list) == 2:
        location = location_list[0].strip()
    else:
        location = " ".join(location_list)
    # Process data
    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __WohnungsBoerse(url):
    # Receiving data from javascript in the html header
    page = urllib.request.urlopen(url)
    find_area = re.compile("geocode\(.*?\}\);", re.DOTALL)

    offer_raw = find_area.findall(str(page.read()))[0]
    identificator = re.findall(r", \d+,", offer_raw)[0].replace(",","").lstrip()

    tokenized = re.findall(r"'.*?'", offer_raw)
    # Position | Data
    # 0        | Address
    # 1        | Rooms
    # 2        | Size
    # 3        | Rent
    # 4,5      | -
    # 6        | Title
    # 7,8      | ZIP + City

    location = tokenized[0].replace("'", "")
    rent = tokenized[3].replace("'", "").replace("&euro", u"€")
    title = tokenized[6].replace("'", "")
    link = "http://www.wohnungsboerse.net/immodetail/" + identificator

    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __Immowelt(url):
    page = urllib.request.urlopen(url)
    immow_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_offer = immow_page.find("div", {"class": "divObject  listitem_new_wrap"})
    # Title
    url = most_recent_offer.find("a")
    title = most_recent_offer.find("h3").get_text()
    # URL
    link = "http://www.immowelt.de" + url.get("href")
    # Rent
    rent = most_recent_offer.find("div", {"class": "hardfact"}).get_text()
    # Location
    location_raw = most_recent_offer.find("div", {"class": "location location_exact"}).get_text(" ")
    location = ' '.join(location_raw.split())
    # Process data
    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __ImmoScout24(url):
    page = urllib.request.urlopen(url)
    immoc_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_offer = immoc_page.find("div", {"class": "resultlist_entry_data"})
    # Title
    url = most_recent_offer.find("a")
    title = url.get("title")
    # URL
    link = "http://www.immobilienscout24.de" + url.get("href")
    # Rent
    rent = most_recent_offer.find("dd", {"class": "value"}).get_text().split()[0]
    # Location
    location = most_recent_offer.find("span", {"class": "street"}).get_text(" ")
    # Process data
    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}


def __Immonet(url):
    page = urllib.request.urlopen(url)
    immonet_page = BeautifulSoup(page.read())
    # Most recent offer
    most_recent_offer = immonet_page.find("div", {"class": "selListItem"})
    # Title
    url = most_recent_offer.find("a")
    title = url.get("title")
    # URL
    link = "http://www.immonet.de" + url.get("href")
    # Rent
    rent = most_recent_offer.find("span", {"class": "fsLarge"}).get_text()
    # Location
    location = most_recent_offer.find("p", {"class": "fsSmall"}).get_text("")
    location = " ".join(location.split())
    # Process data
    return {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
