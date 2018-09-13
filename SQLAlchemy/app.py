import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
    )




@app.route("/api/v1.0/precipitation")
def rain():
	rain_data = []
	for row in session.query(Measurement).filter(Measurement.date.between("2017-01-01","2017-12-31")):
		rain_info = {}
		rain_info["date"] = row.date
		rain_info["prcp"] = row.prcp
		rain_data.append(rain_info)
	return jsonify(rain_data)

@app.route("/api/v1.0/stations")
def stations():
	station_info = []
	for row in session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all():
		station_dict = {}
		station_dict["station"]= row.station
		station_dict["Total Active stations"] = row.func.count(Measurement.station)
		station_info.append(station_dict)
	return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
	temp_data = []
	for row in session.query(Measurement).filter(Measurement.date.between("2017-01-01","2017-12-31")):
		temp_info = {}
		temp_info["station"] = row.station
		temp_info["temp"] = row.tobs
		temp_data.append(temp_info)
	return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)

