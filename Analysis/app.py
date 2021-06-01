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
    results = session.query(Measurement.date, func.round(func.sum(Measurement.prcp),2)).\
    filter(Measurement.date > '2016-08-22').\
    group_by(Measurement.date).\
    order_by((Measurement.date).desc()).all()

    session.close()

    # Convert list of tuples into a dictionary or list
    results = dict(results) 
    #all_precipitation = list(np.ravel(results)) - applicable for lists

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all reporting station related information
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Convert list of tuples into a dictionary or list
    results = dict(results)
    #all_stations = list(np.ravel(results)) - applicable for lists

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature observations for the most active station"""
    # Query all temperature observation related information
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into a dictionary or list
    results = dict(results)
    #all_tobs = list(np.ravel(results)) - applicable for lists

    return jsonify(results)


@app.route("/api/v1.0/<start>")
def start_date(start):
  
    session = Session(engine)

    """Return a calculated list of TMIN, TMAX, and TAVG for all dates greater than or equal to the start date"""
    
    min_result = session.query(func.min(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()
    max_result = session.query(func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()
    avg_result = session.query(func.round(func.avg(Measurement.tobs),1)).\
                            filter(Measurement.date >= start).all()
    
    session.close()
    
    # Create a dictionary to assign 'name tags' to the calculated values
 
    min_result = [r for (r,) in min_result]
    max_result = [r for (r,) in max_result]
    avg_result = [r for (r,) in avg_result]
    tag_list = {"min temperature": min_result[0],
                "max temperature": max_result[0],
                "avg temperature": avg_result[0]}

    tag_list = dict(tag_list)
    #tag_list = list(np.ravel(tag_list)) - applicable for lists
    return jsonify(tag_list)    
   
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start, end):

    session = Session(engine)
    
    """Return a calculated list of TMIN, TMAX, and TAVG for all dates between the start/end dates"""
    
    min_result = session.query(func.min(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
    max_result = session.query(func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
    avg_result = session.query(func.round(func.avg(Measurement.tobs),1)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()     

    session.close()
    
    # Create a dictionary to assign 'name tags' to the calculated values

    min_result = [r for (r,) in min_result]
    max_result = [r for (r,) in max_result]
    avg_result = [r for (r,) in avg_result]
    tag_list = {"min temperature": min_result[0],
                "max temperature": max_result[0],
                "avg temperature": avg_result[0]}

    tag_list = dict(tag_list)
    #tag_list = list(np.ravel(tag_list)) - applicable for lists
    return jsonify(tag_list)  

if __name__ == '__main__':
    app.run(debug=True)