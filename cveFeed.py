import requests
from datetime import datetime, timedelta
import json


curtime = datetime.now(tz=None)
starttime = curtime - timedelta(hours=36)
stime = starttime.strftime("%Y-%m-%dT%H:%M:%S")
etime = curtime.strftime("%Y-%m-%dT%H:%M:%S")

criticals = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=CRITICAL&pubStartDate={stime}&pubEndDate={etime}")
highs = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=HIGH&pubStartDate={stime}&pubEndDate={etime}")
jcrit = criticals.json()
jhigh = highs.json()

def parse(data):
    for vuln in data["vulnerabilities"]:
        vId = str(vuln["cve"]["id"])
        score = str(vuln["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"])
        rating = str(vuln["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"])
        desc = str(vuln["cve"]["descriptions"][0]["value"])

        title = vId + " - Severity:  " + score + " [" + rating + "]"

        desc = desc.split(". ")
        if len(desc) > 1:
            desc = desc[0] + ". " + desc[1]
        else:
            desc = desc[0]

        item = {
            "title": title,
            "description": desc
        }
        cveList.append(item)

######################

with open('cveData.json') as fp:
    cveList = json.load(fp)
    #print(len(newsList))

parse(jhigh)
parse(jcrit)

while len(cveList) > 20:
    print(len(cveList))
    del cveList[0]

# make changes to newsList

with open('cveData.json', 'w') as fp:
    json.dump(cveList, fp, indent=2)