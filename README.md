# Two Bridge Problem

Which bridge is faster, SR-520 or I-90?

This project aims to determine which bridge you should cross between Seattle and Bellevue using location data provided by [The University of Washington's OneBusAway RESTful API](http://developer.onebusaway.org/modules/onebusaway-application-modules/1.1.14/api/where/index.html).

## 1. Collection and Cleansing
Using [busLocationsDatabase.py](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/busLocationsDatabase.py) we collect and store bus locations in a SQLite database between 7/7/2017 and 8/13/2017.

Next we deduplicate entries and define simple metrics to model the speed of traffic in [ExploreSimpleMPH.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/ExploreSimpleMPH.ipynb).
Figure 1

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig4_2.png">

Figure 2

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig5_3.png">

Figure 3

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/fig6_4.png">

## 3. Analysis

First we look for patterns in our data in [Analysis.ipynb](https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/Analysis.ipynb).

Notice in Figure 6 that the I-90 bridge going west is significantly faster during the evening rush hour.

Figure 4

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/analyze_fig1.png">

Figure 5

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/analyze_fig2.png">

Figure 6

<img src="https://github.com/JonathanERuhnke/BridgeTrafficAnalysis-OneBusAway/blob/master/images/analyze_fig3.png">
