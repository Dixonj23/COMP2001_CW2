# features.py

from flask import abort, make_response

from config import db
from models import Feature, Trail, TrailFeatures, feature_schema

def read_one(FeatureID):
    feature = Feature.query.get(FeatureID)

    if feature is not None:
        return feature_schema.dump(feature)
    else:
        abort(
            404, f"Feature with ID {FeatureID} not found"
        )

def update(FeatureID, feature):
	existing_feature = Feature.query.get(FeatureID)

	if existing_feature:
		update_feature = feature_schema.load(feature, session=db.session)
		existing_feature.TrailFeature = update_feature.TrailFeature
		db.session.merge(existing_feature)
		db.session.commit()
		return feature_schema.dump(existing_feature), 201
	else:
		abort(404, f"Feature with id {FeatureID} not found")
		

def delete(FeatureID):
    existing_feature = Feature.query.get(FeatureID)
    if existing_feature:
        # First, delete the corresponding TrailFeature link
        trail_features = TrailFeatures.query.filter_by(FeatureID=FeatureID).all()
        for trail_feature in trail_features:
            db.session.delete(trail_feature)  # Remove the link from the link table

        # Now, delete the feature
        db.session.delete(existing_feature)
            
        # Commit changes to the database
        db.session.commit()

        return make_response(f"Feature {FeatureID} successfully deleted", 200)
		
    else:
	    abort(404, f"Feature with id {FeatureID} not found")


def create(trailfeature):
    trail_id = trailfeature.get("TrailID")
    trail = Trail.query.get(trail_id)
    feature = {
        "FeatureID": trailfeature["FeatureID"],
        "TrailFeature": trailfeature["TrailFeature"]
    }
    

    if trail:
        new_feature = feature_schema.load(feature, session=db.session)
        trail.features.append(new_feature)
        db.session.commit()
        return feature_schema.dump(new_feature), 201
    else:
        abort(
            404, f"Trail not found for ID: {trail_id}"
        )