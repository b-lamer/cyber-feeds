import requests
import ijson
import gzip
import json
from pathlib import Path

kevs = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def vulnstream(kevs, cveList):
    url = requests.get(kevs, stream=True)

    url.raw.decode_content = True
    decompressed_stream = gzip.GzipFile(fileobj=url.raw)

    vulns = ijson.items(url.raw, 'vulnerabilities.item')
    for vuln in vulns:
        #print(vuln)
        name = vuln['vulnerabilityName']
        desc = vuln['shortDescription']
        cveid = vuln['cveID']
        #print(name)
        #print(desc)
        #print(cveid)
        item = {
            "title": name,
            "description": desc,
            "id": cveid
        }
        cveList.append(item)
        if len(cveList) >= 20:
            #print(len(cveList))
            break




######################
def run():
    cveList = []
    p = Path(__file__).with_name('cveData.json')

    vulnstream(kevs, cveList)

    while len(cveList) > 20:
        print(len(cveList))
        del cveList[0]

    # make changes to cveList

    with open(p, 'w') as fp:
        json.dump(cveList, fp, indent=2)