## Overview
This program will scrape cybersecurity news and CVE vulnerability releases and print the latest updates on a dashboard. The output is saved in json format and the scripts can be run on their own if preferred.<br>

To utilize the full program, you will need to do the following:
* Install the dependencies below
* Set up hourly cronjobs in order to run the CVE and News scripts
* Run `streamlit run dashboard.py` in terminal

### Windows:<br>
CVE Feed Script: `pip install requests datetime json`<br>
News Feed Script: `pip install cloudscraper bs4 feedparser` *<- In addition to above*<br>
Dashboard: `pip install streamlit streamlit-autorefresh`
<br>
### Linux:<br>
$\color{red}{\textsf{Note: DO NOT use this if you don't know what you're doing. This could break certain aspects of your linux machine.}}$ <br>

CVE Feed Script: `pip install requests datetime json --break-system-packages`<br>
News Feed Script: `pip install cloudscraper bs4 feedparser --break-system-packages` *<- In addition to above*<br>
Dashboard: `pip install streamlit streamlit-autorefresh --break-system-packages` <br>

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Example
Below is my use case of this program. It is run on a Raspberry Pi 3 connected to a 7-inch display which is held up by two 3D printed stands. 
<br>
<br>
![7 Inch News Feed](https://github.com/user-attachments/assets/2dce950e-4441-4ad2-8b3c-6d20da8829ad)
