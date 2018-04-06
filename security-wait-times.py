import requests
from bs4 import BeautifulSoup

page = requests.get("http://apps.atl.com/Passenger/FlightInfo/Default.aspx")

#[InternationalWaitTime, DomesticNorthWaitTime, DomesticSouthWaitTime, DomesticMainWaitTime]
waitTimes = []

soup = BeautifulSoup(page.text, "html.parser")

securityWaitTextList = soup.find(id="bodySection_wucSecurityWaitTimes_upnWaitTime").find_all("p")

for checkpointText in securityWaitTextList:
    if ("closed" in str(checkpointText)):
        waitTimes.append(86400)
    elif ("less than 15 minutes" in str(checkpointText)):
        waitTimes.append(0)
    elif ("15 – 30 minutes" in str(checkpointText)):
        waitTimes.append(1350)

print(waitTimes)