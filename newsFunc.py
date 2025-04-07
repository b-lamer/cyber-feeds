#This file contains various packages and functions used for scraping or reading RSS feeds of the websites listed below.
#While this file is primarily made for its use for the newsFeed.py program at github.com/b-lamer/cyber-feeds, 
#it can be separated and used on others personal projects as well if desired.

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import feedparser
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}

bleepingcomputer = "https://www.bleepingcomputer.com/news/security/" ###
darkreading = "https://www.darkreading.com/" ###
krebson = "https://krebsonsecurity.com/"
cyberscoop = "https://cyberscoop.com/"
hackernews = "https://thehackernews.com/"
techcrunch = "https://techcrunch.com/tag/security/" ###
infosecmag = "https://www.infosecurity-magazine.com/"
securitymagazine = "https://www.securitymagazine.com/"
threatpost = "https://threatpost.com/"

curtime = datetime.now(tz=None)

#RSS Functions
def bcRSS():
    utctime = datetime.now(timezone.utc)
    feed = feedparser.parse("https://www.bleepingcomputer.com/feed/")

    for item in feed.entries:
        dtime = item.published
        pub_time = datetime.strptime(dtime, "%a, %d %b %Y %H:%M:%S %z")

        if (utctime - pub_time) < timedelta(hours=12):
            if item.category == "Security":
                article = {
                    "title": item.title,
                    "link": item.link,
                    "description": item.description
                }
                
                newsList.append(article)
        else:
            break

def tcRSS():
    curtime = datetime.now(tz=None)
    feed = feedparser.parse("https://techcrunch.com/feed/")

    for item in feed.entries:
        dtime = item.published
        pub_time = datetime.strptime(dtime, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)

        if (curtime - pub_time) < timedelta(hours=12):
            article = {
                "title": item.title,
                #"link": item.link,
                #"description": item.description
            }
            print(article)
            #newsList.append(article)
        else:
            break

def smRSS():
    feed = "https://www.securitymagazine.com/rss"

def tpRSS():
    feed = "https://threatpost.com/rss-feeds/"




#News Scraping Functions

def bcScrape(): #Scraping BleepingComputer security news page
    site = requests.get(bleepingcomputer, headers=headers)
    sitehtml = BeautifulSoup(site.text, features="html.parser")
    news = sitehtml.find_all("div", class_ = "bc_latest_news_text")
    for div in news:
        try:
            date = div.find("li", class_="bc_news_date").text.strip()
            time = div.find("li", class_="bc_news_time").text.strip()
            dtime = f"{date} {time}"
            publish_time = datetime.strptime(dtime, "%B %d, %Y %I:%M %p")
            timediff = curtime - publish_time
            if timediff <= timedelta(hours=12):
                title = div.find("a")
                print(title.text.strip())
                print(title['href'])
                desc = div.find("p").text.strip()
                print(desc)
            else:
                break
        except:
            pass

def drScrape(): #Scraping DarkReading's news page
    site = requests.get(darkreading, headers=headers)
    sitehtml = BeautifulSoup(site.text, features="html.parser")
    news = sitehtml.find_all("div", class_ = "ContentPreview LatestFeatured-ContentItem LatestFeatured-ContentItem_left")

with open('newsData.json') as fp:
    newsList = json.load(fp)
    #print(len(newsList))

#tcRSS()
#bcRSS()
drScrape()

while len(newsList) > 20:
    print(len(newsList))
    del newsList[0]

# make changes to newsList

with open('newsData.json', 'w') as fp:
    
    json.dump(newsList, fp, indent=2)