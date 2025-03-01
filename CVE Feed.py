import requests
from datetime import datetime, timedelta


curtime = datetime.now(tz=None)
starttime = curtime - timedelta(hours=12)
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
        print(vId + " - Severity:  " + score + " [" + rating + "]")
        print(desc.split(". ",1)[0])
        desc += "." if not desc.endswith(".") else ""
        print("")

print(parse(jcrit))
print(parse(jhigh))
