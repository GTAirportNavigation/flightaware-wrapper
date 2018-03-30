from __future__ import print_function
from requests import Session
from requests.auth import HTTPBasicAuth
import zeep
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep import xsd
from zeep.cache import SqliteCache
from zeep.transports import Transport
import collections
import time

username = input("FlightAware API Username:\t")
password = input("FlightAware API Password:\t")
destination = input("Destination:\t")

session = Session()
session.auth = HTTPBasicAuth(username, password)

transport = Transport(cache=SqliteCache(), session=session)
client = Client('http://flightxml.flightaware.com/soap/FlightXML2/wsdl', transport = transport)

#api call for flight schedules
response0 = zeep.helpers.serialize_object(client.service.AirlineFlightSchedules(int(time.time()), int(time.time()) + 86400, origin = "ATL", destination = destination, airline = "", flightno = "", howMany = 15, offset = 0), target_cls=collections.OrderedDict)

#This is the Ordered Dictionary containing flight numbers
#Key = Administrating Carrier Flight No, Value = list containing all crosslisted flight No's
#The ordered dict is ordered by earliest departure
flightOrdDict = collections.OrderedDict()

for x in range(0, len(response0["data"]) - 1):
    if (response0["data"][x]["ident"] not in flightOrdDict):
        if (response0["data"][x]["acutal_ident"] == ""):
            flightOrdDict[response0["data"][x]["acutal_ident"]] = [response0["data"][x]["acutal_ident"]]
        else if (response0["data"][x]["actual_ident"] not in flightOrdDict):

    if(lastFlight != response0["data"][x]["actual_ident"]):


print(flightList)