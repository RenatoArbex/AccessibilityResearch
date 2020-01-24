# Accessibility Calculations

This code calculates population-weighted average accessibility indicators for public transport network analysis using three methods: cumulative opportunies (fixed travel time threshold of 30, 60 and 90 minutes), gravity-based (from a calibrated negative exponential decay function) and zone-specific variable travel time threshold, as explained in the original paper in the link below: 

- (link to paper - to update)

To evaluate accessibility, a spatial unit must be chosen. In this repository, the spatial unit (cell) is defined by an ID, and a group of spatial units form a larger city area. The accessibility metrics are calculated for each zone ID, and then grouped for each region by calculating the population-weighted average accessibility for all indicators.

## Data input

The accessibility calculation requires 5 main files. We have used fictitious example data.

### 1) Travel time matrix between the cells

To estimate how many jobs/opportunities each spatial unit accesses, a travel time matrix is required. 

The travel time matrix is built using the script made by [Rafael Pereira](https://github.com/rafapereirabr/otp-travel-time-matrix) that uses [Open Trip Planner (OTP)](https://github.com/opentripplanner/OpenTripPlanner). OTP requires a GTFS data file along with OSM street network data. The input file is a csv file named traveltime_matrix_xx.csv, where xx is the name of the region, as below:

```
Origin,Destination,Walk_distance,nboardings,Travel_time
1,1,245,1,4319
1,2,148,3,1443
1,3,114,1,3286
1,4,335,1,2969
1,5,125,1,6271
1,6,349,1,1893
1,7,259,2,1774
(...)
```

### 2) Cell ID to larger area

To group accessibility to larger areas, a ID to area file is needed. In the example data provided, we have used 5 areas, N (North), E (East), W (West), C (Central), S (South). The input file is a csv file named id_to_larger_area_xx.csv as below:

```
id,area
1,N
2,N
3,N
4,N
5,N
(...)
```

### 3) Job and Population data for each cell

For accessibility calculations, we need to define the opportunity metric. We have chosen number of jobs, and the file required for this data is named id_jobs_pop_xx.csv as below:

```
id,jobs,pop
1,1978,8340
2,206,4888
3,1111,3668
4,4601,3000
5,663,2572
6,4692,9840
```

### 4) Buffer time between origin-destination pairs

To estimate the effect of travel time reliability, the buffer time between areas is required. The buffer time is added to total travel time to represent how users budget additional time to secure on-time arrival. The csv file required is named buffer_time_between_areas_xx.csv with data as below:

```
area_from,area_to,od,buffer_time
N,N,N-N,1016
N,W,N-W,1114
N,C,N-C,629
N,E,N-E,680
N,S,N-S,1038
W,N,W-N,556
W,W,W-W,1100
```

### 5) Area-specific travel time threshold 

In order to reduce the effect of the arbritrary definition of cutoff times for accessibility calculations, we have proposed the use of a variable area-specific travel time threshold to better reflect travel behavior. This file is named travel_time_limit_from_percentile_xx.csv and contains travel time threshold for each area. 

```
area,time
N,3600
W,3600
C,2700
E,4800
S,3600
```

Finally, to estimate the effect of crowding on accessibility to opportunities, a new travel time matrix that considers the higher travel time perception due to crowdedness is required. The analysis then can be done with and without crowding perception to evaluate which areas in the region are more influenced by crowding discomfort and lower travel time reliability.

This reposity provides the source code used for accessibility calculations as described in the paper (to be updated) thus enabling replicability for researchers in other regions.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Contact
You can contact me at:
renatoarbex@usp.br
