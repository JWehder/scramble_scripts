from pymongo import errors, UpdateOne
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.models import League, FantasyLeagueSeason
from flask_app.config import db, client

fantasy_league_season = db.fantasyLeagueSeasons.find_one({
    "_id": ObjectId("6786dddf987554debb88269e")
})

league = db.leagues.find_one({
    "_id": ObjectId('66cfb58fcb1c3460e49138c2')
})

with db.client.start_session() as db_session:
    with db_session.start_transaction():

        league_instance = League(**league)

        this_season_dict = FantasyLeagueSeason(**fantasy_league_season).dict(by_alias=True, exclude_unset=True)

        # Prepare operations for periods between tournaments
        operations = league_instance.create_periods_between_tournaments(this_season_dict)

        db.fantasyLeagueSeasons.update_one(
            {"_id": fantasy_league_season["_id"]},
            {"$set": {"Periods": operations["period_ids"]}}
        )

        # Execute operations for periods, drafts, and team results
        if operations["period_operations"]:
            db.periods.bulk_write(operations["period_operations"], session=db_session)
        if operations["draft_operations"]:
            db.drafts.bulk_write(operations["draft_operations"], session=db_session)
        if operations["team_result_operations"]:
            db.teamResults.bulk_write(operations["team_result_operations"], session=db_session)