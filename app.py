import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_year = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > '2016-08-22').\
    order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))
    all_precipitation = dict(last_year)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel3=[Measurement.tobs]
    active_station_temp = session.query(*sel3).\
    filter(Measurement.date > '2016-08-22',Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(active_station_temp))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temperature=[Measurement.station,
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
    start_temps = session.query(*temperature).\
        filter(Measurement.date >= start).all()


    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(start_temps))

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temperature=[Measurement.station,
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
    start_end_temps = session.query(*temperature).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()


    session.close()

    # Convert list of tuples into normal list
    all_ended_temps = list(np.ravel(start_end_temps))

    return jsonify(all_ended_temps)

if __name__ == '__main__':
    app.run(debug=True)
