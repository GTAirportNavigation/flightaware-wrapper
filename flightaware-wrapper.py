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
flightId = input("Flight Number:\t")

session = Session()
session.auth = HTTPBasicAuth(username, password)


transport = Transport(cache=SqliteCache(), session=session)
client = Client('http://flightxml.flightaware.com/soap/FlightXML2/wsdl', transport = transport)

response0 = zeep.helpers.serialize_object(client.service.FlightInfo(flightId, 15), target_cls=collections.OrderedDict)

flight = 0

while((flight < 14) and ((response0['flights'][flight + 1]['filed_departuretime'] - int(time.time())) > 0)):
    flight += 1

filed_departuretime = response0['flights'][flight]['filed_departuretime']

faFlightID = zeep.helpers.serialize_object(client.service.GetFlightID(flightId, filed_departuretime), target_cls=collections.OrderedDict)

response1 = client.service.AirlineFlightInfo(faFlightID)

originGate = response1['gate_orig']

print(originGate)