Climate Study using SQLAlchemy and Flask API

The first goal of this development effort was to develop queries for analyzing the climate of Hawaii 
using SQLAlchemy ORM queries, Pandas, and Matplotlib.  The second goal was to design & develop a Flask API
application with routes returning stations, precipitation, and temperature details based on date ranges. 

The repo structure for this development effort consists of 2 folders:                                                                 
1. Resources Folder contains the SQLite data for the Hawaiian weather station and measurements.                                               
2. Analysis Folder contains:                                                    
2a. Jupyter notebook for the Step 1 Climate Analysis and Exploration.                                               
2b. A Climate app utilizing a Flask API that will return all executable routes:                                           
2b1. Dates and precipitation.                                                                           
2b2. List of stations.                                                                                         
2b3. Temperature observations for the previous year for the most active station.                                          
2b4. Minimum, maximum, and average temperature greater than or equal to the input start date.                                       
2b5. Minimum, maximum, and average temperature between the input start and end dates.                                               
