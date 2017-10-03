def getBusPositionData(routeId, key):
	from urllib.request import urlopen
	import numpy as np
	import xml.etree.ElementTree as ET
	
	## http://developer.onebusaway.org/modules/onebusaway-application-modules/1.1.14/api/where/methods/trips-for-route.html
	## IncludeStatus - Can be true/false to determine whether full <tripStatus/> elements with full real-time information are included in the <status/> section for each <tripDetails/> element. Defaults to false.
	## http://api.pugetsound.onebusaway.org/api/where/trips-for-route/40_100236.xml?key=TEST&includeStatus=true
	## http://api.pugetsound.onebusaway.org/api/where/trips-for-route/40_100239.xml?key=TEST&includeStatus=true
	agencyURL = 'http://api.pugetsound.onebusaway.org/api/where/trips-for-route/' + routeId + '.xml?key=' + key + '&includeStatus=true'
	response = urlopen(agencyURL)
	html = response.read()
	e = ET.fromstring(html)
	if e[1].text == '200':
		myList = []
		for bus in e[4][1]:
			status = bus.find('status')
			location = status.find('lastKnownLocation')
			if location is not None:
				position = status.find('position')
				timeHeader = status.find('lastLocationUpdateTime')
				if timeHeader is not None:
					time = int(timeHeader.text)
					tripId = bus.find('tripId').text
					lat = float(position.find('lat').text)
					lon = float(position.find('lon').text)
					realLat = float(location.find('lat').text)
					realLon = float(location.find('lon').text)
					actualDistanceAlongTrip = float(status.find('distanceAlongTrip').text)
					scheduledDistanceAlongTrip = float(status.find('scheduledDistanceAlongTrip').text)
					totalDistanceAlongTrip = float(status.find('totalDistanceAlongTrip').text)
					scheduleDeviation = float(status.find('scheduleDeviation').text)
					orientation = float(status.find('orientation').text)
					nextStop = float(status.find('nextStop').text)
					closestStop = float(status.find('closestStop').text)
					nextStopTimeOffset = float(status.find('nextStopTimeOffset').text)
					closestStopTimeOffset = float(status.find('closestStopTimeOffset').text)
					
					myList.append( [tripId, time, lat, lon, realLat, realLon, actualDistanceAlongTrip, scheduledDistanceAlongTrip, totalDistanceAlongTrip, scheduleDeviation, orientation, nextStop, nextStopTimeOffset, closestStop, closestStopTimeOffset] )
		return(myList)
	else:
		return -1
	
def updateListAndSendtoDB(oldList, pointList, route, boundingBox):
	newList = oldList #[[tripId], [firstEpochTime], [stillGettingResults], [lastUpdateTime]]
	for index in range(len(newList[2])): #set all the variables to 0 so that we know which ones have been updated
		newList[2][index] = 0
	for point in pointList:
		if (boundingBox[0] < point[4] < boundingBox[2]) and (boundingBox[1] < point[5] < boundingBox[3]): # we only want to look at the bus movements in a large rectangular area, don't want to use resources to collect all the data
			pointToSendToDB=[]
			if point[0] in newList[0]: 				#See if the tripId is in our list of active trips, if it is
				index = newList[0].index(point[0]) 		#get the index in our list
				newList[2][index] = 1				#Set this variable to 1 to show that this trip is still being updated
				if newList[3][index] != point[1]:		#If the time of last position update is different than the last
					newList[3][index]=point[1]		#set the time of last position update to the new time
					pointToSendToDB = [newList[1][index]]+point	#keep the same trip index
					sendDataPointToDB(pointToSendToDB)		#send the point to the database
			else: 							#if not add the new trip to the list
				trip = [round(point[1]/1000)]+route	#the trip start information is the start time plus the route information
				identifier = sendTripToDB(trip)			#create the trip in the trip table and return the index
				newList[0].append(point[0]) 			#tripId
				newList[1].append(identifier)			#index in the trip table
				newList[2].append(1)				#trip is active
				newList[3].append(point[1])			#last time of update
				pointToSendToDB = [identifier]+point	#use our new trip index
				sendDataPointToDB(pointToSendToDB)	#send point to database
	for index in range(len(newList[2])-1, -1, -1):	#going backwards to preserve indexes
		if oldList[2][index] == 0:					#if the point has not been updated
			for index2 in range(len(oldList)):			#remove the point from our active list
				newList[index2].pop(index)
	return newList

