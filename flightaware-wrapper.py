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

username = 'username'
password = 'password'
flightId = 'flightId'

session = Session()
session.auth = HTTPBasicAuth(username, password)


transport = Transport(cache=SqliteCache(), session=session)
client = Client('http://flightxml.flightaware.com/soap/FlightXML2/wsdl', transport = transport)

response = zeep.helpers.serialize_object(client.service.FlightInfo('DL2409', 1), target_cls=collections.OrderedDict)

print(response)