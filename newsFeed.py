import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
bleepingcomputer = "https://www.bleepingcomputer.com/news/security/"
darkreading = "https://www.darkreading.com/"
securityweek = "https://www.securityweek.com/"
zdnet = "https://www.securityweek.com/"
krebson = "https://krebsonsecurity.com/"
cyberscoop = "https://cyberscoop.com/"
hackernews = "https://thehackernews.com/"
techcrunch = "https://techcrunch.com/tag/security/"
infosecmag = "https://www.infosecurity-magazine.com/"
threatpost = "https://threatpost.com/"

curtime = datetime.now(tz=None)

def bc():
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
bc()
