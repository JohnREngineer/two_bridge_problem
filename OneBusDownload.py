def getListOfBusIds ( agencyId, key ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	
	if agencyId is None:
		agencyId = 40
	agencyURL = 'http://api.onebusaway.org/api/where/vehicles-for-agency/' + agencyId + '.xml?key=' + key
	response = urlopen(agencyURL)
	html = response.read()
	e = ET.fromstring(html)
	
	busIdList = []
	for bus in e[4][1]:
		vehicleId = bus.find('vehicleId').text
		idList.append(vehicleId)
	return busIdList;
	
def getListOfActiveBusIdAndTripIds ( agencyId, key ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	
	if agencyId is None:
		agencyId = 40
	agencyURL = 'http://api.onebusaway.org/api/where/vehicles-for-agency/' + agencyId + '.xml?key=' + key
	response = urlopen(agencyURL)
	html = response.read()
	e = ET.fromstring(html)
	
	busIdList = []
	tripIdList = []
	for bus in e[4][1]:
		tripId = bus.find('tripId')
		if tripId is not None:
			vehicleId = bus.find('vehicleId').text
			busIdList.append(vehicleId)
			tripIdList.append(tripId.text)
	return (busIdList, tripIdList);
	
def getShapeIdFromTripId ( tripId, key ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	import requests
	from requests.exceptions import HTTPError
	
	shapeId = 0
	url = 'http://api.pugetsound.onebusaway.org/api/where/trip/' + tripId + '.xml?key=' + key
	response = urlopen(url)
	html = response.read()
	e = ET.fromstring(html)
	shapeId = e[4][1].find('shapeId').text
	return shapeId;
	
def getEncodedShapeFromShapeId ( shapeId, key ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	import requests
	from requests.exceptions import HTTPError
	import polyline
	
	shape = 0
	url = 'http://api.pugetsound.onebusaway.org/api/where/shape/' + shapeId + '.xml?key=' + key
	response = urlopen(url)
	html = response.read()
	e = ET.fromstring(html)
	encodedShape = e[4][1].find('points').text
	return encodedShape;

def getShapeFromShapeId ( shapeId, key ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	import requests
	from requests.exceptions import HTTPError
	import polyline
	
	shape = 0
	url = 'http://api.pugetsound.onebusaway.org/api/where/shape/' + shapeId + '.xml?key=' + key
	response = urlopen(url)
	html = response.read()
	e = ET.fromstring(html)
	encodedShape = e[4][1].find('points').text
	shape = polyline.decode(encodedShape)
	return shape;

def updateYugeList( yuge, id, time, lat, lon ):
	if id in yuge[0]:
		i = yuge[0].index(id)
		myList = yuge[1][i]
		if myList[len(myList)-1][0] != int(time):
			yuge[1][i].append((int(time),float(lat),float(lon)))
	else:
		yuge[0].append(id)
		yuge[1].append([(int(time),float(lat),float(lon))])
	return yuge;
		
def updateYugeList2( yuge, busId, tripId, time, lat, lon ):
	if (busId, tripId) in yuge[0]:
		i = yuge[0].index((busId, tripId))
		myList = yuge[1][i]
		if myList[len(myList)-1][0] != int(time):
			yuge[1][i].append((int(time),float(lat),float(lon)))
	else:
		yuge[0].append((busId, tripId))
		yuge[1].append([(int(time),float(lat),float(lon))])
	return yuge;
		
def getYugeList2( agencyId, key, yugeList ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	
	if agencyId is None:
		agencyId = 40
	agencyURL = 'http://api.onebusaway.org/api/where/vehicles-for-agency/' + agencyId + '.xml?key=' + key
	response = urlopen(agencyURL)
	html = response.read()
	e = ET.fromstring(html)
	
	if yugeList == []:
		yugeList = ([],[])
	latList = []
	lonList = []
	idList = []
	timeList = []

	#populate id, time, lat, and lon lists
	for bus in e[4][1]:
		location = bus.find('location')
		tripId = bus.find('tripId')
		if location is not None and tripId is not None:
			lat = location.find('lat').text
			lon = location.find('lon').text
			latList.append(float(lat))
			lonList.append(float(lon))
			vehicleId = bus.find('vehicleId').text
			tripId = bus.find('tripId').text
			idList.append(vehicleId)
			locationTime = bus.find('lastLocationUpdateTime').text
			timeList.append(locationTime)
			
			updateYugeList2( yugeList, vehicleId, tripId, locationTime, lat, lon )
	return [ yugeList ];

def getLatLonList( agencyId, key, yugeList ):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	
	if agencyId is None:
		agencyId = 40
	agencyURL = 'http://api.onebusaway.org/api/where/vehicles-for-agency/' + agencyId + '.xml?key=' + key
	response = urlopen(agencyURL)
	html = response.read()
	
	e = ET.fromstring(html)
	
	if yugeList == []:
		yugeList = ([],[])
	latList = []
	lonList = []
	idList = []
	timeList = []

	#populate id, time, lat, and lon lists
	for bus in e[4][1]:
		location = bus.find('location')
		if location is not None:
			lat = location.find('lat').text
			lon = location.find('lon').text
			latList.append(float(lat))
			lonList.append(float(lon))
			vehicleId = bus.find('vehicleId').text
			idList.append(vehicleId)
			locationTime = bus.find('lastLocationUpdateTime').text
			timeList.append(locationTime)
			
			updateYugeList( yugeList, vehicleId, locationTime, lat, lon )
	return [ yugeList ];