def sendDataPointToDB(datapoint):
	import sqlite3

	db = sqlite3.connect('myDB/mydb')
	cursor = db.cursor()
	test= datapoint
	cursor.execute(''' INSERT INTO datapoints(correspondingTripId, tripId, time, 
							lat, lon, realLat, realLon, 
							actualDistanceAlongTrip, scheduledDistanceAlongTrip, 
							totalDistanceAlongTrip, scheduleDeviation, orientation,
							nextStop, nextStopTimeOffset, closestStop,
							closestStopTimeOffset) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', test)
	db.commit()
	db.close()
	
def sendTripToDB(trip):
	import sqlite3

	db = sqlite3.connect('myDB/mydb')
	cursor = db.cursor()
	test= trip
	cursor.execute(''' INSERT INTO trips(startTime, shortName, routeId, bridgeName) VALUES(?,?,?,?)''', test)
	returnId = cursor.lastrowid
	db.commit()
	db.close()
	return returnId

def checkEndTime():
	import datetime
	timestamp = datetime.datetime.now().time()
	end = datetime.time(16, 23)
	return (timestamp <= end)
	
def main():
	import time
	import csv

	OVERALL_BOX = [47.548725,-122.363319,47.671399,-122.138271]
	MY_BUS_KEY = 'TEST' 	#Replaced key with TEST so that it works but key is not revealed to the public,
						#this works as a key but will often return error 503 (overload)

	#[shortName, routeId, bridgeName]
	routeListImportant = [['255', '1_100146', 'SR520'], 
				['271', '1_100162', 'SR520'], 
				['545', '40_100236', 'SR520'], 
				['542', '40_100511', 'SR520'], 
				['550', '40_100239', 'I90'], 
				['554', '40_100240', 'I90']]
	routeListLong = [['255', '1_100146', 'SR520'], 
				['271', '1_100162', 'SR520'], 
				['545', '40_100236', 'SR520'], 
				['550', '40_100239', 'I90'], 
				['554', '40_100240', 'I90'], 
				['277', '1_100168', 'SR520'], 
				['311', '1_100186', 'SR520'], 
				['540', '40_100235', 'SR520'], 
				['542', '40_100511', 'SR520'], 
				['541', '40_102640', 'SR520'], 
				['167', '1_100059', 'SR520'], 
				['555', '40_100241', 'SR520'], 
				['252', '1_100143', 'SR520'], 
				['556', '40_100451', 'SR520'], 
				['257', '1_100148', 'SR520'], 
				['424', '29_424', 'SR520'], 
				['268', '1_100159', 'SR520'], 
				['111', '1_100011', 'I90'], 
				['114', '1_100013', 'I90'], 
				['212', '1_100104', 'I90'], 
				['214', '1_100106', 'I90'], 
				['216', '1_100108', 'I90'], 
				['217', '1_100109', 'I90'], 
				['218', '1_100459', 'I90'], 
				['219', '1_100110', 'I90']]
				
	routeList = routeListLong
	myList = []
	for route in routeList:
		myList.append([[], [], [], []])
	while checkEndTime():
		routeIndex = 0
		for routeIndex in range(len(routeList)):
			myNewList = getBusPositionData(routeList[routeIndex][1], MY_BUS_KEY)
			if myNewList == -1:
				time.sleep(1)
				print("Error")
			else:
				boundingBox = OVERALL_BOX
				myList[routeIndex] = updateListAndSendtoDB(myList[routeIndex], myNewList, routeList[routeIndex], boundingBox)
				numOnBridge=0
				for stat in myList[routeIndex][2]:
					if stat == 1:
						numOnBridge += 1
				print("Recording " + str(numOnBridge) + "/" + str(len(myNewList)) + " of " + routeList[routeIndex][0] + " buses for " + routeList[routeIndex][2])
			time.sleep(1)
		print("...")
		time.sleep(100)
		
main()