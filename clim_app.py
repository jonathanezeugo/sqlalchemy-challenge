# Importing dependencies - packages and libraries
# 1. Import Flask
from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, desc



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# # Create our session (link) from Python to the DB
# session = Session(engine)

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
# Home Page; list of routes that are available
@app.route("/")
def Home():
    return (
        f"Welcome to the Climate App site:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>,<end>"        
    )


# Route to query date and precipation data from DB
# App route to precipation information for the range of dates in DB
@app.route("/api/v1.0/precipitation")
def preciptn():
    # Create our session (link) from Python to the DB
    session = Session(engine)    
    previous_yr =dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= previous_yr).all()
    
    precip_dic = {date: prcp for date, prcp in results}

    session.close()
    return (precip_dic)

# App route to generate a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Querying the stations DB for station names which would populate the list
    stns = session.query(station.name).all()
    session.close()

    # Converting list of tuples into normal list
    all_stns = list(np.ravel(stns))
    return jsonify(stns)

# App route to generate temperature data for the most active station for the last year
@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    hghst_stn = session.query(station.name, measurement.station, func.count(measurement.station).label('count')).\
        filter(measurement.station == station.station).group_by(measurement.station).order_by(desc('count')).first()
    stn_name = hghst_stn[0]
    stn_wID = hghst_stn[1]

    date_n_precp = session.query(station.name, measurement.date, measurement.tobs).filter(measurement.date >= year_ago).filter(measurement.station == stn_wID).all()
    # Closing out session
    session.close()

    # Putting all queried information into a list of dictionary
    full_stn_data = [{'Name': name, 'Date': date, 'Temp': temp} for name, date, temp in date_n_precp]

    # Improving presentation on JSON
    fst_stn = list(np.ravel(full_stn_data))
     
    return jsonify(fst_stn)

# App route to generate min temp, avg temp, and max temp for a given start or end date range
@app.route("/api/v1.0/start")
def calc_temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # For start-only analysis
    start_date = '2016-08-23'
    #end_date = '2017-08-23'
    
    # Query for start date and above covering last year before most recent year
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    # Session close to free up memory
    session.close()

    one_start = [{'Min Temp': min, 'Avg Temp': avg, 'Max Temp': max} for min, avg, max in results]

    return jsonify(one_start)


@app.route("/api/v1.0/<start>")
def end_dt_tmp(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #end_date = '2017-08-23'
    
    # Query for start date and above covering last year before most recent year
    start_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    # Session close to free up memory
    session.close()

    inpt_start = [{'Min Temp': min, 'Avg Temp': avg, 'Max Temp': max} for min, avg, max in start_results]

    return jsonify(inpt_start)


# 
@app.route("/api/v1.0/<start>,<end>")
def start_end_dt(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    finds = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    # Converting list of tuples into normal list
    #all_finds = list(np.ravel(finds))

    start_end = [{'Min Temp': min, 'Avg Temp': avg, 'Max Temp': max} for min, avg, max in finds]  

    return jsonify(start_end)
    

# This section was inputed for when client requests are made but I thought it may be 
# too broad to tidy up for this HW. It defines end point generation for faulty entries
# by a client on the webpage.

# @app.route("/api/v1.0")
# def start_end():
    
#     start_dt = request.args.get('qs')
#     end_dt = request.args.get('qe')
    

#     if start_dt is None and end_dt is None:
#         results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).all()

#     elif start_dt is not None and end_dt is None:
#         results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start_dt).all()
    
#     elif start_dt is not None and end_dt is not None:
#         results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start_dt).filter(measurement.date <= end_dt).all()

#     else:
#         results = {f"There is nothing to show"}
#         return str(results)

    
    # session.close()
    # return jsonify(results)





# @app.route("/api/v1.0/<start>")

# @app.route("/api/v1.0/<start>/<end>")

# Defining the main module
if __name__ == "__main__":
    app.run(debug=True)


