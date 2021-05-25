import numpy as np
import json 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all 12 months of precipitation"""
    # Query all precipitation related information
    results = session.query(func.round(func.sum(Measurement.prcp),2), Measurement.date).\
    filter(Measurement.date > '2016-08-22').\
    group_by(Measurement.date).\
    order_by((Measurement.date).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all precipitation related information
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature observations for the most active station"""
    # Query all precipitation related information
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):
  
    session = Session(engine)

    """Return a calculated list of TMIN, TMAX, and TAVG for all dates greater than or equal to the start date"""
    
    results1 = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()        
    results2 = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all() 
    results3 = session.query(func.round(func.avg(Measurement.tobs),1)).\
        filter(Measurement.date >= start).all()

    session.close()
    
    # Create a dictionary to assign 'name tags' to the calculated list

    func_dict = {}
    func_dict["min temperature"] = results1
    func_dict["max temperature"] = results2
    func_dict["avg temperature"] = results3
    
    # all_func_values.append(func_dict)  
    start_func_tobs = list(np.ravel(func_dict))
    return jsonify(start_func_tobs)    
   
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start, end):

    session = Session(engine)
    
    """Return a calculated list of TMIN, TMAX, and TAVG for all dates between the start/end dates"""
    
    resultslist = session.query(func.min(Measurement.tobs),\
                                func.max(Measurement.tobs),\
                                func.round(func.avg(Measurement.tobs),1)).\
                                filter(Measurement.date >= start).\
                                filter(Measurement.date <= end).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    date_range_func_tobs = list(np.ravel(resultslist))
    
    return jsonify(date_range_func_tobs)

    """Return the input start and end dates"""
    # return jsonify(start, end)

if __name__ == '__main__':
    app.run(debug=True)