# trails.py

from flask import abort, make_response

from config import db
from models import Trail, trail_schema, trails_schema, User
from authenticator import Authenticate


def read_all(Email, Password):

	valid = Authenticate(Email, Password)

	if valid:
		trails = Trail.query.all()
		return trails_schema.dump(trails), 200
	else:
		abort(
				401,
				f"Invalid login details",
			)




def read_one(TrailName, Email, Password):
	trail = Trail.query.filter(Trail.TrailName == TrailName).one_or_none()

	valid = Authenticate(Email, Password)

	if valid:
		if trail is not None:
			return trail_schema.dump(trail)
		else:
			abort(
				404, f"Trail with name {TrailName} not found"
			)
	else:
		abort(
				401,
				f"Invalid login details",
			)



def create(trail, Email, Password):
	TrailName = trail.get("TrailName")
	existing_trail = Trail.query.filter(Trail.TrailName == TrailName).one_or_none()

	valid = Authenticate(Email, Password)
	
	if valid:
		if existing_trail is None:
			new_trail = {
				"TrailName": trail["TrailName"],
        		"TrailSummary": trail["TrailSummary"],
        		"TrailDescription": trail["TrailDescription"],
        		"Difficulty": trail["Difficulty"],
				"ElevationGain": trail["ElevationGain"],
				"Length": trail["Length"],
				"Location": trail["Location"],
				"OwnerID": trail["OwnerID"],
				"RouteType": trail["RouteType"],
    		}

			created_trail = trail_schema.load(new_trail, session=db.session)
			db.session.add(created_trail)
			db.session.commit()
			return trail_schema.dump(new_trail), 201

		else:
			abort(
				406,
				f"Trail with name {TrailName} already exists",
			)
	else:
		abort(
				401,
				f"Invalid login details",
			)



def update(TrailName, trail, Email, Password):
	existing_trail = Trail.query.filter(Trail.TrailName == TrailName).one_or_none()

	
	valid = Authenticate(Email, Password)
	
	if valid:
		if existing_trail:
			update_trail = trail_schema.load(trail, session=db.session)

			existing_trail.TrailSummary = update_trail.TrailSummary
			existing_trail.TrailDescription = update_trail.TrailDescription
			existing_trail.Difficulty = update_trail.Difficulty
			existing_trail.Location = update_trail.Location
			existing_trail.Length = update_trail.Length
			existing_trail.ElevationGain = update_trail.ElevationGain
			existing_trail.RouteType = update_trail.RouteType
			existing_trail.OwnerID = update_trail.OwnerID

			db.session.merge(existing_trail)
			db.session.commit()
			return trail_schema.dump(existing_trail), 201
		else:
			abort(404, f"Trail with name {TrailName} not found")
	else:
		abort(
				401,
				f"Invalid login details",
			)


def delete(TrailName, Email, Password):
	existing_trail = Trail.query.filter(Trail.TrailName == TrailName).one_or_none()
	valid = Authenticate(Email, Password)

	if valid:
		if existing_trail:
			db.session.delete(existing_trail)
			db.session.commit()
			return make_response(
				f"{TrailName} successfully deleted", 200
			)
		else:
			abort(
				404,
				f"Trail with name {TrailName} not found"
			)
	else:
		abort(
				401,
				f"Invalid login details",
			)
