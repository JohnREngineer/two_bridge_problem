# Bridge Traffic Analysis using OneBusAway API

This project aims to analyze traffic patterns on the I-90 and SR-520 bridges connecting Seattle and Bellevue in Washington State. This is done using the data available through the OneBusAway Rest API developed by The University of Washington.

## 1.Data Collection

Data has been collected between 7/7 and 8/13 of 2017.

### Methods
The data is collected and stored in a database using a [busLocationsDatabase.py](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/busLocationsDatabase.py) which queries the Rest API every 2 minutes. Each bus that is reporting its location is stored in a list and when it no longer updates its location the trip is recorded in a SQLite database. This program is called by a cron job set to 5:45AM before the first buses at 6:00 AM. Then at the 11:50PM a cron job calls a script which backs up the database using [gdrive](https://github.com/prasmussen/gdrive) to my google drive, a linux command line utility for google drive.

## 2. Exploration of the data

In order to get our first look at the data we create a simple metric of the speed of the bus on the bridge. This metric called simpleMPH simply finds adjacent points of data in each trip which cross the longitude of -122.27 and then calculates the average mph given by the delta distance and the delta time between those two points.

[ExploreSimpleMPH.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/ExploreSimpleMPH.ipynb) walks through the first exploration of the data.

One of the first things encountered was that a large portion of the data had been duplicated.
[ExploreDuplicates.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/ExploreDuplicates.ipynb) walks through the exploration of duplicated data. 

![im1](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig4.png)
![im2](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig5_3.png)
![im3](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig6.png)


