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
origin = input("Origin:\t")
destination = input("Destination:\t")

startTime = 1522993920
#startTime = int(time.time())

endTime = 1523016120
#endTime is 3 hours ahead of startTime in Unix epoch time
#endTime = int(time.time()) + 10800

session = Session()
session.auth = HTTPBasicAuth(username, password)

transport = Transport(cache=SqliteCache(), session=session)
client = Client('http://flightxml.flightaware.com/soap/FlightXML2/wsdl', transport = transport)

#api call for flight schedules
response0 = zeep.helpers.serialize_object(client.service.AirlineFlightSchedules(startTime, endTime, origin = origin, destination = destination, airline = "", flightno = "", howMany = 15, offset = 0), target_cls=collections.OrderedDict)


#This is the Ordered Dictionary containing flight numbers
#Key: flightDepartureTime
#Value: a List object with every flight number under that flight. The operating flight number is the first in the list. ["Actual Flight Number", "Some Other Flight Number", "Some Flight Number"]
#The ordered dict is ordered by earliest departure
#flightOrdDict = collections.OrderedDict()
flightDict = {}

#Iterates over the flights going from A to B departing in at most three hours
for x in range(0, len(response0["data"])):

    keyObject = response0["data"][x]["departuretime"]

    #Creates the list used as a key
    #if (response0["data"][x]["actual_ident"] == ""):
    #    keyObject = [response0["data"][x]["ident"], response0["data"][x]["departuretime"]]
    #else:
    #    keyObject = [response0["data"][x]["actual_ident"], response0["data"][x]["departuretime"]]

    if (keyObject not in flightDict):
        if (response0["data"][x]["actual_ident"] == ""):
            flightDict[keyObject] = [response0["data"][x]["ident"]]
        else:
            flightDict[keyObject] = [response0["data"][x]["actual_ident"], response0["data"][x]["ident"]]
    else:
        if (response0["data"][x]["ident"] != flightDict[keyObject][0]):
            flightDict[keyObject].append(response0["data"][x]["ident"])

flightOrderedDict = collections.OrderedDict(sorted(flightDict.items(), key=lambda t: t[0]))

print(flightOrderedDict)