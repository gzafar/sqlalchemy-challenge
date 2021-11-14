import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_data = session.query(measurement.date, measurement.prcp).all()

    session.close()

    all_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_data = session.query(station.station).all()

    session.close()

    all_stations = []
    for stat in stations_data:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    most_active_station_data = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281').first()

    session.close()

    all_tobs = []
    for date, tobs in most_active_station_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)
