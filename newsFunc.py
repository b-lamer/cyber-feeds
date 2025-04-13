#!/usr/bin/python3
#This file contains various packages and functions used for scraping or reading RSS feeds of the websites listed below.
#While this file is primarily made for its use for the newsFeed.py program at github.com/b-lamer/cyber-feeds, 
#it can be separated and used on others personal projects as well if desired.

from pathlib import Path
import requests
import cloudscraper #Used to scrape CloudFlare sites
from bs4 import BeautifulSoup #Used for scraping websites
from datetime import datetime, timedelta, timezone #Used for comparing time/dates to avoid repeat articles 
import feedparser
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}

bleepingcomputer = "https://www.bleepingcomputer.com/news/security/" ###
darkreading = "https://www.darkreading.com/" ###
krebson = "https://krebsonsecurity.com/"
cyberscoop = "https://cyberscoop.com/"
hackernews = "https://thehackernews.com/"
techcrunch = "https://techcrunch.com/category/security/" ###
infosecmag = "https://www.infosecurity-magazine.com/"
securitymagazine = "https://www.securitymagazine.com/"

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
                titlbox = div.find("a")
                link = titlbox['href']
                title = titlbox.text.strip()
                desc = div.find("p").text.strip()
                article = {
                    "title": title,
                    "link": link,
                    "description": desc
                }
                newsList.append(article)
            else:
                break
        except:
            pass

def drScrape(): #Scraping DarkReading's news page
    scraper = cloudscraper.create_scraper()
    site = scraper.get(darkreading)
    sitehtml = BeautifulSoup(site.text, features="html.parser")
    print(sitehtml)
    news = sitehtml.find_all("div", class_ = "ListPreview-TitleWrapper")
    for div in news[0:5]:
        titlbox = div.find("a")
        title = titlbox.text.strip()

        titleCheck = ' '.join(title.split()[:3])
        if any(titleCheck in article['title'] for article in newsList):
            print("no")
            pass
        else:
            print("yes")
            link = "https://www.darkreading.com" + titlbox['href']
            article = {
                "title": title,
                "link": link
            }
            newsList.append(article)

def tcScrape():
    site = requests.get(techcrunch, headers=headers)
    sitehtml = BeautifulSoup(site.text, features="html.parser")
    news = sitehtml.find_all("div", class_ = "loop-card__content")
    for div in news:
        try:
            timebox = div.find("time")
            #print(timebox)
            titlbox = div.find("a", class_ = "loop-card__title-link")
            link = titlbox['href']
            title = titlbox.text.strip()
            print(title)
            print(link)
            #print()
        except:
            pass

p = Path(__file__).with_name('newsData.json')

with open(p) as fp:
    newsList = json.load(fp)
    #print(len(newsList)) # <- Json size bug testing

#tcRSS()
#bcRSS()
#drScrape()
bcScrape()
#tcScrape()

while len(newsList) > 20:
    print(len(newsList))
    del newsList[0]

# make changes to newsList

with open(p, 'w') as fp:
    
    json.dump(newsList, fp, indent=2)