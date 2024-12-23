 # build_database.py

from datetime import datetime
from config import app, db
from models import Trail, TrailFeatures, Feature, LocationPoint

TRAIL_FEATURES = [
    {
        "TrailName": "Plymouth Waterfront",
        "TrailSummary": "a waterfront path through plymouth",
        "TrailDescription": " a path along a waterfront in plymouth",
        "Difficulty": "Medium",
        "Location": "Plymouth, Devon",
        "Length": 70,
        "ElevationGain": 80,
        "RouteType": "Circular",
        "OwnerID": 1,
        "features": [
            ("Great spot to see deer early morning!"),
            ("Rocky path near the quarry needs good shoes."),
        ],
        "locationpoints": [
            (20, 30, "beach path"),
            (21, 35, "Woods entrance"),
            (26, 40, "Old building ruins")
        ],
        "owner": [
            ("grace@plymouth.ac.uk", "Admin")
        ]
    },
    {
        "TrailName": "Test Trail",
        "TrailSummary": "Sum",
        "TrailDescription": "Desc",
        "Difficulty": "Hard",
        "Location": "Test Site",
        "Length": 10,
        "ElevationGain": 100,
        "RouteType": "Linear",
        "OwnerID": 1,
        "features": [
            ("Lovely tea room at the old station building."),
            ("Watch out for cyclists on narrow sections."),
        ],
        "locationpoints": [
            (2, 6, "Bus stop"),
            (10, 9, "Subway tunnel"),
            (15, 11, "Tudor building")
        ],
        "owner": [
            ("ada@plymouth.ac.uk", "User")
        ]
        
    },
 ]

with app.app_context():
   db.create_all()
   for data in TRAIL_FEATURES:
       new_trail = Trail(TrailName=data.get("TrailName"), TrailSummary=data.get("TrailSummary"),
    TrailDescription=data.get("TrailDescription"), Difficulty=data.get("Difficulty"),
    Location=data.get("Location"), Length=data.get("Length")
    , ElevationGain=data.get("ElevationGain"), RouteType=data.get("RouteType"),
    OwnerID=data.get("OwnerID"))
       for content in data.get("features", []):
        new_trail.features.append(
            Feature(
                TrailFeature=content,
                )
                )
       for lat, long, desc in data.get("locationpoints", []):
        new_trail.locationpoints.append(
            LocationPoint(
                Latitude = lat,
                Longitude = long,
                Description= desc,
                )
                )
        
       db.session.add(new_trail)
   db.session.commit()