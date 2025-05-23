from datetime import datetime, timedelta
from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.config import db

def get_closest_draft_date(tournament_start_date, draft_day_of_week):
    """
    Finds the closest draft date before the given tournament start date that does not overlap the tournament.

    :param tournament_start_date_str: The tournament start date as a string from the database.
    :param draft_day_of_week: The preferred draft day (e.g., "Saturday").
    :param draft_time: The preferred draft time in "HH:MM" format.
    :return: The calculated draft datetime.
    """
    # Convert draft day name to a corresponding integer (Monday=0, ..., Sunday=6)
    draft_day_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(draft_day_of_week)

    # Start from the latest possible draft date (7 days before the tournament start)
    closest_draft_date = tournament_start_date - timedelta(days=7)

    # Move to the nearest previous occurrence of the draft day
    while closest_draft_date.weekday() != draft_day_index:
        closest_draft_date += timedelta(days=1)  # Move fwd one day at a time
        # Ensure the draft does not overlap with the tournament
        if closest_draft_date >= tournament_start_date:
            closest_draft_date -= timedelta(weeks=2)  # Move back another week if necessary

    return closest_draft_date.date()

tournament = db.tournaments.find_one({
    "_id": ObjectId('6776de93202130da68f72a0e')
})

start_date = tournament["StartDate"]
draft_day_of_week = "Wednesday"

closest_draft_date = get_closest_draft_date(start_date, draft_day_of_week)
print(closest_draft_date)