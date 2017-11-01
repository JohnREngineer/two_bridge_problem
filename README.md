# Bridge Traffic Analysis using OneBusAway API

This project aims to analyze traffic patterns on the I-90 and SR-520 bridges connecting Seattle and Bellevue in Washington State. This is done using the data available through the OneBusAway Rest API developed by The University of Washington.

## 1.Data Collection

Data has been collected between 7/7 and 8/13 of 2017.

### Methods
The data is collected and stored in a database using a [busLocationsDatabase.py](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/busLocationsDatabase.py) which queries the Rest API every 2 minutes. Each bus that is reporting its location is stored in a list and when it no longer updates its location the trip is recorded in a SQLite database. This program is called by a cron job set to 5:45AM before the first buses at 6:00 AM. Then at the 11:50PM a cron job calls a script which backs up the database using [gdrive](https://github.com/prasmussen/gdrive) to my google drive, a linux command line utility for google drive.

## 2. Exploration of the data

In order to get our first look at the data we create a simple metric of the speed of the bus on the bridge. This metric called simpleMPH simply finds adjacent points of data in each trip which cross the longitude of -122.27 and then calculates the average mph given by the delta distance and the delta time between those two points.

[ExploreSimpleMPH.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/ExploreSimpleMPH.ipynb) walks through the first exploration of the data.

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig4_2.png" height="175"><img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig5_3.png" height="175"><img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig6_4.png" height="175">

One of the first issues encountered was that a large portion of the data had been duplicated. See 
[ExploreDuplicates.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/ExploreDuplicates.ipynb) which walks through the exploration of duplicated data. After looking into the documentation more it turned out that the source of this duplication is actually on the OneBusAway side. According to the link below "Agencies often schedule major changes to their system around a particular date, with one GTFS feed for before the service change and a different GTFS feed for after." http://developer.onebusaway.org/modules/onebusaway-gtfs-modules/1.3.3/onebusaway-gtfs-merge-cli.html



