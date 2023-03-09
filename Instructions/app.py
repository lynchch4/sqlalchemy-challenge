# Imports
import numpy as np
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify



app = Flask(__name__)

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measure = Base.classes.measurement

Station = Base.classes.station


# create api route
@app.route("/")
def home():

# list avaiable APIs
    return (
        f"Available Routes<br/>"
        f"Percipitation /api/v1.0/percipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/<start><br/>"
        f"Start Date and End Date: /api/v1.0/<start>/<end><br/>"
    )

# create api route
@app.route("/api/v1.0/percipitation")
def perc():

# Create session
    session = Session(engine)

# Create query for percipitation
    most_recent_date = session.query(Measure.date).order_by(Measure.date.desc()).first()
    recent_date = pd.to_datetime(most_recent_date).date[0]

    year_ago = recent_date - dt.timedelta(days=365)

    eq_stat = session.query(Measure.date, Measure.prcp).filter(Measure.date > year_ago).all()

    prcp_df = pd.DataFrame(eq_stat).sort_values(by=['date']).dropna()

    prcp_df = prcp_df.set_index('date')

    session.close()


# Create list for jsonify
    all_perc = list(np.ravel(eq_stat))
    
    return jsonify(all_perc)


# create api route
@app.route("/api/v1.0/stations")
def stat():

# Create session
    session = Session(engine)

 # Create query for stations   
    stations = session.query(Measure.station, func.count(Measure.station)).group_by(Measure.station).order_by(func.count(Measure.station).desc()).all()
    
    session.close()
    
# Create list for jsonify
    all_stat = list(np.ravel(stations))
    
    return jsonify(all_stat)


# create api route
@app.route("/api/v1.0/tobs")
def tobs():

# Create session
    session = Session(engine)
    
# Create query for temperatures    
    plot_stat = session.query(Measure.date, Measure.tobs).filter(Measure.station == 'USC00519281').filter(Measure.date > '2016-08-23').all()
     
    session.close()
    
# Create list for jsonify
    all_tobs = list(np.ravel(plot_stat))
    
    return jsonify(all_tobs)


# create api route
@app.route("/api/v1.0/<begin>")
def start(begin):

# Create session
    session = Session(engine)

# Create query for temperatures by dates    
    ev_stat_min = session.query(func.min(Measure.tobs)).filter(Measure.date >= (begin)).all()[0]
    ev_stat_max = session.query(func.max(Measure.tobs)).filter(Measure.date >= (begin)).all()[0]
    ev_stat_avg = session.query(func.avg(Measure.tobs)).filter(Measure.date >= (begin)).all()[0]

# create list for results
    begin_list = [ev_stat_min, ev_stat_avg, ev_stat_max]
   
    session.close()
    
# Create list for jsonify
    all_start = list(np.ravel(begin_list))
    
    return jsonify(all_start)


# create api route
@app.route("/api/v1.0/<begin>/<end>")
def end(begin, end):

# Create session
    session = Session(engine)

# Create query for temperatures by dates    
    ev_stat_min1 = session.query(func.min(Measure.tobs)).filter(Measure.date >= (begin), Measure.date <= (end)).all()[0]
    ev_stat_max1 = session.query(func.max(Measure.tobs)).filter(Measure.date >= (begin), Measure.date <= (end)).all()[0]
    ev_stat_avg1 = session.query(func.avg(Measure.tobs)).filter(Measure.date >= (begin), Measure.date <= (end)).all()[0]

#Create list for results
    end_list = [ev_stat_min1, ev_stat_avg1, ev_stat_max1]
   
    session.close()
    
# Create list for jsonify
    all_end = list(np.ravel(end_list))
    
    return jsonify(all_end)


# end results
if __name__ == "__main__":
    app.run(debug=True)