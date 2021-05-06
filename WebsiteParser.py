# -*- coding: utf-8 -*-
__author__ = 'Johannes Gontrum <gontrum@vogelschwarm.com>'

from urllib.request import Request,  urlopen
from urllib.parse import urlparse
import time
import sys
import re
from bs4 import BeautifulSoup


def get_beautiful_soup(url):
    req = Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(urlopen(req).read(), 'html.parser')


def get_netloc(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)


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
    ebay_page = get_beautiful_soup(url)
    # Get the results for the search
    search_results = ebay_page.find("div", attrs={"id": "srchrslt-content"})
    # Get the newest ad
    newest_ad = search_results.find("article", attrs={"class": "aditem"})
    ad_content = newest_ad.find("div", attrs={"class": "aditem-main--middle"})
    # Get the link
    link = get_netloc(url) + ad_content.find("a").get("href")
    # Get title
    desc = ad_content.find("a").get_text()
    # Get rent
    rent = ad_content.find("p", attrs={"class": "aditem-main--middle--price"}).get_text().strip()
    # Get location
    location = newest_ad.find("div", attrs={"class": "aditem-main--top--left"}).get_text().strip()

    # Process data
    ad = {"title": desc, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __WG1Zimmer(url):
    wg_page = get_beautiful_soup(url)
    # Most recent offer
    most_recent_ad = wg_page.find("div", attrs={"class": "wgg_card offer_list_item"})
    card_body = most_recent_ad.find("div", attrs={"class": "card_body"})
    # URL
    link = "http://www.wg-gesucht.de/" + card_body.find("a").get("href")
    # Title
    title = card_body.find("h3").get("title")
    # Rent
    rent_list = card_body.find("b").get_text().split()
    if len(rent_list) == 3:
        rent = rent_list[2]
    else:
        rent = " ".join(rent_list)
    # Location
    card_body_row = card_body.find("div", attrs={"col-xs-11"})
    location_list_raw = card_body_row.find("span").get_text().strip().split("|")
    location_list = location_list_raw[1].strip("\n").split()
    location = "{} {}".format(location_list[0], location_list[1])

    # Process data
    ad = {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __WGWohnung(url):
    wg_page = get_beautiful_soup(url)
    # Most recent offer
    most_recent_ad = wg_page.find("div", attrs={"class": "wgg_card offer_list_item"})
    card_body = most_recent_ad.find("div", attrs={"class": "card_body"})
    # URL
    link = "http://www.wg-gesucht.de/" + card_body.find("a").get("href")
    # Title
    title = card_body.find("h3").get("title")
    # Rent
    rent_list = card_body.find("b").get_text().split()
    if len(rent_list) == 3:
        rent = rent_list[2]
    else:
        rent = " ".join(rent_list)
    # Location
    card_body_row = card_body.find("div", attrs={"col-xs-11"})
    location_list_raw = card_body_row.find("span").get_text().strip().split("|")
    location_list = location_list_raw[1].strip("\n").split()
    location = "{} {}".format(location_list[0], location_list[1])

    # Process data
    ad = {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __WohnungsBoerse(url):
    page = get_beautiful_soup(url)
    # Search results
    search_results = page.find("section", attrs={"class": "search_result_container"})
    # Newest ad
    newest_ad = search_results.find("div", attrs={"class": "search_result_entry"})
    ad_data = newest_ad.find("div", attrs={"class": "search_result_entry-data"})
    headline = ad_data.find("h3", attrs={"class": "search_result_entry-headline"})
    # Title
    title = headline.find("a").get("title")
    # Link
    link = get_netloc(url) + headline.find("a").get("href")
    # Rent
    props = newest_ad.find("div", attrs={"class": "search_result_entry-objectproperties"})
    rent = "".join(props.find("dd").get_text().strip().split())
    # Location
    location = "".join(
        newest_ad.find("div", attrs={"class": "search_result_entry-subheadline"}).get_text().strip())

    # Process data
    ad = {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __Immowelt(url):
    immow_page = get_beautiful_soup(url)
    # Most recent offer
    results = immow_page.find("div", attrs={"class": "iw_list_content"})
    newest_ad = results.find("div", attrs={"class": "listitem"})
    ad_content = newest_ad.find("div", attrs={"class": "listcontent"})
    # Title
    title = newest_ad.find("h2").get_text()
    # URL
    link = get_netloc(url) + newest_ad.find("a").get("href")
    # Rent
    hard_fact = ad_content.find("div", attrs={"class": "hardfact price_rent"})
    rent = hard_fact.find("strong").get_text().strip()
    # Location
    location = ad_content.find("div", {"class": "listlocation"}).get_text().strip()
    # Process data
    ad = {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __ImmoScout24(url):
    immoc_page = get_beautiful_soup(url)
    # Most recent offer
    ads = immoc_page.find("div", attrs={"id": "listings"})
    newest_ad = ads.find("article", attrs={"class": "result-list-entry"})
    # Title
    header = newest_ad.find("h5", attrs={"class": "result-list-entry__brand-title"}).get_text().strip()
    title = header[3:]
    # URL
    link = get_netloc(url) + newest_ad.find("a").get("href")
    # Rent
    rent = newest_ad.find("dd").get_text().strip()
    # Location
    location = newest_ad.find("button", attrs={"class": "result-list-entry__map-link"}).get_text().strip()
    # Process data
    ad = {"title": title, "url": link, "rent": rent, "location": location, "time": get_time_stamp()}
    return ad


def __Immonet(url):
    immonet_page = get_beautiful_soup(url)
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
