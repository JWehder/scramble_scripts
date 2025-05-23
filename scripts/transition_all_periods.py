from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db, client
from flask_app.models import League

def transition_all_periods(tournament_id):
    # find all periods associated with this particular tournament
    periods = db.periods.find({"TournamentId": ObjectId(tournament_id)})
    league_ids = [period["LeagueId"] for period in periods]
 
    leagues = db.leagues.find({"_id": {"$in": league_ids}})

    for league in leagues:
        league = League(**league)

        league.start_new_period()
