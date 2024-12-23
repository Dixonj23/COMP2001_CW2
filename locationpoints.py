# locationpoints.py

from flask import abort, make_response

from config import db
from models import LocationPoint, Trail, TrailLocationPt, locationpt_schema

def read_one(LocationPointID):
    point = LocationPoint.query.get(LocationPointID)

    if point is not None:
        return locationpt_schema.dump(point)
    else:
        abort(
            404, f"Location point with ID {LocationPointID} not found"
        )


def update(LocationPointID, locationpoint):
    existing_point = LocationPoint.query.get(LocationPointID)

    if existing_point:
       update_point = locationpt_schema.load(locationpoint, session=db.session)
       existing_point.Latitude = update_point.Latitude
       existing_point.Longitude = update_point.Longitude
       existing_point.Description = update_point.Description
        
       db.session.merge(existing_point)
       db.session.commit()
       return locationpt_schema.dump(existing_point), 201
    else:
       abort(404, f"Location point with id {LocationPointID} not found")
		

def delete(LocationPointID):
    existing_point = LocationPoint.query.get(LocationPointID)
    if existing_point:
        # First, delete the corresponding TrailLocationPt link
        trail_location = TrailLocationPt.query.filter_by(LocationPointID=LocationPointID).all()
        for trail_pt in trail_location:
            db.session.delete(trail_pt)  # Remove the link from the link table

        # Now, delete the feature
        db.session.delete(existing_point)
            
        # Commit changes to the database
        db.session.commit()

        return make_response(f"Location point {LocationPointID} successfully deleted", 200)
		
    else:
	    abort(404, f"Location point with id {LocationPointID} not found")


def create(traillocation):
    trail_id = traillocation.get("TrailID")
    trail = Trail.query.get(trail_id)
    locationpt = {
        "LocationPointID": traillocation["LocationPointID"],
        "Latitude": traillocation["Latitude"],
        "Longitude": traillocation["Longitude"],
        "Description": traillocation["Description"],
    }
    

    if trail:
        new_locationpt = locationpt_schema.load(locationpt, session=db.session)
        trail.locationpoints.append(new_locationpt)
        db.session.commit()
        return locationpt_schema.dump(new_locationpt), 201
    else:
        abort(
            404, f"Trail not found for ID: {trail_id}"
        )